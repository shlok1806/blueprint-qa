<script lang="ts">
  import type { Issue } from '$lib/api';

  export let issue: Issue;

  const severityStyles: Record<string, string> = {
    high:   'bg-red-100 text-red-800 border-red-200',
    medium: 'bg-amber-100 text-amber-800 border-amber-200',
    low:    'bg-green-100 text-green-800 border-green-200',
  };

  const issueTypeLabels: Record<string, string> = {
    missing_tag:              'Missing Tag',
    dimension_mismatch:       'Dimension Mismatch',
    unlabeled_element:        'Unlabeled Element',
    inconsistent_annotation:  'Inconsistent Annotation',
    missing_scale:            'Missing Scale',
    incomplete_detail:        'Incomplete Detail',
  };

  $: severityClass = severityStyles[issue.severity] ?? severityStyles.low;
  $: typeLabel = issueTypeLabels[issue.issue_type] ?? issue.issue_type;
</script>

<div class="card p-4 flex flex-col gap-3">
  <div class="flex items-start justify-between gap-3 flex-wrap">
    <div class="flex items-center gap-2 flex-wrap">
      <span class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wide {severityClass}">
        {issue.severity}
      </span>
      <span class="inline-flex items-center rounded-md bg-blue-50 border border-blue-200 px-2.5 py-0.5 text-xs font-medium text-blue-700">
        {typeLabel}
      </span>
    </div>
    <span class="text-xs text-gray-400 whitespace-nowrap">Page {issue.page_number}</span>
  </div>

  <p class="text-sm text-gray-800 leading-relaxed">{issue.description}</p>

  {#if issue.location_hint}
    <div class="flex items-center gap-1.5 text-xs text-gray-500">
      <svg class="h-3.5 w-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
      </svg>
      <span>{issue.location_hint}</span>
    </div>
  {/if}
</div>
