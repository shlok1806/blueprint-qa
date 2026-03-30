<script lang="ts">
  import '../app.css';
</script>

<div class="min-h-screen bg-gray-50">
  <!-- Nav -->
  <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 flex items-center gap-3 h-14">
      <a href="/" class="flex items-center gap-2 text-gray-900 hover:text-blue-600 transition-colors">
        <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <span class="text-base font-bold tracking-tight">Blueprint QA</span>
      </a>
      <span class="ml-1 text-xs text-gray-400 font-medium hidden sm:inline">AI-powered drawing QA</span>
    </div>
  </header>

  <!-- Page content -->
  <main class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-8">
    <slot />
  </main>
</div>
