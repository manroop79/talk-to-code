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

    // 1) Make a new local projectId (don’t depend on DB here)
    const projectId = crypto.randomUUID();

    // 2) Ensure target folder
    const root = path.join(process.cwd(), "uploaded", projectId);
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