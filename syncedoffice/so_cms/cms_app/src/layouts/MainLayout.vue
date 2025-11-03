<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-900">CMS</h1>
            <div class="ml-10 flex space-x-8">
              <router-link
                to="/cms/content-types"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                :class="isActive('/cms/content-types') ? 'text-primary-600 border-b-2 border-primary-600' : 'text-gray-500 hover:text-gray-700'"
              >
                Content Types
              </router-link>
              <router-link
                to="/cms/components"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium"
                :class="isActive('/cms/components') ? 'text-primary-600 border-b-2 border-primary-600' : 'text-gray-500 hover:text-gray-700'"
              >
                Components
              </router-link>
            </div>
          </div>
          <div class="flex items-center">
            <a href="/app/automation" class="text-sm text-gray-500 hover:text-gray-700">
              ← Back to Desk
            </a>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

function isActive(path) {
  return route.path.startsWith(path)
}
</script>
