<script lang="ts">
  import type { DocumentStatus } from '$lib/api';

  export let status: DocumentStatus;

  const config: Record<DocumentStatus, { label: string; classes: string; spin: boolean }> = {
    pending:    { label: 'Pending',    classes: 'bg-gray-100 text-gray-600 border-gray-200',  spin: false },
    processing: { label: 'Analyzing', classes: 'bg-blue-100 text-blue-700 border-blue-200',   spin: true  },
    completed:  { label: 'Completed', classes: 'bg-green-100 text-green-700 border-green-200', spin: false },
    failed:     { label: 'Failed',    classes: 'bg-red-100 text-red-700 border-red-200',       spin: false },
  };

  $: cfg = config[status] ?? config.pending;
</script>

<span class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium {cfg.classes}">
  {#if cfg.spin}
    <svg class="h-3 w-3 animate-spin" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
  {:else if status === 'completed'}
    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
    </svg>
  {:else if status === 'failed'}
    <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
    </svg>
  {:else}
    <span class="h-1.5 w-1.5 rounded-full bg-current"></span>
  {/if}
  {cfg.label}
</span>
