// lib/supabase.ts
import { createClient } from "@supabase/supabase-js";
import OpenAI from "openai";
import crypto from "node:crypto";

export const supabase = createClient(
process.env.SUPABASE_URL!,
process.env.SUPABASE_ANON_KEY!
);

// One shared OpenAI client
export const openai = new OpenAI({
apiKey: process.env.OPENAI_API_KEY!,
timeout: 10000,
});

const EMBEDDING_MODEL = "text-embedding-3-small";

// naive char-based chunking (tunable)
function chunkText(input: string, size = 2000, overlap = 200) {
const chunks: string[] = [];
for (let i = 0; i < input.length; i += size - overlap) {
chunks.push(input.slice(i, i + size));
}
return chunks;
}

function sha256(text: string) {
return crypto.createHash("sha256").update(text).digest("hex");
}

// Batch embed (OpenAI supports array input)
async function embedBatch(texts: string[]) {
const resp = await openai.embeddings.create({
model: EMBEDDING_MODEL,
input: texts,
});
return resp.data.map((d) => d.embedding);
}

// Embed a file into many chunks; skip duplicates by sha256
export async function embedFileToProject(
projectId: string,
absPath: string,
filename: string,
content: string
) {
const chunks = chunkText(content);
if (chunks.length === 0) return { inserted: 0, skipped: 0 };

// precompute hashes and detect existing
const hashRows = chunks.map((c) => ({ hash: sha256(c), content: c }));
const { data: existing, error: exErr } = await supabase
.from("documents")
.select("sha256")
.in("sha256", hashRows.map((h) => h.hash))
.eq("project_id", projectId);

if (exErr) throw new Error("Supabase read error: " + exErr.message);
const existingSet = new Set((existing || []).map((r) => r.sha256));

const toInsert = hashRows.filter((h) => !existingSet.has(h.hash));
if (toInsert.length === 0) return { inserted: 0, skipped: chunks.length };

// batch in groups to respect token/size constraints
const BATCH = 32;
let inserted = 0;

for (let i = 0; i < toInsert.length; i += BATCH) {
const slice = toInsert.slice(i, i + BATCH);
const embeddings = await embedBatch(slice.map((s) => s.content));

const rows = slice.map((s, idx) => ({
project_id: projectId,
path: absPath,
filename,
sha256: s.hash,
content: s.content,
embedding: embeddings[idx],
}));

const { error } = await supabase.from("documents").insert(rows);
if (error) throw new Error("Supabase insert error: " + error.message);
inserted += rows.length;
}

return { inserted, skipped: chunks.length - inserted };
}

// Query top-N chunks for a project
export async function searchRelevantChunks(
projectId: string,
query: string,
matchCount = 6,
threshold = 0.85
) {
const embedding = await openai.embeddings.create({
model: EMBEDDING_MODEL,
input: query,
});

const { data, error } = await supabase.rpc("match_documents", {
project: projectId,
query_embedding: embedding.data[0].embedding,
match_count: matchCount,
match_threshold: threshold,
});

if (error) throw new Error("Supabase search error: " + error.message);
return data as { id: string; path: string; filename: string; content: string; similarity: number }[];
}