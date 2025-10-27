// app/api/embed/route.ts
import { NextRequest, NextResponse } from "next/server";
import { promises as fs } from "node:fs";
import path from "node:path";
import { getFilesRecursively } from "@/lib/server/getFilesRecursively";
import { embedFileToProject, supabase } from "@/lib/supabase";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ALLOWED = [
    ".js",".ts",".jsx",".tsx",".json",".md",".mdx",".yml",".yaml",".toml",
    ".py",".rs",".go",".java",".kt",".rb",".php",".sh",".css",".scss",".html",
    ".c",".h",".cpp"
];

function shouldIndex(file: string) {
const ext = path.extname(file).toLowerCase();
return ALLOWED.includes(ext);
}

export async function POST(req: NextRequest) {
    try {
        const { projectId, projectName } = await req.json();
        if (!projectId) {
            return NextResponse.json({ error: "Missing projectId" }, { status: 400 });
        }

    // 1) Ensure a row exists in projects (insert-if-missing)
    const { data: existing, error: selErr } = await supabase
    .from("projects")
    .select("id")
    .eq("id", projectId)
    .maybeSingle();

    if (selErr) {
        console.error("Supabase select(projects) error:", selErr);
        return NextResponse.json({ error: `DB read failed: ${selErr.message}` }, { status: 500 });
    }

    if (!existing) {
        const { error: insErr } = await supabase
        .from("projects")
        .insert({ id: projectId, name: projectName ?? `Project ${new Date().toISOString()}` });

    // Ignore duplicate-key races; otherwise surface the error
    if (insErr && insErr.code !== "23505") {
        console.error("Supabase insert(projects) error:", insErr);
        return NextResponse.json({ error: `DB insert failed: ${insErr.message}` }, { status: 500 });
    }
    }

    // 2) Walk extracted files under uploaded/<projectId> and embed allowed ones
    // Use /tmp on Vercel, uploaded/ locally
    const isVercel = process.env.VERCEL === "1";
    const uploadBase = isVercel ? "/tmp" : path.join(process.cwd(), "uploaded");
    const base = path.join(uploadBase, projectId);
    const allFiles = await getFilesRecursively(base);
    const files = allFiles.filter(shouldIndex);

    let inserted = 0;
    let skipped = 0;

    for (const file of files) {
        const content = await fs.readFile(file, "utf-8");
        const filename = path.basename(file);
        const res = await embedFileToProject(projectId, file, filename, content);
        inserted += res.inserted;
        skipped += res.skipped;
    }

    return NextResponse.json({
        message: "Embedding complete",
        files: files.length,
        inserted,
        skipped,
    });
    } catch (e: unknown) {
    console.error("/api/embed error:", e);
    let message = "Embedding Failed: unknown";
    if (e instanceof Error) {
        message = `Embedding Failed ${e.message}`;
    }
    return NextResponse.json(
    { error: message },
    { status: 500 }
    );
    }
}