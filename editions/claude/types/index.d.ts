export type Pose = { path: string; name: string; base64: string; width: number; height: number }
export type Move = { name: string; gif: string; sheet: string }
export type Snapshot = {
  dir: string
  title: string
  style: string
  used: number
  keysFolder: string
  poses: Pose[]
  moves: Move[]
  error?: string
}

declare module 'claude-code' {
  interface PluginState {
    'pixellab-pip-studio': { snap: Snapshot | null; note: string; dir: string; view: 'welcome' | 'project'; newName: string; ask: string
      activity: { step: string; since: number; running: boolean; cost: number; spent: number; needsYou: string }
      level: '' | 'ask' | 'plan' | 'auto' }
  }
}
