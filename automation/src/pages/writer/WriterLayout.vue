<template>
  <div class="min-h-screen bg-gray-50 p-4 sm:p-8">
    <div class="max-w-6xl mx-auto">
      <header class="flex flex-col items-center gap-3 mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Content Writer</h1>
        <nav class="flex gap-4">
          <router-link
            to="/writer"
            class="px-4 py-2 rounded-md transition-colors"
            :class="$route.name === 'Writer' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-700'"
          >
            Writer
          </router-link>
          <router-link
            to="/writer/history"
            class="px-4 py-2 rounded-md transition-colors"
            :class="$route.name === 'WriterHistory' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-700'"
          >
            History
          </router-link>
          <router-link
            to="/workflow"
            class="px-4 py-2 rounded-md bg-gray-200 hover:bg-gray-300 text-gray-700 transition-colors"
          >
            ← Back to Workflows
          </router-link>
        </nav>
      </header>
      <router-view />
    </div>
  </div>
</template>
