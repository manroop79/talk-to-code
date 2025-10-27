"use client";

import React, { useEffect, useRef, useState } from "react";
import Button from "@/components/ui/Button";

export type Source = { id: string; filename: string; similarity?: number };
export type Message = { role: "user" | "assistant"; content: string; sources?: Source[] };

interface Props {
messages: Message[];
input: string;
setInput: (v: string) => void;
onSend: () => void;
sending?: boolean;
inputRef?: React.Ref<HTMLTextAreaElement>;
className?: string;
}

const starters = [
"List all endpoints and their handlers",
"Explain the main.cpp file",
"Where are environment variables read?",
"Show all React hooks used in the project",
];

export default function ChatPanel({
messages,
input,
setInput,
onSend,
sending,
inputRef,
className,
}: Props) {
const endRef = useRef<HTMLDivElement>(null);
const scrollParent = useRef<HTMLDivElement>(null);
const [showJump, setShowJump] = useState(false);

// Auto-scroll to bottom on new messages
useEffect(() => {
endRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages]);

// Show a floating "scroll to latest" when user scrolled up
useEffect(() => {
const el = scrollParent.current;
if (!el) return;
const onScroll = () => {
const nearBottom = el.scrollTop >= el.scrollHeight - el.clientHeight - 200;
setShowJump(!nearBottom);
};
el.addEventListener("scroll", onScroll);
onScroll();
return () => el.removeEventListener("scroll", onScroll);
}, []);

const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
if (e.key === "Enter" && !e.shiftKey) {
e.preventDefault();
onSend();
}
};

const addStarter = (s: string) => setInput(s);

return (
<div className={`relative flex w-full flex-col min-h-[70vh] md:min-h-[65vh] lg:min-h-[70vh] ${className ?? ""}`}>
{/* Subtle grid background */}
<div className="absolute inset-0 -z-10 bg-[linear-gradient(to_right,rgba(255,255,255,0.08)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.08)_1px,transparent_1px)] bg-[size:32px_32px]" />
<div className="pointer-events-none absolute inset-0 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]" />

{/* Messages */}
<div ref={scrollParent} className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 pb-28 md:pb-0">
{messages.length === 0 ? (
<div className="pt-12 text-center space-y-4">
<div className="text-white/60">Ask anything about your codebase…</div>
<div className="flex flex-wrap justify-center gap-2">
{starters.map((s) => (
<button
key={s}
onClick={() => addStarter(s)}
className="text-xs px-3 py-1.5 rounded-full bg-white/10 hover:bg-white/15 cursor-pointer"
>
{s}
</button>
))}
</div>
</div>
) : (
messages.map((m, i) => (
<div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
<div
className={`max-w-[92%] md:max-w-[75%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm leading-relaxed ${
m.role === "user"
? "bg-white text-black shadow"
: "bg-white/5 text-white border border-white/10 backdrop-blur"
}`}
>
{m.content}

{/* Citations */}
{m.role === "assistant" && m.sources && m.sources.length > 0 && (
<div className="mt-3 flex flex-wrap gap-2">
{m.sources.map((s, idx) => (
<span
key={`${s.id}-${idx}`}
className="text-[10px] rounded-full bg-white/10 px-2 py-1 text-white/80 border border-white/10
cursor-pointer hover:bg-white/15 active:bg-white/20"
title={s.filename}
>
{s.filename}{" "}
{typeof s.similarity === "number" ? `(${s.similarity.toFixed(2)})` : ""}
</span>
))}
</div>
)}
</div>
</div>
))
)}

{/* Loading indicator */}
{sending && (
<div className="flex justify-start">
<div className="rounded-2xl px-4 py-3 bg-white/5 border border-white/10 backdrop-blur">
<div className="flex space-x-1.5">
<div className="h-2.5 w-2.5 animate-bounce rounded-full bg-white/70" style={{ animationDelay: "0ms" }} />
<div className="h-2.5 w-2.5 animate-bounce rounded-full bg-white/70" style={{ animationDelay: "150ms" }} />
<div className="h-2.5 w-2.5 animate-bounce rounded-full bg-white/70" style={{ animationDelay: "300ms" }} />
</div>
</div>
</div>
)}

<div ref={endRef} />
</div>

{/* Scroll to latest */}
{showJump && (
<button
onClick={() => endRef.current?.scrollIntoView({ behavior: "smooth" })}
className="absolute right-4 bottom-24 z-10 bg-white text-black text-xs px-3 py-1.5 rounded-full shadow cursor-pointer"
aria-label="Jump to latest"
>
↓ New
</button>
)}

{/* Composer */}
<div className="border-t border-white/10 bg-black/60 backdrop-blur px-4 py-3 fixed bottom-0 left-0 right-0 z-20 md:static">
<div className="mx-auto flex max-w-4xl items-end gap-2">
<textarea
ref={inputRef}
value={input}
onChange={(e) => setInput(e.target.value)}
onKeyDown={handleKeyDown}
placeholder="Ask a question…"
className="min-h-[48px] max-h-40 flex-1 resize-none rounded-xl bg-white/5 px-4 py-3 text-sm text-white placeholder:text-white/40 outline-none border border-white/10 focus:border-white/30"
/>
<Button
onClick={onSend}
disabled={sending || !input.trim()}
variant={input.trim() ? "success" : "secondary"}
aria-label="Send message"
>
{sending ? "Sending…" : "Send"}
</Button>
</div>
<div className="mx-auto mt-1 max-w-4xl text-[10px] text-white/40">
Press <kbd className="rounded bg-white/10 px-1">Enter</kbd> to send •{" "}
<kbd className="rounded bg-white/10 px-1">Shift</kbd>+<kbd className="rounded bg-white/10 px-1">Enter</kbd> for a new line
</div>
</div>
</div>
);
}