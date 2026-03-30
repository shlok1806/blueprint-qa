<script lang="ts">
  import type { Issue, IssueSeverity, IssueType } from '$lib/api';
  import IssueCard from './IssueCard.svelte';

  export let issues: Issue[];

  type SortKey = 'severity' | 'page' | 'type';
  const severityOrder: Record<IssueSeverity, number> = { high: 0, medium: 1, low: 2 };

  let filterSeverity: string = 'all';
  let filterType: string = 'all';
  let sortBy: SortKey = 'severity';

  $: uniqueTypes = [...new Set(issues.map((i) => i.issue_type))].sort();

  $: filtered = issues
    .filter((i) => filterSeverity === 'all' || i.severity === filterSeverity)
    .filter((i) => filterType === 'all' || i.issue_type === filterType)
    .sort((a, b) => {
      if (sortBy === 'severity') return severityOrder[a.severity] - severityOrder[b.severity];
      if (sortBy === 'page') return a.page_number - b.page_number;
      return a.issue_type.localeCompare(b.issue_type);
    });

  const issueTypeLabels: Record<string, string> = {
    missing_tag:             'Missing Tag',
    dimension_mismatch:      'Dimension Mismatch',
    unlabeled_element:       'Unlabeled Element',
    inconsistent_annotation: 'Inconsistent Annotation',
    missing_scale:           'Missing Scale',
    incomplete_detail:       'Incomplete Detail',
  };
</script>

<div class="flex flex-col gap-4">
  <!-- Filters & Sort -->
  <div class="flex flex-wrap gap-3 items-center">
    <div class="flex items-center gap-2">
      <label for="filter-severity" class="text-xs text-gray-500 font-medium whitespace-nowrap">Severity</label>
      <select
        id="filter-severity"
        bind:value={filterSeverity}
        class="rounded-lg border border-gray-300 bg-white px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">All</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
    </div>

    <div class="flex items-center gap-2">
      <label for="filter-type" class="text-xs text-gray-500 font-medium whitespace-nowrap">Type</label>
      <select
        id="filter-type"
        bind:value={filterType}
        class="rounded-lg border border-gray-300 bg-white px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">All</option>
        {#each uniqueTypes as t}
          <option value={t}>{issueTypeLabels[t] ?? t}</option>
        {/each}
      </select>
    </div>

    <div class="flex items-center gap-2 ml-auto">
      <label for="sort-by" class="text-xs text-gray-500 font-medium whitespace-nowrap">Sort by</label>
      <select
        id="sort-by"
        bind:value={sortBy}
        class="rounded-lg border border-gray-300 bg-white px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="severity">Severity</option>
        <option value="page">Page</option>
        <option value="type">Type</option>
      </select>
    </div>
  </div>

  <!-- Results count -->
  <p class="text-xs text-gray-400">
    Showing {filtered.length} of {issues.length} issue{issues.length !== 1 ? 's' : ''}
  </p>

  {#if filtered.length === 0}
    <div class="card p-8 text-center text-gray-400">
      <svg class="mx-auto h-10 w-10 mb-2 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p class="text-sm">No issues match your filters.</p>
    </div>
  {:else}
    <div class="flex flex-col gap-3">
      {#each filtered as issue (issue.id)}
        <IssueCard {issue} />
      {/each}
    </div>
  {/if}
</div>
