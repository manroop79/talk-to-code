// app/api/upload/route.ts
import { NextRequest, NextResponse } from "next/server";
import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import AdmZip from "adm-zip";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
    try {
        const form = await req.formData();
        const file = form.get("file") as File | null;
        if (!file) {
            return NextResponse.json({ error: "No file provided. Use form field 'file'." }, { status: 400 });
        }

        // Check file size limit (Vercel has 4.5MB body size limit on Hobby plan)
        const maxSize = 50 * 1024 * 1024; // 50MB for local, but Vercel may have lower limits
        if (file.size > maxSize) {
            return NextResponse.json({ 
                error: `File too large. Maximum size is ${maxSize / 1024 / 1024}MB` 
            }, { status: 413 });
        }

    // 1) Make a new local projectId (don't depend on DB here)
    const projectId = crypto.randomUUID();

    // 2) Ensure target folder - use /tmp for Vercel compatibility
    // On Vercel, only /tmp is writable (ephemeral storage)
    const isVercel = process.env.VERCEL === "1";
    const uploadBase = isVercel ? "/tmp" : path.join(process.cwd(), "uploaded");
    const root = path.join(uploadBase, projectId);
    await mkdir(root, { recursive: true });

    // 3) Save the uploaded zip
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    const zipPath = path.join(root, "upload.zip");
    await writeFile(zipPath, buffer);

    // 4) Extract
    try {
        const zip = new AdmZip(zipPath);
        zip.extractAllTo(root, true);
        } catch (e) {
        console.error("ZIP extract error:", e);
        return NextResponse.json({ error: "Invalid ZIP or extract failed." }, { status: 400 });
    }

    // 5) On Vercel, immediately process the files since /tmp is ephemeral
    // Files won't persist across function invocations
    if (isVercel) {
        try {
            // Import and call embedding logic directly
            const { promises: fs } = await import("node:fs");
            const { getFilesRecursively } = await import("@/lib/server/getFilesRecursively");
            const { embedFileToProject, supabase } = await import("@/lib/supabase");
            
            const ALLOWED = [
                ".js",".ts",".jsx",".tsx",".json",".md",".mdx",".yml",".yaml",".toml",
                ".py",".rs",".go",".java",".kt",".rb",".php",".sh",".css",".scss",".html",
                ".c",".h",".cpp"
            ];
            
            function shouldIndex(file: string) {
                const ext = path.extname(file).toLowerCase();
                return ALLOWED.includes(ext);
            }
            
            // Ensure project exists in DB
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
                    .insert({ id: projectId, name: `Project ${new Date().toISOString()}` });

                if (insErr && insErr.code !== "23505") {
                    console.error("Supabase insert(projects) error:", insErr);
                    return NextResponse.json({ error: `DB insert failed: ${insErr.message}` }, { status: 500 });
                }
            }
            
            // Process files
            const allFiles = await getFilesRecursively(root);
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
                projectId, 
                folder: root,
                embedded: true,
                files: files.length,
                inserted,
                skipped
            });
        } catch (embedError: unknown) {
            console.error("Embedding error on Vercel:", embedError);
            return NextResponse.json({ 
                error: "Upload succeeded but embedding failed: " + (embedError instanceof Error ? embedError.message : "Unknown error"),
                projectId 
            }, { status: 500 });
        }
    }

    // 6) For local development, return projectId for separate embed call
    return NextResponse.json({ projectId, folder: root });
    } catch (e: unknown) {
        console.error("/api/upload error:", e);
        return NextResponse.json({ error: "Upload failed" }, { status: 500 });
    }
}