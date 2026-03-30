import { writable } from 'svelte/store';
import type { Document } from '$lib/api';

export const documents = writable<Document[]>([]);

export function upsertDocument(doc: Document) {
  documents.update((list) => {
    const idx = list.findIndex((d) => d.id === doc.id);
    if (idx === -1) return [doc, ...list];
    const next = [...list];
    next[idx] = doc;
    return next;
  });
}

export function removeDocument(id: string) {
  documents.update((list) => list.filter((d) => d.id !== id));
}
