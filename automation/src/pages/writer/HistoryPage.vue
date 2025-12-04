<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold">Content History</h2>
      <button
        @click="loadHistory"
        :disabled="isLoading"
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
      >
        <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Refresh
      </button>
    </div>

    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-600">Loading history...</p>
      </div>
    </div>

    <div v-else-if="contents.length === 0" class="flex items-center justify-center py-12">
      <div class="text-center text-gray-500">
        <svg class="h-12 w-12 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p>No content history yet. Generate some content to see it here.</p>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="content in contents"
        :key="content.name"
        class="bg-white rounded-lg shadow p-4 hover:shadow-lg transition-shadow cursor-pointer"
        @click="viewContent(content)"
      >
        <div class="flex items-start justify-between mb-2">
          <h3 class="font-semibold text-lg line-clamp-2">{{ content.title }}</h3>
        </div>
        <div class="space-y-1 text-sm text-gray-600 mb-3">
          <p><span class="font-medium">Type:</span> {{ content.content_type }}</p>
          <p><span class="font-medium">Keyword:</span> {{ content.keyword }}</p>
          <p><span class="font-medium">Tone:</span> {{ content.tone }}</p>
          <p><span class="font-medium">Created:</span> {{ formatDate(content.creation) }}</p>
        </div>
        <div class="flex gap-2">
          <button
            @click.stop="viewContent(content)"
            class="flex-1 px-3 py-1.5 text-sm bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-md"
          >
            View
          </button>
          <button
            @click.stop="handleDelete(content.name)"
            class="px-3 py-1.5 text-sm bg-red-100 hover:bg-red-200 text-red-700 rounded-md"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getGeneratedContents, deleteContent } from '@/lib/writer-api'

export default {
  name: 'HistoryPage',
  setup() {
    const router = useRouter()
    const contents = ref([])
    const isLoading = ref(false)

    const loadHistory = async () => {
      isLoading.value = true
      const response = await getGeneratedContents()
      if (response.message) {
        contents.value = response.message
      }
      isLoading.value = false
    }

    const viewContent = (content) => {
      router.push({ name: 'Writer', params: { activeContent: content } })
    }

    const handleDelete = async (name) => {
      if (confirm('Are you sure you want to delete this content?')) {
        await deleteContent(name)
        await loadHistory()
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }

    onMounted(() => {
      loadHistory()
    })

    return {
      contents,
      isLoading,
      loadHistory,
      viewContent,
      handleDelete,
      formatDate,
    }
  },
}
</script>
