<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { uploadDocument } from '$lib/api';
  import type { Document } from '$lib/api';

  const dispatch = createEventDispatcher<{ uploaded: Document }>();

  const MAX_MB = 50;
  let dragOver = false;
  let uploading = false;
  let progress = 0;
  let error = '';
  let inputEl: HTMLInputElement;

  function onDragOver(e: DragEvent) {
    e.preventDefault();
    dragOver = true;
  }

  function onDragLeave() {
    dragOver = false;
  }

  async function onDrop(e: DragEvent) {
    e.preventDefault();
    dragOver = false;
    const file = e.dataTransfer?.files[0];
    if (file) await handleFile(file);
  }

  function onInputChange(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) handleFile(file);
  }

  async function handleFile(file: File) {
    error = '';
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      error = 'Only PDF files are accepted.';
      return;
    }
    if (file.size > MAX_MB * 1024 * 1024) {
      error = `File exceeds the ${MAX_MB}MB limit.`;
      return;
    }

    uploading = true;
    progress = 10;

    // Fake progress while uploading
    const ticker = setInterval(() => {
      if (progress < 85) progress += 5;
    }, 200);

    try {
      const doc = await uploadDocument(file);
      progress = 100;
      dispatch('uploaded', doc);
    } catch (err) {
      error = (err as Error).message;
    } finally {
      clearInterval(ticker);
      uploading = false;
      progress = 0;
      if (inputEl) inputEl.value = '';
    }
  }
</script>

<div
  role="button"
  tabindex="0"
  class="relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed transition-colors px-8 py-16 cursor-pointer
         {dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white hover:border-blue-400 hover:bg-gray-50'}"
  on:dragover={onDragOver}
  on:dragleave={onDragLeave}
  on:drop={onDrop}
  on:click={() => !uploading && inputEl?.click()}
  on:keydown={(e) => e.key === 'Enter' && !uploading && inputEl?.click()}
>
  <input
    bind:this={inputEl}
    type="file"
    accept=".pdf,application/pdf"
    class="hidden"
    on:change={onInputChange}
  />

  {#if uploading}
    <div class="flex flex-col items-center gap-4 w-full max-w-xs">
      <svg class="h-12 w-12 animate-spin text-blue-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
      <p class="text-sm font-medium text-gray-600">Uploading…</p>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div
          class="bg-blue-500 h-2 rounded-full transition-all duration-300"
          style="width: {progress}%"
        ></div>
      </div>
      <p class="text-xs text-gray-400">{progress}%</p>
    </div>
  {:else}
    <svg class="h-14 w-14 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 48 48">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
        d="M28 8H12a4 4 0 00-4 4v24a4 4 0 004 4h24a4 4 0 004-4V20M28 8l12 12M28 8v12h12M24 28v-8m-4 4l4-4 4 4"/>
    </svg>
    <p class="text-base font-semibold text-gray-700">Drop a PDF here</p>
    <p class="text-sm text-gray-400 mt-1">or <span class="text-blue-600 underline underline-offset-2">browse to upload</span></p>
    <p class="text-xs text-gray-300 mt-3">PDF only · max {MAX_MB}MB</p>
  {/if}
</div>

{#if error}
  <p class="mt-3 text-sm text-red-600 flex items-center gap-1">
    <svg class="h-4 w-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
    </svg>
    {error}
  </p>
{/if}
