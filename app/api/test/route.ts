import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
    try {
        const { data, error } = await supabase.from("documents").select("*").limit(1);
        if (error) {
            console.error("Test fetch error:", error);
            return NextResponse.json({ error: error.message }, { status: 500 });
        }

        return NextResponse.json({ data });
    } catch (err) {
        console.error("Test route error:", err);
        return NextResponse.json({ error: "Internal server error" }, { status: 500 });
    }
}