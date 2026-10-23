import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Move, Pose, Snapshot } from '../types'

const PANE = 'pga-panel'
const snap = atom({ plugin: 'pixellab-pip-studio', key: 'snap' } as const, null)
const note = atom({ plugin: 'pixellab-pip-studio', key: 'note' } as const, '')
const dirAtom = atom({ plugin: 'pixellab-pip-studio', key: 'dir' } as const, '')
const view = atom({ plugin: 'pixellab-pip-studio', key: 'view' } as const, 'project')
const newName = atom({ plugin: 'pixellab-pip-studio', key: 'newName' } as const, '')
const askAtom = atom({ plugin: 'pixellab-pip-studio', key: 'ask' } as const, '')
const activity = atom({ plugin: 'pixellab-pip-studio', key: 'activity' } as const, {
  step: '', since: 0, running: false, cost: 0, spent: 0, needsYou: '',
})
const levelAtom = atom({ plugin: 'pixellab-pip-studio', key: 'level' } as const, '')   // shown as chosen here; '' = not set yet

const COST = /(?:cost[":\s]*|estimated_generations[":\s]*)([\d.]+)/i   // a PixelLab result states what the call costs
const isPixelLab = (e: any) => /pixellab/i.test(e.tool) || (e.tool === 'Bash' && /fetch\.py/.test(JSON.stringify(e)))
const shortName = (e: any) => (e.tool === 'Bash' ? 'waiting for PixelLab' : String(e.tool).replace(/^mcp__[^_]+(?:_[^_]+)*?__/, ''))

const WELCOME = `# Welcome to PixelLab Pip Studio

Make pixel-art characters, their attacks and skills, effects, backgrounds and icons by describing them in plain
words. Claude picks the right [PixelLab](https://pixellab.ai) tool, writes the prompts, checks the art and hands you
game-ready sprite sheets.

## How a project goes

1. **Name a project** below. A folder is made for it.
2. **Choose your art style.** You always choose it: describe it in words, show art you like and Claude matches it,
   or pick a named example such as *Side-view dark fantasy* or *Top-down cozy*. Nothing is applied without asking.
3. **Describe a character**, for example *a hooded necromancer with a skull staff*. You get a few versions to pick from.
4. **Ask for a move**, for example *a whip attack* or *a jump and slash*. The two key poses (wind-up and hit) show up
   in this panel first. Press **Looks good: animate it**, or say what's wrong and press **Redo these poses**.
5. **Get the files.** Finished sheets, GIFs and a showcase appear here under *Finished moves*. Your raw PixelLab
   files are always kept; every clean-up is a labelled copy.

## What it costs, and when Claude asks

PixelLab counts **generations** from your monthly allowance: a character is about 6-18, a full attack about 30-50.
Claude always shows the plan and its cost first. Pick how often it asks:

| Level | What it means |
|---|---|
| **Ask** | approve every job before it spends |
| **Plan** (default here) | approve a whole plan once, with a budget and a few redos; it pauses only for you to check the key poses |
| **Auto** | runs on its own inside a budget you set |

Change it any time below, or with \`/pga-level\`. Deleting anything at PixelLab or overwriting files always asks.

## Before you start

- A [PixelLab](https://pixellab.ai) account; the plugin asked for your key when you installed it.
- Python 3 on your computer. **Check my setup** below tells you anything missing, in plain words.

## Handy commands

| Type this | What it does |
|---|---|
| \`/pga-start\` | a guided first project, explained step by step |
| \`/pga-char a red-haired archer\` | a new character |
| \`/pga-anim hero.png "overhead axe chop"\` | an attack or skill animation |
| \`/pga-fix\` | checks finished frames and fixes what it can for free |
| \`/pga-level plan 45 2\` | approve plans once, budget 45 generations, 2 redos |
| \`/pga-help\` | every command |
| \`/pga-panel <name>\` | opens this panel on a project, or starts a new one |
`

const SKIP = /(sheet|zoom|grid|cmp|flagged|[234]x)/i   // review sheets the skill writes next to the poses
const SVG_MAX = 120000                                  // the Svg element takes 131072 characters

const join = (a: string, b: string) => (a.endsWith('/') || a.endsWith('\\') ? a + b : a + '/' + b)

function pngSize(base64: string): [number, number] {
  const b = Uint8Array.fromBase64(base64.slice(0, 64))   // IHDR: width and height at bytes 16-23
  const be = (i: number) => (b[i] << 24) | (b[i + 1] << 16) | (b[i + 2] << 8) | b[i + 3]
  return [be(16), be(20)]
}

type Found = { keys: { dir: string; mtime: number }[]; manifests: string[]; finals: string[] }

async function walk($: any, dir: string, depth: number, found: Found) {
  let entries
  try {
    entries = await $.fs.list(dir)
  } catch {
    return
  }
  for (const e of entries) {
    const p = join(dir, e.name)
    if (e.kind === 'dir') {
      if (e.name === 'orig') continue
      if (e.name === 'keys') {
        const files = (await $.fs.list(p)).filter((f: any) => f.kind === 'file' && f.name.endsWith('.png'))
        let mtime = 0
        for (const f of files) mtime = Math.max(mtime, (await $.fs.stat(join(p, f.name))).mtimeMs)
        if (files.length) found.keys.push({ dir: p, mtime })
      }
      if (e.name === 'final') found.finals.push(p)
      if (depth > 0) await walk($, p, depth - 1, found)
    } else if (e.name === 'manifest.json') {
      found.manifests.push(p)
    }
  }
}

async function scan($: any, dir: string): Promise<Snapshot> {
  const empty: Snapshot = { dir, title: '', style: '', used: 0, keysFolder: '', poses: [], moves: [] }
  let cfg: any = {}
  const hasProfile = await $.fs.exists(join(dir, 'pixellab.json'))
  const out = join(dir, 'pixellab-pip-generations')   // Pip's run folders: <run>/keys, <run>/final, <run>/manifest.json
  if (!hasProfile && !(await $.fs.exists(out)))
    return { ...empty, error: `No project in ${dir} yet. /pga-panel <name> starts a new one; /pga-panel <folder> opens an existing one.` }
  try {
    if (hasProfile) cfg = JSON.parse(await $.fs.read(join(dir, 'pixellab.json')))
  } catch {}
  const styles = cfg.styles && typeof cfg.styles === 'object' ? cfg.styles : {}
  const style = cfg.active_style in styles ? cfg.active_style : ''   // never assumed: no chosen style shows as none
  const found: Found = { keys: [], manifests: [], finals: [] }
  await walk($, out, 3, found)

  let used = 0   // charged generations of finished jobs, from every run's manifest
  for (const m of found.manifests) {
    try {
      for (const j of JSON.parse(await $.fs.read(m)).jobs || [])
        if ((j.status || 'ok') === 'ok') used += Number(j.reported_usage?.generations) || 0
    } catch {}
  }

  const poses: Pose[] = []
  const add = async (path: string, name: string) => {
    try {
      const { base64 } = await $.fs.read(path, { as: 'bytes' })
      if (base64.length > SVG_MAX) return
      const [width, height] = pngSize(base64)
      poses.push({ path, name, base64, width, height })
    } catch {}
  }
  const anchor = styles[style]?.anchors?.heroes || styles[style]?.reference
  if (anchor) await add(join(dir, anchor), 'standing')
  const newest = found.keys.sort((a, b) => b.mtime - a.mtime)[0]
  if (newest) {
    const files = (await $.fs.list(newest.dir))
      .filter((f: any) => f.kind === 'file' && f.name.endsWith('.png') && !SKIP.test(f.name))
      .map((f: any) => f.name)
      .sort()
      .slice(0, 4)
    for (const f of files) await add(join(newest.dir, f), f.replace(/\.png$/, ''))
  }

  const moves: Move[] = []
  for (const fin of found.finals) {
    const names = (await $.fs.list(fin)).map((f: any) => f.name)
    for (const n of names) {
      if (!n.endsWith('.json')) continue
      const stem = n.slice(0, -5)
      if (stem.endsWith('_showcase')) continue
      moves.push({ name: stem, gif: names.includes(stem + '.gif') ? join(fin, stem + '.gif') : '', sheet: join(fin, stem + '.png') })
    }
    const show = names.find((n: string) => n.endsWith('_showcase.gif'))
    if (show) moves.push({ name: 'showcase', gif: join(fin, show), sheet: '' })
  }

  return { ...empty, title: cfg.game || dir.split(/[\\/]/).pop() || dir, style, used, keysFolder: newest?.dir || '', poses, moves }
}

const sig = (s: Snapshot | null) =>
  s ? JSON.stringify([s.dir, s.used, s.keysFolder, s.error, s.poses.map(p => p.path + p.base64.length), s.moves.map(m => m.name)]) : ''

async function refresh($: any) {
  const dir = await read($, dirAtom)
  if (!dir) return
  const next = await scan($, dir)
  const now = await read($, snap)
  if (sig(next) !== sig(now)) await update($, snap, () => next)
}

async function openFile($: any, path: string) {
  const win = /^[A-Za-z]:/.test(path)
  const argv = win ? ['explorer.exe', path.replace(/\//g, '\\')] : ['open', path]
  try {
    await $.process.run(argv)
  } catch {
    if (!win) await $.process.run(['xdg-open', path]).catch(() => $.ui.toast('Could not open ' + path))
  }
}

// Poses side by side in one picture at one pixel scale, so a pose on a padded canvas isn't drawn smaller than the
// standing sprite; no width/height, so the strip fills the pane and grows with it. Split where it would pass the
// Svg element's size limit.
function strips(poses: Pose[]): Pose[][] {
  const out: Pose[][] = []
  let cur: Pose[] = []
  let size = 0
  for (const p of poses) {
    if (cur.length && size + p.base64.length > SVG_MAX) {
      out.push(cur)
      cur = []
      size = 0
    }
    cur.push(p)
    size += p.base64.length
  }
  if (cur.length) out.push(cur)
  return out
}

function stripSvg(row: Pose[]) {
  const GAP = 8
  const total = row.reduce((w, p) => w + p.width + GAP, -GAP)
  const FS = Math.max(10, Math.round(total / 28))   // drawn ~13 px when the strip fills a ~360 px pane
  const LABEL = FS + 6
  const h = Math.max(...row.map(p => p.height))
  let x = 0
  let body = ''
  for (const p of row) {
    body +=
      `<image href="data:image/png;base64,${p.base64}" x="${x}" y="${h - p.height}" width="${p.width}" height="${p.height}" style="image-rendering:pixelated"/>` +
      `<text x="${x + p.width / 2}" y="${h + FS + 2}" text-anchor="middle" font-size="${FS}" font-family="sans-serif" fill="#8a8a8a">${p.name.replace(/[<>&]/g, "")}</text>`
    x += p.width + GAP
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${x - GAP} ${h + LABEL}">${body}</svg>`
}

async function showWelcome($: any) {
  await update($, view, () => 'welcome')
  await $.store.set('welcomed', true)
  await $.ui.open({ id: PANE, title: 'PixelLab art' })
}

// /pga-panel <arg>: an existing project opens; a new name or folder becomes a project Claude sets up
async function openProject($: any, rawArg: string): Promise<string> {
  const cwd = await $.session.cwd()
  const arg = rawArg.trim().replace(/^"(.*)"$/, '$1')
  if (!arg && !(await $.store.get('welcomed')) && !(await $.fs.exists(join(cwd, 'pixellab.json')))) {
    await showWelcome($)   // a first-time user with nothing open yet gets the welcome page
    return 'Welcome page opened in the PixelLab art panel.'
  }
  const dir = !arg ? cwd : /^([a-zA-Z]:|[\\/])/.test(arg) ? arg : join(cwd, arg)   // a bare name: a folder here
  await update($, dirAtom, () => dir)
  await update($, view, () => 'project')
  await $.store.set('dir', dir)
  await refresh($)
  await $.ui.open({ id: PANE, title: 'PixelLab art' })
  if (arg && !(await $.fs.exists(join(dir, 'pixellab.json')))) {
    // a new project: Claude makes the folder and runs the skill's setup there; the panel fills in as files appear.
    // Sent from a timer: a prompt submitted inside the command would wait on the turn the command holds.
    $.clock.after(0, () => void $.prompt.submit({
      text: `Start a new PixelLab project in ${dir} (create the folder if it doesn't exist and work there): ` +
        `help me choose an art style for it, set the approval level to plan with a budget of 50 generations and 2 redos ` +
        `(this edition's default; I can change it in the panel), then ask me what character or asset to make first.`,
      asUser: true,
    }).catch(() => $.ui.toast('Could not start the setup in the chat: type it there instead.')))
    return 'New project ' + dir + ': setting it up.'
  }
  return 'PixelLab panel opened for ' + dir
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'pga-panel', description: 'Open the PixelLab art panel for a project folder' })
    await $.command.register({ name: 'pga-setup', description: 'Welcome page: how PixelLab game art works and how to start' })
    const last = (await $.store.get('dir')) as string | undefined
    if (last && !(await read($, dirAtom))) await update($, dirAtom, () => last)
    $.clock.every(4000, () => void refresh($))
    return next(e)
  })

  on('command.run', { command: 'pga-panel' }, async ($, e) => ({ text: await openProject($, e.args) }))

  on('command.run', { command: 'pga-setup' }, async $ => {
    await showWelcome($)
    return { text: 'Welcome page opened in the PixelLab art panel.' }
  })

  // /pga-start (the skill's guided first project) also opens the welcome page beside it
  // the activity strip: every PixelLab call and wait the agent makes, with its cost
  on('tool.call', async ($, e, next) => {
    if (!isPixelLab(e)) return next(e)
    await update($, activity, a => ({ ...a, step: shortName(e), since: Date.now(), running: true, needsYou: '' }))
    const result = await next(e)
    const m = COST.exec(JSON.stringify(result ?? ''))
    const cost = m && e.tool !== 'Bash' ? Number(m[1]) : 0
    await update($, activity, a => ({ ...a, running: false, cost, spent: a.spent + cost }))
    return result
  })

  // "Needs you": the turn ended on a cost approval or a pose review
  on('turn.complete', async ($, e, next) => {
    const result: any = await next(e)
    if ((e as any).agentId) return result   // a subagent's turn: the main chat isn't waiting on the user
    const text = String((e as any).answer ?? '')
    const needsYou = /approve this pixellab run/i.test(text)
      ? 'Approve the plan in the chat: yes, no, or say what to change'
      : /key poses?/i.test(text) && /(approve|redo|look(s)? good|re-?roll)/i.test(text)
        ? 'Check the key poses below: animate them, or say what to fix'
        : ''
    await update($, activity, a => ({ ...a, running: false, needsYou }))
    return result
  })

  on('prompt.submit', async ($, e, next) => {
    if (/^\/pga-start\b/.test(e.text.trim()) && !/\b(off|on)\s*$/.test(e.text.trim()))
      showWelcome($).catch(() => undefined)   // the panel is a convenience: never hold up the prompt
    return next(e)
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button, Input, Svg, Markdown } = $.ui.resolve(e) as any
    const card = (key: string, children: any) => (
      <Box key={key} flexDirection="column" gap={1} borderStyle="round" borderDimColor padding={1}>
        {children}
      </Box>
    )
    const say = (text: string) =>
      void $.prompt.submit({ text, asUser: true }).catch(() => $.ui.toast('Could not send that to the chat: type it there instead.'))

    if ((await read($, view)) === 'welcome') {
      const go = async () => {
        const n = (await read($, newName)).trim()
        if (n) await openProject($, n)
      }
      const hasProject = !!(await read($, snap))?.title
      return (
        <Box flexDirection="column" gap={1}>
          {card(
            'start',
            <>
              <Text weight="medium" size="heading">Start here</Text>
              {Input && (
                <Input
                  key="newName"
                  label="Name your project"
                  placeholder="my-first-hero"
                  submitLabel="start"
                  onInput={(v: string) => void update($, newName, () => v)}
                  onSubmit={async (v: string) => {
                    await update($, newName, () => v)
                    await go()
                  }}
                />
              )}
              <Button key="start" variant="primary" label="Start project" onPress={() => void go()} />
              <Text dimColor size="footnote">First time? Let Claude walk you through it, or check that your computer is ready.</Text>
              <Box flexDirection="row" gap={1} flexWrap="wrap">
                <Button key="guided" variant="secondary" label="Guided first project" onPress={() => say('/pga-start')} />
                <Button
                  key="check"
                  variant="secondary"
                  label="Check my setup"
                  onPress={() =>
                    say('Check that PixelLab Pip is ready on this computer: PixelLab MCP connected (its setup reference), ' +
                      'Python 3 with Pillow, and numpy and scipy for the animation doctor. Tell me in plain words what, if ' +
                      'anything, I need to fix.')
                  }
                />
                {hasProject && <Button key="back" dimColor label="Back to my project" onPress={() => void update($, view, () => 'project')} />}
              </Box>
            </>,
          )}
          {Markdown ? <Markdown text={WELCOME} /> : <Text>{WELCOME}</Text>}
        </Box>
      )
    }

    const s = await read($, snap)
    if (!s) return <Text dimColor>Run /pga-panel in a project folder (one with pixellab.json).</Text>
    if (s.error)
      return (
        <Box flexDirection="column" gap={1}>
          <Text dimColor>{s.error}</Text>
          <Button key="help" variant="primary" label="Welcome and help" onPress={() => void update($, view, () => 'welcome')} />
        </Box>
      )
    const keyPoses = s.poses.filter(p => p.name !== 'standing')
    const names = keyPoses.map(p => p.name).join(', ')
    const folder = s.keysFolder
    const hasChar = s.poses.some(p => p.name === 'standing')
    const act = await read($, activity)
    const level = await read($, levelAtom)
    const step = !hasChar
      ? 'Step 1 of 3 · Describe your character below, then press Send.'
      : keyPoses.length && !s.moves.length
        ? 'Step 2 of 3 · Check the key poses below: animate them, or say what to fix.'
        : s.moves.length
          ? 'Step 3 of 3 · Done. Open your files below, or ask for another move.'
          : 'Step 2 of 3 · Ask for a move (an attack or a skill) below.'
    const ask = await read($, askAtom)
    const chips: [string, string][] = [
      ['New character', 'Make a new character: '],
      ['New attack', 'Make an attack animation for the standing sprite: '],
      ['New skill', 'Make a skill animation for the standing sprite: '],
    ]
    const redo = async () => {
      const n = (await read($, note)).trim()
      say(`Re-roll the key poses in ${folder} (${names}). ` +
        (n ? 'What is wrong: ' + n : 'Look at them at 3x next to the standing sprite and fix what fails the look checklist.'))
      await update($, note, () => '')
    }
    const send = async (v: string) => {
      if (v.trim()) say(v.trim())
      await update($, askAtom, () => '')
    }

    return (
      <Box flexDirection="column" gap={1}>
        <Box flexDirection="row" justifyContent="space-between">
          <Text weight="medium">{s.title}{s.style ? ' · ' + s.style : ''}</Text>
          <Text dimColor size="footnote">{s.used} gens used</Text>
        </Box>
        <Text color="cyan">{step}</Text>

        {act.needsYou ? <Text color="yellow" weight="medium">Needs you: {act.needsYou}</Text> : null}
        <Box flexDirection="row" justifyContent="space-between">
          <Text dimColor>
            {act.running
              ? `Running: ${act.step} · ${Math.max(0, Math.round((Date.now() - act.since) / 1000))} s`
              : act.step
                ? `Last: ${act.step}${act.cost ? ` · ${act.cost} gens` : ''}`
                : 'Nothing running'}
          </Text>
          <Text dimColor size="footnote">{act.spent} gens this session</Text>
        </Box>
        <Box flexDirection="row" gap={1} alignItems="center">
          <Text dimColor size="footnote">Approval: {level ? '' : 'not set (each job asks)'}</Text>
          {(['ask', 'plan', 'auto'] as const).map(l => (
            <Button
              key={'lvl-' + l}
              variant={level === l ? 'primary' : 'secondary'}
              label={l === 'ask' ? 'Ask each job' : l === 'plan' ? 'Plan (budget 50)' : 'Auto (budget 50)'}
              onPress={async () => {
                await update($, levelAtom, () => l)
                await $.store.set('level', l)
                say(l === 'ask'
                  ? 'Set my PixelLab approval level to ask: approve every job.'
                  : `Set my PixelLab approval level to ${l} with a budget of 50 generations and 2 redos.`)
              }}
            />
          ))}
        </Box>

        {card(
          'ask',
          <>
            <Text weight="medium">Ask for something</Text>
            <Box flexDirection="row" gap={1} flexWrap="wrap">
              {chips.map(([label, text]) => (
                <Button key={'chip' + label} variant="secondary" label={label} onPress={() => void update($, askAtom, () => text)} />
              ))}
            </Box>
            {Input && (
              <Input
                key="ask"
                value={ask}
                rows={2}
                placeholder="a hooded necromancer with a skull staff"
                submitLabel="send"
                onInput={(v: string) => void update($, askAtom, () => v)}
                onSubmit={(v: string) => void send(v)}
              />
            )}
          </>,
        )}

        {card(
          'poses',
          <>
            <Text weight="medium">Key poses</Text>
            {folder && <Text dimColor size="caption">{folder.split(/[\\/]/).slice(-2).join('/')}</Text>}
            {s.poses.length === 0 && <Text dimColor>Your character and its poses show up here.</Text>}
            {strips(s.poses).map((row, i) =>
              Svg ? (
                <Svg key={'strip' + i} source={stripSvg(row)} alt={row.map(p => p.name).join(', ')} />
              ) : (
                <Text key={'strip' + i}>{row.map(p => p.name).join(', ')}</Text>
              ),
            )}
            {keyPoses.length > 0 && (
              <>
                <Box marginTop={1}>
                  <Text dimColor size="footnote">Not right? Say what's wrong, then redo them:</Text>
                </Box>
                {Input && (
                  <Input
                    key="note"
                    placeholder="the whip should stay in the gloved hand"
                    submitLabel="redo"
                    onInput={(v: string) => void update($, note, () => v)}
                    onSubmit={async (v: string) => {
                      await update($, note, () => v)
                      await redo()
                    }}
                  />
                )}
                <Box flexDirection="row" gap={1} flexWrap="wrap">
                  <Button
                    key="approve"
                    variant="primary"
                    label="Looks good: animate it"
                    onPress={() => say(`Key poses approved (${names} in ${folder}). Go on with the animation.`)}
                  />
                  <Button key="reroll" variant="secondary" label="Redo these poses" onPress={() => void redo()} />
                </Box>
              </>
            )}
          </>,
        )}

        {card(
          'moves',
          <>
            <Text weight="medium">Finished moves</Text>
            {s.moves.length === 0 && <Text dimColor>Finished animations show up here.</Text>}
            {s.moves.map(m => (
              <Box key={m.name} flexDirection="row" justifyContent="space-between" alignItems="center">
                <Text>{m.name.replace(/^[^_]+_/, '')}</Text>
                <Box flexDirection="row" gap={1}>
                  {m.gif && <Button key={'gif' + m.name} variant="secondary" label="Play GIF" onPress={() => void openFile($, m.gif)} />}
                  {m.sheet && <Button key={'sheet' + m.name} variant="secondary" label="Sheet" onPress={() => void openFile($, m.sheet)} />}
                </Box>
              </Box>
            ))}
            {s.moves.length > 0 && (
              <Button
                key="folder"
                dimColor
                label="Open the folder"
                onPress={() => void openFile($, (s.moves[0].gif || s.moves[0].sheet).replace(/[\\/][^\\/]+$/, ''))}
              />
            )}
          </>,
        )}

        <Button key="help" dimColor label="Welcome and help" onPress={() => void update($, view, () => 'welcome')} />
      </Box>
    )
  })
}
