import type { Register } from 'claude-code'
import type { PanelImage, PanelSnapshot } from '../../types'

const TOOL = 'mcp__pixellab-pip__panel'
const PANE = 'pixellab-pip-panel'
const MAX_SNAPSHOT = 12 * 1024 * 1024
const SVG_LIMIT = 120000
const LABEL_KEYS = ['title', 'project', 'run', 'style', 'none', 'snapshot', 'snapshot_help', 'charged', 'committed', 'unknown',
  'preview_alt', 'note', 'request', 'redo', 'animate', 'refresh', 'policy', 'empty_note', 'style_none',
  'draft_ready', 'draft_unavailable', 'no_images', 'native_preview_unavailable', 'setup',
  'new_character', 'new_attack', 'new_skill', 'character_prompt', 'attack_prompt', 'skill_prompt']
let snapshot: PanelSnapshot | null = null
let snapshotPath = ''
let note = ''
let error = ''

const absolute = (value: unknown): value is string =>
  typeof value === 'string' && (/^\//.test(value) || /^[A-Za-z]:[\\/]/.test(value) || /^\\\\[^\\]+\\[^\\]+/.test(value))
const text = (value: unknown, limit = 4096): value is string => typeof value === 'string' && value.length <= limit
const relative = (value: unknown): value is string =>
  text(value) && value.length > 0 && !absolute(value) && !value.includes('\\') &&
  !value.includes(':') && value.split('/').every(part => part !== '' && part !== '.' && part !== '..')
const digest = (value: unknown): value is string => typeof value === 'string' && /^[a-f0-9]{64}$/.test(value)
const amount = (value: unknown) => value === null || (typeof value === 'number' && Number.isFinite(value) && value >= 0)
const object = (value: unknown): value is Record<string, any> => !!value && typeof value === 'object' && !Array.isArray(value)
const xml = (value: string) => value.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[c]!))
const normalized = (path: string) => /^[A-Za-z]:|^\\\\/.test(path) ? path.replace(/\\/g, '/').toLowerCase().replace(/\/$/, '') : path.replace(/\/$/, '')

export function parseSnapshot(raw: string): PanelSnapshot {
  if (raw.length > MAX_SNAPSHOT) throw new Error('Panel snapshot is too large; rebuild a smaller explicit selection.')
  const s = JSON.parse(raw)
  if (!object(s) || s.version !== 1 || typeof s.review_ready !== 'boolean' || !absolute(s.project) || !text(s.project) ||
      !(s.run === null || relative(s.run)) || !text(s.created_at, 64) || !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|\+00:00)$/.test(s.created_at) || !Number.isFinite(Date.parse(s.created_at)) ||
      !text(s.style) || !object(s.usage) || !amount(s.usage.charged) || !amount(s.usage.committed) ||
      !object(s.labels) || Object.keys(s.labels).length > 100 || !Object.values(s.labels).every(value => text(value, 2048) && value.trim().length > 0) ||
      !LABEL_KEYS.every(key => typeof s.labels[key] === 'string') ||
      !(s.manifest_sha256 === null || digest(s.manifest_sha256)) ||
      !Array.isArray(s.jobs) || s.jobs.length > 1000 || !s.jobs.every((j: unknown) => object(j) &&
        text(j.job_id) && (j.tool === undefined || text(j.tool)) && (j.status === undefined || text(j.status)) && (j.outcome === undefined || text(j.outcome))) ||
      !Array.isArray(s.warnings) || s.warnings.length > 100 || !s.warnings.every((w: unknown) => text(w)) ||
      !Array.isArray(s.images) || s.images.length > 32 || !s.images.every((i: unknown) => object(i) &&
        text(i.role, 128) && i.role.length > 0 && relative(i.path) && digest(i.sha256) &&
        text(i.data_url, MAX_SNAPSHOT) && /^data:image\/(png|gif);base64,[A-Za-z0-9+/]+={0,2}$/.test(i.data_url) &&
        Number.isInteger(i.width) && i.width > 0 && i.width <= 16384 &&
        Number.isInteger(i.height) && i.height > 0 && i.height <= 16384)) {
    throw new Error('Invalid panel snapshot. Rebuild it with the Pip panel helper.')
  }
  return s as PanelSnapshot
}

export function previewSvg(images: PanelImage[]): string | null {
  if (!images.length || images.some(i => !i.data_url.startsWith('data:image/png;base64,'))) return null
  const height = Math.max(...images.map(i => i.height))
  const width = images.reduce((sum, i) => sum + i.width + 8, -8)
  let x = 0
  let body = ''
  for (const image of images) {
    body += `<image href="${image.data_url}" x="${x}" y="${height - image.height}" width="${image.width}" height="${image.height}"/>` +
      `<text x="${x}" y="${height + 14}" font-size="12" fill="gray">${xml(image.role)}</text>`
    x += image.width + 8
  }
  const result = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height + 20}" style="image-rendering:pixelated">${body}</svg>`
  return result.length <= SVG_LIMIT ? result : null
}

async function load($: any, path: string) {
  if (!absolute(path) || !text(path) || !/\.json$/i.test(path)) throw new Error('snapshot_path must be an absolute JSON file path.')
  const raw = await $.fs.read(path)
  if (typeof raw !== 'string') throw new Error('Could not read the panel snapshot as JSON text.')
  const next = parseSnapshot(raw)
  if (!normalized(path).startsWith(normalized(next.project) + '/') || path.replace(/\\/g, '/').split('/').some(part => part === '..' || part === '.')) {
    throw new Error('The snapshot must be inside its selected project root.')
  }
  // Embedded previews must identify the bytes they actually show. Pip's verify command separately checks current disk state.
  for (const image of next.images) {
    const bytes = Uint8Array.fromBase64(image.data_url.split(',')[1])
    if (image.data_url.startsWith('data:image/png;')) {
      const be = (offset: number) => bytes[offset] * 16777216 + bytes[offset + 1] * 65536 + bytes[offset + 2] * 256 + bytes[offset + 3]
      if (bytes.length < 24 || ![137, 80, 78, 71, 13, 10, 26, 10].every((value, index) => bytes[index] === value) ||
          String.fromCharCode(...bytes.slice(12, 16)) !== 'IHDR' || be(16) !== image.width || be(20) !== image.height) {
        throw new Error('A PNG preview does not match its declared dimensions; rebuild the snapshot.')
      }
    }
    const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))).map(n => n.toString(16).padStart(2, '0')).join('')
    if (hash !== image.sha256) throw new Error('An embedded preview does not match its content digest; rebuild the snapshot.')
  }
  snapshot = next
  snapshotPath = path
  error = ''
  $.ui.invalidate('ui.render')
}

async function draft($: any, action: string, s: PanelSnapshot, path: string) {
  if (action === 'request' && !note.trim()) {
    $.ui.toast(s.labels.empty_note)
    return
  }
  const payload = { action, project: s.project, run: s.run, snapshot_path: path,
    created_at: s.created_at, manifest_sha256: s.manifest_sha256,
    images: s.images.map(({ role, path, sha256 }) => ({ role, path, sha256 })), note }
  try {
    const result = await $.prompt.fill({
      text: '\nPixelLab Pip panel request\n' + JSON.stringify(payload, null, 2), mode: 'append',
    })
    $.ui.toast(result.isFilled ? s.labels.draft_ready : s.labels.draft_unavailable)
  } catch {
    $.ui.toast(s.labels.draft_unavailable)
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({ name: 'panel', description: 'Open the read-only PixelLab Pip panel for an explicit panel.py JSON snapshot. No generation, settings changes or automatic approvals.',
      inputSchema: { type: 'object', properties: { snapshot_path: { type: 'string', description: 'Absolute path to the generated panel.json' } }, required: ['snapshot_path'], additionalProperties: false } })
    return next(e)
  })

  on('tool.call', { tool: TOOL }, async ($, e: any) => {
    try {
      const surfaces = await $.session.surfaces()
      if (!surfaces.length) return { result: 'Native panel unavailable: this session has no interactive surface. Use the portable panel.html and return feedback in chat.' }
      note = ''
      await load($, e.snapshot_path)
      const htmlPath = e.snapshot_path.replace(/[^/\\]+$/, 'panel.html')
      const placed = await $.ui.open({ id: PANE, title: snapshot!.labels.title, focus: true, closeOnEscape: true })
      if (!placed.isPlaced) return { result: 'The host did not place the native panel. Open the portable HTML: ' + htmlPath + ' and return feedback in chat.' }
      const previewsUnavailable = snapshot!.images.length > 0 &&
        (!surfaces.some((surface: string) => surface === 'desktop' || surface === 'vscode') || !previewSvg(snapshot!.images))
      return { result: 'PixelLab Pip snapshot panel opened. Requests become chat drafts; no paid work or settings changes were performed.' +
        (previewsUnavailable ? ' This native surface or selection cannot show every selected preview. Open the portable HTML: ' + htmlPath + ' and return feedback in chat.' : '') }
    } catch (failure: any) {
      snapshot = null
      error = String(failure?.message || failure)
      $.ui.invalidate('ui.render')
      return { result: 'Native panel unavailable: ' + error +
        ' Open the generated panel.html for a helper-built snapshot. Rebuild invalid or stale snapshots; use a smaller selection if this host rejects the snapshot size.' }
    }
  }).catch(($: any) => ({ result: 'Native panel unavailable in this host. Use the portable panel.html and return feedback in chat.' }))

  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    if (e.requestId !== PANE) return next(e)
    const { Box, Text, Button, Input, Svg } = $.ui.resolve(e) as any
    const s = snapshot
    if (!s) return <Text>{error || 'Open /pixellab-pip panel to select a project and run.'}</Text>
    const path = snapshotPath
    const l = s.labels
    const svg = previewSvg(s.images)
    const visible = (e.surface === 'desktop' || e.surface === 'vscode') && !!Svg && !!svg
    const canReview = visible && s.review_ready && !!s.run && !!s.manifest_sha256 && s.images.length > 0
    return <Box flexDirection="column" gap={1}>
      <Text bold>{l.title}</Text>
      <Text>{l.project + ': ' + s.project + '\n' + l.run + ': ' + (s.run || l.none) + '\n' + l.style + ': ' + (s.style || l.style_none)}</Text>
      <Text>{l.snapshot + ': ' + s.created_at + '\n' + l.snapshot_help}</Text>
      <Text>{l.charged + ': ' + (s.usage.charged === null ? l.unknown : s.usage.charged) +
        '\n' + l.committed + ': ' + (s.usage.committed === null ? l.unknown : s.usage.committed)}</Text>
      {s.jobs.map((job, i) => <Text key={'job-' + i}>{[job.job_id, job.tool, job.status, job.outcome].filter(Boolean).join(' · ')}</Text>)}
      {s.warnings.map((warning, i) => <Text key={'warning-' + i}>{warning}</Text>)}
      {visible ? <Svg source={svg!} alt={l.preview_alt} /> : <Text>{s.images.length ? l.native_preview_unavailable : l.no_images}</Text>}
      {s.images.map((image, i) => <Text key={'image-' + i}>{image.role + ': ' + image.path + '\nSHA-256: ' + image.sha256}</Text>)}
      <Box flexDirection="row" gap={1}>
        <Button key="new-character" label={l.new_character} onPress={() => { note = l.character_prompt; $.ui.invalidate('ui.render') }} />
        <Button key="new-attack" label={l.new_attack} onPress={() => { note = l.attack_prompt; $.ui.invalidate('ui.render') }} />
        <Button key="new-skill" label={l.new_skill} onPress={() => { note = l.skill_prompt; $.ui.invalidate('ui.render') }} />
      </Box>
      <Input key="note" label={l.note} value={note} onInput={(value: string) => { note = value; $.ui.invalidate('ui.render') }} onSubmit={(value: string) => { note = value; $.ui.invalidate('ui.render') }} />
      <Button key="request" label={l.request} onPress={() => void draft($, 'request', s, path)} />
      {canReview && <Button key="redo" label={l.redo} onPress={() => void draft($, 'redo', s, path)} />}
      {canReview && <Button key="animate" label={l.animate} onPress={() => void draft($, 'animate', s, path)} />}
      <Button key="setup" label={l.setup} onPress={() => void draft($, 'setup', s, path)} />
      <Button key="refresh" label={l.refresh} onPress={async () => {
        try { await load($, path) } catch (failure: any) { snapshot = null; error = String(failure?.message || failure); $.ui.invalidate('ui.render') }
      }} />
      <Text dimColor>{l.policy}</Text>
    </Box>
  })
}
