"use client";

import { useEffect, useRef, useState } from "react";
import ChatPanel, { Message, Source } from "@/components/ChatPanel";
import FileUpload from "@/components/FileUpload";

type ApiResponse = { answer?: string; error?: string; sources?: Source[] };

export default function WorkspacePage() {
const [messages, setMessages] = useState<Message[]>([]);
const [input, setInput] = useState("");
const [sending, setSending] = useState(false);
const inputRef = useRef<HTMLTextAreaElement>(null);

// Cmd/Ctrl + K focuses the composer
useEffect(() => {
  const onKey = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    inputRef.current?.focus();
  }
};
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}, []);

const sendQuestion = async () => {
  const trimmed = input.trim();
  if (!trimmed || sending) return;

  const projectId = typeof window !== "undefined" ? localStorage.getItem("ttc_project_id") : null;
  if (!projectId) {
    alert("No project selected. Upload a ZIP first.");
    return;
  }

  setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
  setInput("");
  setSending(true);

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: trimmed, projectId }),
  });

  let data: ApiResponse = {};
  try {
    data = await res.json();
  } catch {}

  const answer =
  data?.answer ??
  data?.error ??
  (res.ok ? "No answer." : "Server error. Please try again.");

  setMessages((prev) => [
    ...prev,
    { role: "assistant", content: answer, sources: data.sources },
    ]);
    } catch {
    setMessages((prev) => [
    ...prev,
    { role: "assistant", content: "Request failed. Check console and try again." },
    ]);
    } finally {
    setSending(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-black text-white">
      <div className="mx-auto max-w-7xl px-4 py-4 lg:py-6">
      {/* Desktop: sidebar + chat; Mobile: stacked */}
        <div className="grid lg:grid-cols-[340px_1fr] gap-0 lg:gap-6 min-h-[calc(100vh-4rem)]">
          <aside className="space-y-4 border-b lg:border-b-0 lg:border-r border-gray-300 dark:border-gray-600">

            <div className="text-xl font-semibold text-center mb-4">Workspace</div>
            <div className="p-4 lg:pr-6 lg:pl-0 lg:pb-0 lg:pt-0">
              <FileUpload />
            </div>
       
          </aside>

          <main className="min-h-[60vh] flex flex-col lg:pl-8">
            <ChatPanel
              className="h-full"
              messages={messages}
              input={input}
              setInput={setInput}
              onSend={sendQuestion}
              sending={sending}
              inputRef={inputRef}
            />
    </main>
      </div>
      </div>
    </div>
  );
}