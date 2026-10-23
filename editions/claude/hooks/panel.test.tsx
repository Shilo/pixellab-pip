import { expect, test } from 'claude-code/testing'

// A small in-memory project the panel reads through $.fs.
const FILES: Record<string, string> = {
  '/proj/pixellab.json': JSON.stringify({ styles: { neon: { look: 'neon on black' } }, active_style: 'neon' }),
  '/proj/pixellab-pip-generations/run1/manifest.json': JSON.stringify({ jobs: [
    { job_id: 'a', status: 'ok', reported_usage: { generations: 6 } },
    { job_id: 'b', status: 'failed', reported_usage: { generations: 9 } },
    { job_id: 'c', status: 'ok', reported_usage: { generations: 4.5 } },
  ] }),
}
const DIRS: Record<string, string[]> = {
  '/proj/pixellab-pip-generations': ['run1/'],
  '/proj/pixellab-pip-generations/run1': ['manifest.json'],
}

const PANE = {
  plugin: 'pixellab-pip-studio',
  component: 'Pane',
  requestId: 'pga-panel',
  props: { title: 'PixelLab art', isFocused: false, bodyColumns: 60, placement: 'dock', scroll: { offset: 0, bodyRows: 40 }, view: {} },
} as const

// the engine resolves paths against the session's drive: compare in one form
const norm = (p: string) => p.replace(/^[A-Za-z]:/, '').split('\\').join('/')

function engine(on: any, submitted: string[] = []) {
  const store: Record<string, unknown> = {}
  on('command.register', () => ({ value: undefined }))
  on('store.get', (_: any, e: any) => ({ value: store[e.key] }))
  on('store.set', (_: any, e: any) => {
    store[e.key] = e.value
    return { value: undefined }
  })
  on('clock.every', () => ({ value: null }))
  on('clock.after', () => ({ value: null }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_: any, e: any) => ({ cwd: e.cwd }))
  on('session.cwd', () => ({ value: '/proj' }))
  on('fs.exists', (_: any, e: any) => ({ value: norm(e.path) in FILES || norm(e.path) in DIRS }))
  on('fs.read', (_: any, e: any) => (norm(e.path) in FILES ? { value: FILES[norm(e.path)] } : { error: 'missing' }))
  on('fs.list', (_: any, e: any) => ({
    value: (DIRS[norm(e.path)] || []).map(n => ({ name: n.replace(/\/$/, ''), kind: n.endsWith('/') ? 'dir' : 'file' })),
  }))
  on('fs.stat', () => ({ value: { mtimeMs: 1 } }))
  on('prompt.submit', (_: any, e: any) => {
    submitted.push(e.text)
    return { text: e.text }
  })
  on('tool.call', () => ({ result: { text: 'cost: 4 generations' } }))
}

test('spend comes from the run manifests, failed jobs refunded', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  await $.command.run({ command: 'pga-panel', args: '/proj' } as any)
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect((await ui.find({ type: 'Text', text: /gens used/ }))?.text).toContain('10.5 gens used')
  expect((await ui.find({ type: 'Text', text: /neon/ }))?.text).toContain('neon')
  await ui.unmount()
})

test('welcome page names the style choice and the approval levels', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  await $.command.run({ command: 'pga-setup', args: '' } as any)
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  const md = await ui.find({ type: 'Markdown' })
  expect(md?.text).toMatch(/choose|style/i)
  expect(md?.text).toMatch(/Ask.*Plan.*Auto/s)
  await ui.unmount()
})

test('a PixelLab call shows in the activity strip with its cost', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  await $.command.run({ command: 'pga-panel', args: '/proj' } as any)
  await $.tool.call({ tool: 'mcp__pixellab__animate_image', action: 'swing' } as any)
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  const strip = await ui.find({ type: 'Text', text: /animate_image/ })
  expect(strip?.text).toContain('animate_image')
  expect((await ui.find({ type: 'Text', text: /this session/ }))?.text).toContain('4')
  await ui.unmount()
})

test('a new name starts a project, quoted names with spaces kept whole', async ($, on) => {
  const submitted: string[] = []
  engine(on, submitted)
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  const r: any = await $.command.run({ command: 'pga-panel', args: '"my game"' } as any)
  expect(r.text).toMatch(/New project .*my game/)      // the setup request itself is queued to the chat
})

test('needs you appears when the turn ends on a cost approval', async ($, on) => {
  engine(on)
  on('turn.complete', () => ({ text: '' }))
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  await $.command.run({ command: 'pga-panel', args: '/proj' } as any)
  await $.turn.complete({ reason: 'answer', answer: '💳 **Approve this PixelLab run?** — ~12 generations',
    durationMs: 5, isAborted: false, turnId: 't1' } as any)
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect((await ui.find({ type: 'Text', text: /Needs you/ }))?.text).toMatch(/Approve the plan/)
  await ui.unmount()
})

test('check my setup asks for the Pip setup check', async ($, on) => {
  const submitted: string[] = []
  engine(on, submitted)
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  await $.command.run({ command: 'pga-setup', args: '' } as any)
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  await ui.press({ key: 'check' } as any)
  expect(submitted.join(' ')).toMatch(/PixelLab Pip/)
  expect(submitted.join(' ')).not.toMatch(/check_setup\.py|pixellab-game-art/)
  await ui.unmount()
})

test('the approval level shows as not set until one is chosen', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/proj', surface: 'desktop', isInteractive: true })
  await $.command.run({ command: 'pga-panel', args: '/proj' } as any)
  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect((await ui.find({ type: 'Text', text: /Approval/ }))?.text).toMatch(/not set/)
  await ui.unmount()
})
