# EchoCode — Talk to Your Codebase

> Upload your codebase as a ZIP file and ask questions in plain English—EchoCode indexes your project with embeddings stored in **your** Supabase instance, then answers with clear, source-linked replies. Built with **Next.js 15, TypeScript, Tailwind CSS, Framer Motion, Supabase (pgvector),** and **OpenAI**.

![Next.js](https://img.shields.io/badge/Next.js-15-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Tailwind](https://img.shields.io/badge/TailwindCSS-3-38B2AC)
![Framer Motion](https://img.shields.io/badge/Framer%20Motion-animations-ff55cc)
![Supabase](https://img.shields.io/badge/Supabase-pgvector-3FCF8E)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991)

---

## Table of Contents

- [Overview](#overview)
- [Screenshots](#screenshots)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Core Flows](#core-flows)
- [API Reference](#api-reference)
- [Accessibility & Performance](#accessibility--performance)
- [Testing](#testing)
- [Security Notes](#security-notes)
- [Contributing](#contributing)

---

## Overview

**EchoCode** (also known as *TalkToCode*) lets you upload a ZIP of your project and interact with it:  
Ask questions like “What does `main.cpp` do?” or “Where do we validate login?”  
EchoCode extracts and embeds your files, stores embeddings as vectors in Supabase, and uses a lightweight RAG pipeline to deliver fast, readable, source-linked answers. The UI is responsive, minimal, and keyboard-friendly.

---

## Screenshots

> Replace these with your own project images in `public/readme/`.

![Landing](./public/readme/landing.png)
![Workspace](./public/readme/workspace.png)
![Features + Pricing](./public/readme/features-pricing.png)

---

## Features

- 📦 **Upload & Index:** Drag-and-drop ZIP file; chunk and embed files into `pgvector`.
- 💬 **Ask Anything:** Natural language Q&A over your codebase.
- 🔗 **Citations:** Clickable sources back to files/lines.
- ⚡ **Streaming Replies:** Markdown answers, code highlighting, fast response.
- 🗂️ **Multiple Projects:** Switch between uploads; recent history.
- 🧩 **Clean UI:** Hero/Features/Pricing landing; modern workspace.
- 🧠 **Model Options:** Default GPT-3.5; simply swap to 4o-mini/others.
- 🧹 **Your Data Stays Yours:** Vectors live in your Supabase.

---

## Tech Stack

- **Frontend:** Next.js 15 (App Router), React 18, TypeScript, Tailwind CSS, Framer Motion, Tabler Icons
- **Backend:** Next.js Route Handlers (`/app/api/*`)
- **Data:** Supabase Postgres + **pgvector** (`vector(1536)`)
- **AI:** OpenAI Embeddings (`text-embedding-3-small`), Chat (`gpt-3.5-turbo` default)

---

## System Architecture

- **Client (Next.js app):**  
  Renders pages/components, triggers uploads, asks questions.

- **API Routes:**  
  - `/api/upload` — accepts ZIP, unzips to `/uploaded`
  - `/api/embed` — reads files, chunks & embeds using OpenAI, stores to Supabase
  - `/api/ask` — embeds questions, does ANN search in Supabase, streams answer

- **Supabase:**  
  - Postgres + `pgvector` for document/project storage
  - RPC for semantic search

- **App Structure:**  
  - UI: `Navbar`, `Hero`, `Features`, `Pricing`, `Workspace`
  - Workspace: `FileUpload`, `ChatPanel` (Enter to send, Shift+Enter for newline), `Sidebar`
  - Custom Hooks: `useOutsideClick` for modals/overlays

```txt
Client UI → Next.js API Routes → Supabase pgvector
            ↘ OpenAI Embeddings/Chat (RAG)
