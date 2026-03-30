<script lang="ts">
  import type { Document } from '$lib/api';
  import { deleteDocument } from '$lib/api';
  import { removeDocument } from '$lib/stores/documents';
  import StatusBadge from './StatusBadge.svelte';

  export let document: Document;

  let deleting = false;
  let error = '';

  function formatDate(iso: string) {
    return new Date(iso).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });
  }

  async function handleDelete(e: MouseEvent) {
    e.preventDefault();
    if (!confirm(`Delete "${document.filename}"? This cannot be undone.`)) return;
    deleting = true;
    try {
      await deleteDocument(document.id);
      removeDocument(document.id);
    } catch (err) {
      error = (err as Error).message;
      deleting = false;
    }
  }
</script>

<div class="card p-5 flex flex-col gap-4 hover:shadow-md transition-shadow">
  <!-- Header -->
  <div class="flex items-start justify-between gap-2">
    <div class="flex items-center gap-2 min-w-0">
      <svg class="h-5 w-5 flex-shrink-0 text-red-500" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/>
      </svg>
      <span class="text-sm font-semibold text-gray-800 truncate" title={document.filename}>
        {document.filename}
      </span>
    </div>
    <StatusBadge status={document.status} />
  </div>

  <!-- Meta -->
  <div class="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-500">
    {#if document.page_count}
      <span>{document.page_count} page{document.page_count !== 1 ? 's' : ''}</span>
    {/if}
    <span>Uploaded {formatDate(document.uploaded_at)}</span>
    {#if document.issue_count > 0}
      <span class="font-medium text-amber-600">{document.issue_count} issue{document.issue_count !== 1 ? 's' : ''}</span>
    {:else if document.status === 'completed'}
      <span class="font-medium text-green-600">No issues</span>
    {/if}
  </div>

  {#if error}
    <p class="text-xs text-red-600">{error}</p>
  {/if}

  <!-- Actions -->
  <div class="flex gap-2 mt-auto pt-1">
    <a href="/documents/{document.id}" class="btn-primary text-xs flex-1 justify-center">
      View Analysis
    </a>
    <button
      class="btn-secondary text-xs px-3"
      on:click={handleDelete}
      disabled={deleting}
      title="Delete document"
    >
      {#if deleting}
        <svg class="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
      {:else}
        <svg class="h-4 w-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
      {/if}
    </button>
  </div>
</div>
