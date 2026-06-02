const BASE = "/api";

export async function uploadBOM(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/boms/upload`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function listBOMs() {
  const res = await fetch(`${BASE}/boms/`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getBOM(id: string) {
  const res = await fetch(`${BASE}/boms/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getRiskSummary(bomId: string) {
  const res = await fetch(`${BASE}/reports/${bomId}/risk-summary`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function screenEntity(name: string) {
  const res = await fetch(`${BASE}/compliance/screen?name=${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
