// lib/server/getFilesRecursively.ts
import { readdir, stat } from "node:fs/promises";
import path from "node:path";

export async function getFilesRecursively(dir: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = await Promise.all(
    entries.map(async (e) => {
      const full = path.join(dir, e.name);
      if (e.isDirectory()) return getFilesRecursively(full);
        return [full];
    })
  );
  return files.flat();
}