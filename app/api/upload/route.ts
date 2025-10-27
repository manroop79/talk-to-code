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

    // 5) Return projectId for the client to use
    return NextResponse.json({ projectId, folder: root });
    } catch (e: unknown) {
        console.error("/api/upload error:", e);
        return NextResponse.json({ error: "Upload failed" }, { status: 500 });
    }
}