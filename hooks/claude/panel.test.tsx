import { expect, test } from 'claude-code/testing'
import { parseSnapshot, previewStrips } from './register'

const PATH = '/project-b/review/panel.json'
const TOOL = 'mcp__pixellab-pip__panel'
const pane = (surface: string) => ({ plugin: 'pixellab-pip', surface, component: 'Pane', requestId: 'pixellab-pip-panel',
  props: { title: 'PixelLab Pip', isFocused: false, bodyColumns: 60, placement: 'dock', scroll: { offset: 0, bodyRows: 40 }, view: {} } })

// Captured from panel.build_snapshot with a real Pillow PNG and manifest; only the absolute project path is anonymized.
const BUILDER_SNAPSHOT = {
  "version": 1,
  "lang": "en",
  "project": "/project-b",
  "run": "pixellab-pip-generations/run",
  "created_at": "2026-10-23T20:34:36.497299Z",
  "style": "chosen",
  "labels": {
    "title": "PixelLab Pip review panel",
    "project": "Project",
    "run": "Run",
    "style": "Saved appearance",
    "none": "none selected",
    "snapshot": "Snapshot",
    "snapshot_help": "Not live. Run /pixellab-pip panel again in a fresh output directory to refresh.",
    "charged": "charged generations",
    "committed": "committed generations",
    "unknown": "unknown",
    "preview_alt": "Selected preview",
    "preview_unavailable": "Preview could not be displayed. Open the original and rebuild the panel.",
    "no_images": "No previews selected. Ask the agent to open the panel with explicit image roles and paths.",
    "note": "Request or correction notes",
    "request": "Compose request",
    "redo": "Request redo",
    "animate": "Request animation",
    "open_review": "Open full review",
    "open_failed": "Could not open full review. Ask the agent for its HTML link.",
    "opened_review": "Requested the full review in your browser.",
    "welcome": "Start a project or describe what you want to make.",
    "guide": "Guided first project",
    "guide_prompt": "Guide me through my first PixelLab project.",
    "feedback_intro": "Please review this request for the selected project.",
    "policy_short": "Compose a request, then send it in chat. Nothing runs from this panel.",
    "input_unavailable": "This surface cannot edit notes. Use the full review or agent chat.",
    "native_image_unavailable": "Open full review for this preview.",
    "setup": "Request project setup",
    "native_preview_unavailable": "This native surface or selection cannot show every preview. Open the sibling panel.html in a browser; redo and animation requests are unavailable here until every selected image can be reviewed.",
    "policy": "This snapshot does not submit work or change settings. Compose a request, then send it in the agent chat. The agent must verify the current files and apply Pip’s normal routing and approval rules.",
    "empty_note": "Enter a request first.",
    "draft_ready": "Request composed. Send it in chat; no work has been submitted.",
    "draft_unavailable": "Could not place the request in chat. Copy it manually.",
    "usage_scope": "Selected run only",
    "cost_explanation": "reported charges or unresolved estimates",
    "previews": "Selected previews",
    "scale": "Shared pixel scale",
    "jobs": "Selected run jobs",
    "job": "Job",
    "tool": "Tool",
    "status": "Status",
    "outcome": "Outcome",
    "not_recorded": "not recorded",
    "compose_heading": "Compose a request",
    "new_character": "New character",
    "new_attack": "New attack",
    "new_skill": "New skill",
    "character_prompt": "Make a new character: ",
    "attack_prompt": "Make an attack animation: ",
    "skill_prompt": "Make a skill animation: ",
    "note_placeholder": "Describe what you want or what should change.",
    "feedback_label": "Request to send in chat",
    "copy_request": "Copy request",
    "review_blocked": "Redo/animation composition requires an identifiable selected run and every selected preview. Resolve unavailable previews in chat first.",
    "send_request": "Send request to chat",
    "send_title": "Send this PixelLab Pip request to chat?",
    "host_handoff": "Request handed to the host for confirmation. It may be canceled; this panel has not approved or run a generation.",
    "send_unavailable": "The host could not receive the request. Copy it and send it in chat instead.",
    "copy_empty": "Compose a request first.",
    "copied": "Copied. Paste and send it in chat.",
    "copy_unavailable": "Clipboard access unavailable. Copy the selected request manually and send it in chat.",
    "style_none": "No saved style",
    "style_project": "Project appearance",
    "style_unavailable": "Style unavailable"
  },
  "usage": {
    "charged": 0,
    "committed": 0
  },
  "jobs": [
    {
      "job_id": "one",
      "tool": "generate",
      "status": "failed"
    }
  ],
  "images": [
    {
      "role": "standing",
      "path": "pixellab-pip-generations/run/standing.png",
      "sha256": "8e14bb85d64f8c7b12541e72b7c39686fae398fb222a3c75388f2e87ee5b2cbb",
      "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGO4o+H2HwAFeAJKMbwy1wAAAABJRU5ErkJggg==",
      "width": 1,
      "height": 1
    }
  ],
  "manifest_sha256": "f04f3fc7776c47713552e988ca75f0a606bded9e8375ef4522b82017b59cfa02",
  "warnings": [],
  "review_ready": true
}

async function fixture() {
  return JSON.parse(JSON.stringify(BUILDER_SNAPSHOT))
}

const requestFromDraft = (value: string) => JSON.parse(value.split('```json\n')[1].split('\n```')[0])

function engine(on: any, raw: () => string, surfaces = ['desktop'], fills = true) {
  const drafts: any[] = []
  const registrations: any[] = []
  const writes: any[] = []
  const toasts: string[] = []
  on('tool.register', (_: any, e: any) => { registrations.push(e); return { value: undefined } })
  on('session.start', () => ({ cwd: '/project-a' }))
  on('session.surfaces', () => ({ value: surfaces }))
  on('fs.read', (_: any, e: any) => { if (e.path.replace(/^[A-Za-z]:/, '').replace(/\\/g, '/') !== PATH) throw new Error('unexpected path'); return { value: raw() } })
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('ui.toast', (_: any, e: any) => { toasts.push(e.text); return { value: undefined } })
  on('prompt.fill', (_: any, e: any) => { drafts.push(e); return { isFilled: fills, text: e.text, cursor: e.text.length } })
  on('fs.write', (_: any, e: any) => { writes.push(e); throw new Error('panel must not write') })
  return { drafts, registrations, writes, toasts }
}

test('panel tool registers without adding a competing command or connector', async ($, on) => {
  const s = await fixture()
  const h = engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  expect(h.registrations[0].name).toBe('panel')
  const result: any = await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  expect(result.result).toContain('opened')
  expect(h.writes.length).toBe(0)
})

test('visual review requests preserve selected project B rather than session project A, digest and zero cost', async ($, on) => {
  const s = await fixture()
  const h = engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  expect(await ui.find({ type: 'Svg' })).toBeDefined()
  expect((await ui.find({ type: 'Text', text: /charged generations/ }))?.text).toContain('charged generations: 0')
  await ui.input({ key: 'note', text: 'Change the silhouette.' })
  await ui.press({ key: 'animate' })
  const request = requestFromDraft(h.drafts[0].text)
  expect(request.project).toBe('/project-b')
  expect(request.run).toBe(s.run)
  expect(request.images[0].sha256).toBe(s.images[0].sha256)
  expect(request.manifest_sha256).toBe(s.manifest_sha256)
  expect(request.note).toBe('Change the silhouette.')
  expect(h.drafts[0].mode).toBe('append')
  expect(h.writes.length).toBe(0)
  await ui.unmount()
})

test('unsupported terminal images omit animation and redo controls', async ($, on) => {
  const s = await fixture()
  engine(on, () => JSON.stringify(s), ['terminal'])
  await $.session.start({ cwd: '/project-a', surface: 'terminal', isInteractive: true })
  const result: any = await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  expect(result.result).toContain('Open the portable HTML: /project-b/review/panel.html')
  const terminal = await $.ui.mount(pane('terminal') as any)
  expect(await terminal.find({ key: 'animate' })).toBeUndefined()
  expect(await terminal.find({ type: 'Text', text: /cannot show every preview/ })).toBeDefined()
  await terminal.unmount()
})

test('GIF selection reports its exact portable fallback to the agent', async ($, on) => {
  const s = await fixture()
  const gif = Uint8Array.fromBase64('R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==')
  s.images[0].data_url = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='
  s.images[0].sha256 = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', gif))).map(n => n.toString(16).padStart(2, '0')).join('')
  engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  const result: any = await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  expect(result.result).toContain('cannot show every selected preview')
  expect(result.result).toContain('/project-b/review/panel.html')
  const ui = await $.ui.mount(pane('desktop') as any)
  expect(await ui.find({ key: 'animate' })).toBeUndefined()
  await ui.unmount()
})

test('accounting warnings do not prevent composing requests when art review is ready', async ($, on) => {
  const s = await fixture()
  s.warnings.push('The manifest has an unresolved charge.')
  engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'vscode', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('vscode') as any)
  expect(await ui.find({ type: 'Svg' })).toBeDefined()
  expect(await ui.find({ key: 'animate' })).toBeDefined()
  expect(await ui.find({ key: 'redo' })).toBeDefined()
  await ui.unmount()
})

test('incomplete selected previews disable review controls independently of warnings', async ($, on) => {
  const s = await fixture()
  s.review_ready = false
  engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  expect(await ui.find({ key: 'animate' })).toBeUndefined()
  expect(await ui.find({ key: 'redo' })).toBeUndefined()
  await ui.unmount()
})

test('localized shared labels and user feedback remain literal', async ($, on) => {
  const s = await fixture()
  s.labels.project = 'プロジェクト'
  s.labels.animate = 'アニメーションを依頼'
  s.labels.note = '修正内容'
  const h = engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  expect((await ui.find({ type: 'Text', text: /プロジェクト/ }))?.text).toContain('project-b')
  expect((await ui.find({ key: 'animate' }))?.props.label).toBe('アニメーションを依頼')
  await ui.input({ key: 'note', text: 'シルエットを直してください。' })
  await ui.press({ key: 'redo' })
  expect(requestFromDraft(h.drafts[0].text).note).toBe('シルエットを直してください。')
  await ui.unmount()
})

test('a malformed PNG cannot enable native review requests', async ($, on) => {
  const s = await fixture()
  s.images[0].width = 2
  engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  const result: any = await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  expect(result.result).toContain('declared dimensions')
})

test('snapshots outside their selected project are rejected', async ($, on) => {
  const s = await fixture()
  s.project = '/other-project'
  engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  const result: any = await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  expect(result.result).toContain('selected project root')
})

test('refused draft filling reports copy-back fallback without submitting a turn', async ($, on) => {
  const s = await fixture()
  const { toasts } = engine(on, () => JSON.stringify(s), ['desktop'], false)
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  await ui.press({ key: 'animate' })
  expect(toasts.join(' ')).toContain(s.labels.draft_unavailable)
  await ui.unmount()
})

test('no interactive surface returns an explicit portable fallback', async ($, on) => {
  engine(on, () => '', [])
  await $.session.start({ cwd: '/project-a', surface: null, isInteractive: false })
  const result: any = await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  expect(result.result).toContain('no interactive surface')
})

test('reopening rejects mismatched same-length embedded content without a misleading reload control', async ($, on) => {
  const s = await fixture()
  let raw = JSON.stringify(s)
  engine(on, () => raw)
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  expect(await ui.find({ key: 'refresh' })).toBeUndefined()
  s.images[0].sha256 = 'b'.repeat(64)
  raw = JSON.stringify(s)
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  expect(await ui.find({ type: 'Text', text: /does not match its content digest/ })).toBeDefined()
  expect(await ui.find({ key: 'animate' })).toBeUndefined()
  await ui.unmount()
})

test('invalid snapshots reject unsafe paths, remote previews and invalid accounting', async () => {
  const s = await fixture()
  for (const mutate of [
    (v: any) => { v.images[0].path = '../outside.png' },
    (v: any) => { v.images[0].data_url = 'https://example.invalid/private.png' },
    (v: any) => { v.usage.charged = -1 },
    (v: any) => { v.images[0].width = 0 },
  ]) {
    const value = JSON.parse(JSON.stringify(s))
    mutate(value)
    expect(() => parseSnapshot(JSON.stringify(value))).toThrow()
  }
  expect(() => parseSnapshot(JSON.stringify(s))).not.toThrow()
  const legacy = { ...s, created_at: '2026-01-01T00:00:00+00:00', jobs: [{ job_id: 'legacy' }] }
  expect(() => parseSnapshot(JSON.stringify(legacy))).not.toThrow()
})

test('bounded SVG strips retain supported PNGs beside GIFs and oversized images at one shared scale', async () => {
  const s = await fixture()
  s.images[0].role = '<script>&'
  const selected = [
    { ...s.images[0], data_url: 'data:image/png;base64,' + 'A'.repeat(80000), width: 16 },
    { ...s.images[0], data_url: 'data:image/png;base64,' + 'B'.repeat(80000), width: 32 },
    { ...s.images[0], data_url: 'data:image/gif;base64,R0lGODlh' },
    { ...s.images[0], data_url: 'data:image/png;base64,' + 'A'.repeat(130000) },
  ]
  const result = previewStrips(selected)
  expect(result.strips.length).toBe(2)
  expect(result.unavailable.length).toBe(2)
  expect(result.strips[0].width).toBe(32)
  expect(result.strips[1].width).toBe(32)
  expect(result.strips[0].source).toContain('viewBox="0 0 32 1"')
  expect(result.strips[1].source).toContain('viewBox="0 0 32 1"')
  expect(result.strips[0].source).toContain('width="16"')
  expect(result.strips[1].source).toContain('width="32"')
  expect(result.strips.every(strip => strip.source.length <= 120000)).toBe(true)
  expect(result.strips[0].source).not.toContain('<script>')
})

test('a mixed GIF and PNG selection retains its still preview without approving unseen animation', async ($, on) => {
  const s = await fixture()
  const data_url = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='
  const bytes = Uint8Array.fromBase64(data_url.split(',')[1])
  const sha256 = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))).map(n => n.toString(16).padStart(2, '0')).join('')
  s.images.push({ ...s.images[0], role: 'finished move', data_url, sha256 })
  engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  expect(await ui.find({ type: 'Svg' })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /finished move: Open full review/ })).toBeDefined()
  expect(await ui.find({ key: 'animate' })).toBeUndefined()
  expect(await ui.find({ key: 'open-review' })).toBeDefined()
  await ui.unmount()
})

test('mobile without Input keeps the view usable and directs notes to supported presentations', async ($, on) => {
  const s = await fixture()
  engine(on, () => JSON.stringify(s), ['mobile'])
  await $.session.start({ cwd: '/project-a', surface: 'mobile', isInteractive: true } as any)
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('mobile') as any)
  expect(await ui.find({ key: 'note' })).toBeUndefined()
  expect(await ui.find({ key: 'request' })).toBeUndefined()
  expect(await ui.find({ type: 'Text', text: /cannot edit notes/ })).toBeDefined()
  expect(await ui.find({ key: 'open-review' })).toBeDefined()
  await ui.unmount()
})

test('empty onboarding composes a scoped guided draft without settings, payment or submission', async ($, on) => {
  const s = await fixture()
  s.run = null; s.images = []; s.manifest_sha256 = null; s.review_ready = false
  const h = engine(on, () => JSON.stringify(s))
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  expect(await ui.find({ type: 'Text', text: /Start a project/ })).toBeDefined()
  await ui.press({ key: 'guide' })
  const request = requestFromDraft(h.drafts[0].text)
  expect(h.drafts[0].text).toContain(s.labels.feedback_intro)
  expect(request.project).toBe('/project-b')
  expect(request.note).toBe(s.labels.guide_prompt)
  expect(h.writes.length).toBe(0)
  await ui.unmount()
})

test('native limit measures UTF-8 bytes rather than accepting multibyte text over 4 MiB', async () => {
  expect(() => parseSnapshot(' '.repeat(4 * 1024 * 1024 + 1))).toThrow('4 MiB')
  expect(() => parseSnapshot('あ'.repeat(1_400_000))).toThrow('4 MiB')
})

test('full review opener invokes only the bundled helper for the selected snapshot', async ($, on) => {
  const s = await fixture()
  const h = engine(on, () => JSON.stringify(s))
  const calls: any[] = []
  on('process.run', (_: any, e: any) => {
    calls.push(e)
    return { value: { exitCode: 0, stdout: '{"opened":true}', stderr: '' } }
  })
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  await ui.press({ key: 'open-review' })
  expect(calls.length).toBe(1)
  expect(calls[0].argv[0]).toBe('python3')
  expect(calls[0].argv[1]).toContain('/skills/pixellab-pip/assets/panel.py')
  expect(calls[0].argv.slice(2)).toEqual(['open', PATH])
  expect(h.toasts.join(' ')).toContain(s.labels.opened_review)
  expect(h.drafts.length).toBe(0)
  expect(h.writes.length).toBe(0)
  await ui.unmount()
})

test('opener reports missing Python and helper refusal without a second launch attempt', async ($, on) => {
  const s = await fixture()
  const h = engine(on, () => JSON.stringify(s))
  const calls: any[] = []
  on('process.run', (_: any, e: any) => {
    calls.push(e.argv)
    if (calls.length === 1) throw new Error('executable not found')
    return { value: { exitCode: 2, stdout: '', stderr: 'The selected HTML changed.' } }
  })
  await $.session.start({ cwd: '/project-a', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, snapshot_path: PATH })
  const ui = await $.ui.mount(pane('desktop') as any)
  await ui.press({ key: 'open-review' })
  expect(calls.map(argv => argv[0])).toEqual(['python3'])
  expect(h.toasts.join(' ')).toContain(s.labels.open_failed)
  await ui.press({ key: 'open-review' })
  expect(calls.length).toBe(2)
  expect(h.toasts.join(' ')).toContain(s.labels.open_failed)
  expect(h.drafts.length).toBe(0)
  await ui.unmount()
})
