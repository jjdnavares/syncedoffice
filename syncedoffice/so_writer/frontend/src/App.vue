<template>
  <div class="min-h-screen bg-gray-50 p-4 sm:p-8">
    <div class="max-w-6xl mx-auto">
      <header class="flex flex-col items-center gap-3 mb-8">
        <h1 class="text-3xl font-bold">Content Writer</h1>
        <nav class="flex border-b w-full justify-center">
          <router-link 
            to="/" 
            class="py-2 px-4"
            :class="$route.path === '/' ? 'border-b-2 border-blue-600 font-semibold' : 'text-gray-600'"
          >
            Writer
          </router-link>
          <router-link 
            to="/history" 
            class="py-2 px-4"
            :class="$route.path === '/history' ? 'border-b-2 border-blue-600 font-semibold' : 'text-gray-600'"
          >
            History
          </router-link>
        </nav>
      </header>
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>
