import { NextRequest, NextResponse } from "next/server";
import { searchRelevantChunks, openai } from "@/lib/supabase";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const CHAT_MODEL = process.env.OPENAI_CHAT_MODEL || "gpt-3.5-turbo";

export async function POST(req: NextRequest) {
    try {
        const body = await req.json().catch(() => ({} as { question?: string; projectId: string; }));

        const question = typeof body.question === "string" ? body.question.trim() : "";
        const projectId = typeof body.projectId === "string" ? body.projectId : "";

        if (!question) {
            return NextResponse.json({ error: "Missing question" }, { status: 400 });
        }
        if (!projectId) {
            return NextResponse.json({ error: "Missing projectId" }, { status: 400 });
        }

// 1) Retrieve top-N chunks for this project
    let chunks: Array<{ id: string; filename: string; content: string; similarity: number }> = [];
        try {
            chunks = await searchRelevantChunks(projectId, question, 6, 0.90);
        } catch (err: unknown) {
            let msg = "Search Error";
            if (err instanceof Error) {
                console.error("Supabase search error:", err?.message || err);
                msg = err.message;
            }
            return NextResponse.json({ error: "Search failed" }, { status: 502 });
        }

// Build short source list for the UI
    const sources = (chunks || []).map((c) => ({
        id: c.id,
        filename: c.filename,
        similarity: c.similarity,
    }));

// 2) Construct prompt
    const contextText =
    chunks.length > 0
    ? chunks.map((c, i) => `Source ${i + 1}: ${c.filename}\n${c.content}`).join("\n\n")
    : "(no retrieved context)";

    const system =
        "You are a precise coding assistant. Prefer using the provided project sources. If unsure, say so. Keep answers concise and cite file names when helpful.";
    const user = `Use the following project context to answer the question.\n\nContext:\n${contextText}\n\nQuestion: ${question}\n\nAnswer clearly.`;

// 3) Ask OpenAI
    let completion;
        try {
            completion = await openai.chat.completions.create({
                model: CHAT_MODEL,
                temperature: 0.2,
                messages: [
                { role: "system", content: system },
                { role: "user", content: user },
                ],
            });
        } catch (err: unknown) {
            let msg = "OpenAI request failed";
            if (err instanceof Error) {
                console.error("OpenAI chat error:", err.message);
                msg = err.message;
            } else {
                console.error("OpenAI chat error:", err);
            }
            return NextResponse.json({ error: msg }, { status: 502 });
        }

    const answer = completion.choices[0]?.message?.content ?? "No answer.";

    return NextResponse.json({ answer, sources });
    } catch (e: unknown) {
        let msg = "Internal Server Error";
        if (e instanceof Error) {
            console.error("/api/ask fatal:", e.message);
            msg = e.message;
        } else {
            console.error("/api/ask fatal:", e);
        }
        return NextResponse.json({ error: msg }, { status: 500 });
    }
}