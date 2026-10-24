import type { Register } from 'claude-code'
import type { PanelImage, PanelSnapshot } from './types'

const TOOL = 'mcp__pixellab-pip__panel'
const PANE = 'pixellab-pip-panel'
const MAX_SNAPSHOT = 4 * 1024 * 1024
const SVG_LIMIT = 120000
const PREVIEW_WIDTH = 320
const LABEL_KEYS = ['title', 'project', 'run', 'style', 'none', 'snapshot', 'snapshot_help', 'charged', 'committed', 'unknown',
  'preview_alt', 'note', 'request', 'redo', 'animate', 'policy_short', 'empty_note', 'style_none',
  'draft_ready', 'draft_unavailable', 'no_images', 'native_preview_unavailable', 'setup',
  'new_character', 'new_attack', 'new_skill', 'character_prompt', 'attack_prompt', 'skill_prompt',
  'open_review', 'open_failed', 'opened_review', 'welcome', 'guide', 'guide_prompt', 'feedback_intro',
  'input_unavailable', 'native_image_unavailable']
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
const normalized = (path: string) => /^[A-Za-z]:|^\\\\/.test(path) ? path.replace(/\\/g, '/').toLowerCase().replace(/\/$/, '') : path.replace(/\/$/, '')
const basename = (path: string) => path.replace(/\\/g, '/').replace(/\/$/, '').split('/').pop() || path

export function parseSnapshot(raw: string): PanelSnapshot {
  if (new TextEncoder().encode(raw).length > MAX_SNAPSHOT) throw new Error('Panel snapshot exceeds this host’s 4 MiB limit; use the full HTML review or rebuild a smaller explicit selection.')
  const s = JSON.parse(raw)
  if (object(s) && s.lang === undefined) s.lang = 'en'
  if (!object(s) || s.version !== 1 || typeof s.review_ready !== 'boolean' || !absolute(s.project) || !text(s.project) ||
      !text(s.lang, 64) || !/^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$/.test(s.lang) ||
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

export function previewStrips(images: PanelImage[]) {
  const groups: PanelImage[][] = []
  const unavailable: PanelImage[] = []
  const svg = (group: PanelImage[], width: number) => {
    const height = Math.max(...group.map(image => image.height))
    let x = 0
    const body = group.map(image => {
      const element = `<image href="${image.data_url}" x="${x}" y="${height - image.height}" width="${image.width}" height="${image.height}"/>`
      x += image.width + 8
      return element
    }).join('')
    return { source: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" style="image-rendering:pixelated">${body}</svg>`, width, height, images: group }
  }
  const width = (group: PanelImage[]) => group.reduce((sum, image) => sum + image.width + 8, -8)
  for (const image of images) {
    if (!image.data_url.startsWith('data:image/png;base64,') || svg([image], image.width).source.length > SVG_LIMIT) {
      unavailable.push(image)
      continue
    }
    const last = groups[groups.length - 1]
    if (last && width([...last, image]) <= PREVIEW_WIDTH / 2 &&
        svg([...last, image], width([...last, image])).source.length <= SVG_LIMIT) last.push(image)
    else groups.push([image])
  }
  // One integer scale keeps small sprites readable without changing relative pixel sizes.
  const sharedWidth = Math.max(1, ...groups.map(width))
  const scale = Math.max(1, Math.min(4, Math.floor(PREVIEW_WIDTH / sharedWidth)))
  return { strips: groups.map(group => ({ ...svg(group, sharedWidth), scale })), unavailable }
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
    const sentence = s.labels.feedback_intro + ': ' + s.labels[action] + (note.trim() ? ' — ' + note.trim() : '')
    const result = await $.prompt.fill({
      text: '\n' + sentence + '\n\n```json\n' + JSON.stringify(payload) + '\n```\n', mode: 'append',
    })
    $.ui.toast(result.isFilled ? s.labels.draft_ready : s.labels.draft_unavailable)
  } catch {
    $.ui.toast(s.labels.draft_unavailable)
  }
}

async function openReview($: any, s: PanelSnapshot, path: string) {
  const args = [$.plugin.root + '/skills/pixellab-pip/assets/panel.py', 'open', path]
  try {
    const python = /^[A-Za-z]:|^\\\\/.test(path) ? 'python' : 'python3'
    const result = await $.process.run([python, ...args], { cwd: $.plugin.root })
    if (result.exitCode !== 0 || JSON.parse(result.stdout).opened !== true) throw new Error('Review opener did not confirm success.')
    $.ui.toast(s.labels.opened_review)
  } catch { $.ui.toast(s.labels.open_failed) }
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
        (!surfaces.some((surface: string) => surface === 'desktop' || surface === 'vscode') || previewStrips(snapshot!.images).unavailable.length > 0)
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
    const canInput = !!Input && e.surface !== 'mobile'
    const s = snapshot
    if (!s) return <Text>{error || 'Open /pixellab-pip panel to select a project and run.'}</Text>
    const path = snapshotPath
    const l = s.labels
    const { strips, unavailable } = previewStrips(s.images)
    const visible = (e.surface === 'desktop' || e.surface === 'vscode') && !!Svg
    const canReview = visible && !unavailable.length && s.review_ready && !!s.run && !!s.manifest_sha256 && s.images.length > 0
    const empty = !s.run && !s.images.length
    return <Box flexDirection="column" gap={1}>
      <Text bold>{l.title}</Text>
      <Text>{l.project + ': ' + basename(s.project) + '\n' + l.run + ': ' + (s.run ? basename(s.run) : l.none) + '\n' + l.style + ': ' + (s.style || l.style_none)}</Text>
      <Text>{l.snapshot + ': ' + s.created_at}</Text>
      <Text>{l.charged + ': ' + (s.usage.charged === null ? l.unknown : s.usage.charged) +
        '\n' + l.committed + ': ' + (s.usage.committed === null ? l.unknown : s.usage.committed)}</Text>
      {s.warnings.map((warning, i) => <Text key={'warning-' + i}>{warning}</Text>)}
      {empty && <Text>{l.welcome}</Text>}
      {visible && strips.map((strip, i) => <Box key={'strip-' + i} flexDirection="column">
        <Svg source={strip.source} width={strip.width * strip.scale} height={strip.height * strip.scale} alt={l.preview_alt} />
        <Text>{strip.images.map(image => image.role).join(' · ')}</Text>
      </Box>)}
      {(visible ? unavailable : s.images).map((image, i) => <Text key={'unavailable-' + i}>{image.role + ': ' + l.native_image_unavailable}</Text>)}
      {!s.images.length && !empty && <Text>{l.no_images}</Text>}
      {!visible && s.images.length > 0 && <Text>{l.native_preview_unavailable}</Text>}
      {e.surface !== 'mobile' && <Button key="open-review" label={l.open_review} onPress={() => void openReview($, s, path)} />}
      {canInput && empty && <Box flexDirection="row" gap={1}>
        <Button key="new-character" label={l.new_character} onPress={() => { note = l.character_prompt; $.ui.invalidate('ui.render') }} />
        <Button key="new-attack" label={l.new_attack} onPress={() => { note = l.attack_prompt; $.ui.invalidate('ui.render') }} />
        <Button key="new-skill" label={l.new_skill} onPress={() => { note = l.skill_prompt; $.ui.invalidate('ui.render') }} />
      </Box>}
      {canInput ? <Input key="note" label={l.note} value={note} onInput={(value: string) => { note = value; $.ui.invalidate('ui.render') }} onSubmit={(value: string) => { note = value; $.ui.invalidate('ui.render') }} /> : <Text>{l.input_unavailable}</Text>}
      {canInput && <Button key="request" label={l.request} onPress={() => void draft($, 'request', s, path)} />}
      {canReview && <Button key="redo" label={l.redo} onPress={() => void draft($, 'redo', s, path)} />}
      {canReview && <Button key="animate" label={l.animate} onPress={() => void draft($, 'animate', s, path)} />}
      {empty && <Button key="guide" label={l.guide} onPress={() => { if (!note.trim()) note = l.guide_prompt; void draft($, 'guide', s, path) }} />}
      {empty && <Button key="setup" label={l.setup} onPress={() => void draft($, 'setup', s, path)} />}
      <Text dimColor>{l.policy_short}</Text>
    </Box>
  })
}
