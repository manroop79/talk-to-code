// components/FileUpload.tsx
"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";

type EmbedResult = { message: string; files: number; inserted: number; skipped: number };

type HistoryItem = {
projectId: string;
zipName: string;
at: number; // timestamp
summary?: EmbedResult; // optional stats
};

const HISTORY_KEY = "ttc_upload_history";

function loadHistory(): HistoryItem[] {
try {
const raw = localStorage.getItem(HISTORY_KEY);
if (!raw) return [];
const arr = JSON.parse(raw) as HistoryItem[];
return Array.isArray(arr) ? arr : [];
} catch {
return [];
}
}

function saveHistory(items: HistoryItem[]) {
localStorage.setItem(HISTORY_KEY, JSON.stringify(items));
}

function short(id: string, n = 8) {
return id.length > n ? id.slice(0, n) : id;
}

function niceDate(ts: number) {
try {
const d = new Date(ts);
return d.toLocaleString();
} catch {
return String(ts);
}
}

export default function FileUpload() {
const [dragOver, setDragOver] = useState(false);
const [busy, setBusy] = useState(false);
const [zipName, setZipName] = useState<string | null>(null);
const [projectId, setProjectId] = useState<string | null>(null);
const [embedSummary, setEmbedSummary] = useState<EmbedResult | null>(null);
const [history, setHistory] = useState<HistoryItem[]>([]);
const inputRef = useRef<HTMLInputElement>(null);

// hydrate from localStorage after mount
useEffect(() => {
try {
const id = localStorage.getItem("ttc_project_id");
if (id) setProjectId(id);
setHistory(loadHistory());
} catch {}
}, []);

const resetInput = () => {
if (inputRef.current) inputRef.current.value = "";
};

const startEmbed = async (pid: string) => {
    const res = await fetch("/api/embed", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ projectId: pid }),
    });
  
    const data = (await res.json()) as EmbedResult | { error: string };
  
    if (!res.ok) {
      // Type narrowing: check if data has 'error'
      if ("error" in data && typeof data.error === "string") {
        throw new Error(data.error);
      }
      throw new Error("Embedding failed");
    }
  
    setEmbedSummary(data as EmbedResult);
    return data as EmbedResult;
  };

const storeHistory = (item: HistoryItem) => {
const next = [item, ...history.filter((h) => h.projectId !== item.projectId)].slice(0, 20);
setHistory(next);
saveHistory(next);
};

const handleFiles = async (file: File) => {
if (!file) return;
if (!file.name.endsWith(".zip")) {
alert("Please upload a .zip file.");
return;
}

setBusy(true);
setZipName(file.name);
setEmbedSummary(null);

try {
// 1) Upload ZIP
const form = new FormData();
form.append("file", file);

const up = await fetch("/api/upload", { method: "POST", body: form });
const upData = (await up.json()) as { projectId?: string; error?: string };
if (!up.ok || !upData.projectId) throw new Error(upData.error || "Upload failed");

// 2) Persist project id
localStorage.setItem("ttc_project_id", upData.projectId);
setProjectId(upData.projectId);

// 3) Embed
const summary = await startEmbed(upData.projectId);

// 4) History
storeHistory({
projectId: upData.projectId,
zipName: file.name,
at: Date.now(),
summary,
});
} catch (e: unknown) {
    console.error("Upload/index error:", e);
    if (e instanceof Error) {
      alert(e.message);
    } else if (typeof e === "string") {
      alert(e);
    } else {
      alert("Something went wrong while uploading.");
    }
  } finally {
setBusy(false);
resetInput();
setDragOver(false);
}
};

const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
const f = e.target.files?.[0];
if (f) handleFiles(f);
};

const onDrop = useCallback((e: React.DragEvent) => {
e.preventDefault();
e.stopPropagation();
setDragOver(false);
const f = e.dataTransfer.files?.[0];
if (f) handleFiles(f);
}, []); // eslint-disable-line react-hooks/exhaustive-deps

const setActiveProject = (pid: string) => {
    localStorage.setItem("ttc_project_id", pid);
    setProjectId(pid);
};

const removeItem = (pid: string) => {
const next = history.filter((h) => h.projectId !== pid);
setHistory(next);
saveHistory(next);
if (projectId === pid) {
localStorage.removeItem("ttc_project_id");
setProjectId(null);
}
};

return (
<div className="w-full">
<div
onDragEnter={(e) => {
e.preventDefault();
setDragOver(true);
}}
onDragOver={(e) => e.preventDefault()}
onDragLeave={() => setDragOver(false)}
onDrop={onDrop}
className={[
"rounded-2xl border bg-white/5 backdrop-blur p-5",
"border-white/10 hover:border-white/20 transition",
dragOver ? "ring-2 ring-blue-500/50" : "",
].join(" ")}
>
<div className="flex items-start justify-between gap-2">
<div>
<h3 className="text-base font-semibold">Upload ZIP</h3>
<p className="text-xs text-white/60 mt-1">
Drag & drop your repository ZIP here, or choose a file.
</p>
</div>
<span className="text-[10px] px-2 py-1 rounded bg-white/10 text-white/70">
Project: {projectId ? short(projectId) : "—"}
</span>
</div>

<div className="mt-4 flex flex-wrap items-center gap-3">
<input
ref={inputRef}
type="file"
accept=".zip"
disabled={busy}
onChange={onFileChange}
className="hidden"
/>
<button
disabled={busy}
onClick={() => inputRef.current?.click()}
className="rounded-md px-4 py-2 text-sm font-medium bg-white text-black disabled:opacity-50 transition hover:brightness-95 cursor-pointer"
>
{busy ? "Working..." : "Choose file"}
</button>
{zipName && <span className="text-xs text-white/70 truncate">Selected: {zipName}</span>}
</div>

<div className="mt-4">
{busy ? (
<div className="text-xs text-white/70">
<div className="mb-2">Uploading & Indexing…</div>
<div className="h-2 w-full bg-white/10 rounded overflow-hidden">
<div className="h-2 w-1/3 animate-pulse bg-white/60 rounded" />
</div>
</div>
) : (
embedSummary && (
<div className="text-xs text-white/80 space-y-1">
<div className="font-medium text-white">Index complete</div>
<div>Files scanned: {embedSummary.files}</div>
<div>Chunks inserted: {embedSummary.inserted}</div>
<div>Duplicates skipped: {embedSummary.skipped}</div>
</div>
)
)}
</div>
</div>

{/* Upload history */}
<div className="mt-5">
<div className="mb-2 text-sm font-semibold">Recent uploads</div>
{history.length === 0 ? (
<div className="text-xs text-white/50">No uploads yet.</div>
) : (
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-3">
{history.map((h) => (
<div
key={h.projectId}
className="rounded-xl border border-white/10 bg-white/5 p-3"
>
<div className="flex items-center justify-between gap-2">
<div className="min-w-0">
<div className="text-xs font-medium truncate">{h.zipName}</div>
<div className="text-[10px] text-white/50">
ID: {short(h.projectId)} • {niceDate(h.at)}
</div>
</div>
<div className="flex gap-2">

<button
className="rounded-md px-2 py-1 text-[11px] bg-white text-black transition hover:brightness-95 cursor-pointer"
onClick={() => setActiveProject(h.projectId)}
>
  Use
</button>

<button
className="rounded-md px-2 py-1 text-[11px] bg-white/10 transition hover:bg-white/15 cursor-pointer"
onClick={() => removeItem(h.projectId)}
>
Remove
</button>
</div>
</div>

{h.summary && (
<div className="mt-2 flex flex-wrap gap-2">
<span className="text-[10px] rounded-full bg-white/10 px-2 py-1">
files: {h.summary.files}
</span>
<span className="text-[10px] rounded-full bg-white/10 px-2 py-1">
inserted: {h.summary.inserted}
</span>
<span className="text-[10px] rounded-full bg-white/10 px-2 py-1">
skipped: {h.summary.skipped}
</span>
</div>
)}
</div>
))}
</div>
)}
</div>
</div>
);
}