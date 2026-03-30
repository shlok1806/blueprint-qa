<script lang="ts">
  import type { Document } from '$lib/api';
  import { onMount } from 'svelte';
  import UploadZone from '$lib/components/UploadZone.svelte';
  import DocumentCard from '$lib/components/DocumentCard.svelte';
  import { documents, upsertDocument } from '$lib/stores/documents';
  import { listDocuments } from '$lib/api';

  let loading = true;

  onMount(async () => {
    try {
      const result = await listDocuments();
      documents.set(result.documents);
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      loading = false;
    }
  });

  let refreshing = false;

  async function refresh() {
    refreshing = true;
    try {
      const result = await listDocuments();
      documents.set(result.documents);
    } finally {
      refreshing = false;
    }
  }

  function onUploaded(e: CustomEvent<Document>) {
    upsertDocument(e.detail);
  }
</script>

<svelte:head>
  <title>Blueprint QA</title>
</svelte:head>

<div class="flex flex-col gap-10">
  <!-- Hero -->
  <section class="text-center py-6">
    <h1 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">Blueprint QA</h1>
    <p class="mt-2 text-gray-500 max-w-xl mx-auto text-sm sm:text-base">
      Upload engineering drawings and let AI flag QA issues automatically — missing tags, dimension mismatches, unlabeled elements, and more.
    </p>
  </section>

  <!-- Upload Zone -->
  <section class="max-w-2xl mx-auto w-full">
    <UploadZone on:uploaded={onUploaded} />
  </section>

  <!-- Documents Grid -->
  <section>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-bold text-gray-800">
        Documents
        {#if $documents.length > 0}
          <span class="ml-1 text-sm font-normal text-gray-400">({$documents.length})</span>
        {/if}
      </h2>
      <button
        class="btn-secondary text-xs"
        on:click={refresh}
        disabled={refreshing}
        title="Refresh list"
      >
        <svg class="h-3.5 w-3.5 {refreshing ? 'animate-spin' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        Refresh
      </button>
    </div>

    {#if loading}
      <div class="card p-12 text-center text-gray-400">
        <svg class="mx-auto h-8 w-8 animate-spin mb-3 text-blue-400" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        <p class="text-sm">Loading documents…</p>
      </div>
    {:else if $documents.length === 0}
      <div class="card p-12 text-center text-gray-400">
        <svg class="mx-auto h-14 w-14 mb-3 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
        </svg>
        <p class="text-base font-medium text-gray-500">No drawings uploaded yet</p>
        <p class="text-sm mt-1">Upload a PDF above to get started.</p>
      </div>
    {:else}
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {#each $documents as doc (doc.id)}
          <DocumentCard document={doc} />
        {/each}
      </div>
    {/if}
  </section>
</div>
