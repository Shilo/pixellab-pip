export type PanelImage = {
  role: string;
  path: string;
  sha256: string;
  data_url: string;
  width: number;
  height: number;
};

export type PanelSnapshot = {
  version: 1;
  project: string;
  run: string | null;
  created_at: string;
  style: string;
  usage: { charged: number | null; committed: number | null };
  jobs: { job_id: string; tool?: string; status?: string; outcome?: string }[];
  images: PanelImage[];
  warnings: string[];
  manifest_sha256: string | null;
  labels: Record<string, string>;
  review_ready: boolean;
};
