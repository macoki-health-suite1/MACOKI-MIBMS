import { openDB } from "idb";
import type { AppData } from "./types";

const DB_NAME = "macoki-mibms";
const STORE = "workspace";
const KEY = "main";

const emptyData: AppData = {
  products: [], batches: [], contacts: [], sales: [], purchases: [], expenses: [],
  branches: [{ id: "branch-main", name: "Main Branch", code: "MAIN", address: "", active: true }]
};

async function db() {
  return openDB(DB_NAME, 1, {
    upgrade(database) {
      if (!database.objectStoreNames.contains(STORE)) database.createObjectStore(STORE);
    }
  });
}

export async function loadData(): Promise<AppData> {
  try {
    const database = await db();
    const saved = await database.get(STORE, KEY) as AppData | undefined;
    if (!saved) {
      await database.put(STORE, emptyData, KEY);
      return structuredClone(emptyData);
    }
    return { ...structuredClone(emptyData), ...saved };
  } catch {
    const raw = localStorage.getItem("macoki-mibms-fallback");
    return raw ? JSON.parse(raw) as AppData : structuredClone(emptyData);
  }
}

export async function saveData(data: AppData): Promise<void> {
  try {
    const database = await db();
    await database.put(STORE, data, KEY);
  } catch {
    localStorage.setItem("macoki-mibms-fallback", JSON.stringify(data));
  }
}

export function downloadBackup(data: AppData) {
  const blob = new Blob([JSON.stringify({ app: "MACOKI-MIBMS", version: 1, exportedAt: new Date().toISOString(), data }, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `macoki-mibms-backup-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

export async function restoreBackup(file: File): Promise<AppData> {
  const parsed = JSON.parse(await file.text()) as { data?: AppData };
  const data = parsed.data ?? parsed as unknown as AppData;
  const required = ["products", "batches", "contacts", "sales", "purchases", "expenses", "branches"];
  if (!data || required.some((key) => !Array.isArray((data as unknown as Record<string, unknown>)[key]))) {
    throw new Error("This file is not a valid MACOKI MIBMS backup.");
  }
  return data;
}
