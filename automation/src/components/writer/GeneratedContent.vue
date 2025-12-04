<template>
  <div class="bg-white rounded-lg shadow p-6 h-[calc(100vh-200px)] overflow-y-auto">
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-600">Generating your content...</p>
      </div>
    </div>

    <div v-else-if="error" class="flex items-center justify-center py-12">
      <div class="text-center text-red-600">
        <svg class="h-12 w-12 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="font-medium">{{ error }}</p>
      </div>
    </div>

    <div v-else-if="!activeContent" class="flex items-center justify-center py-12">
      <div class="text-center text-gray-500">
        <svg class="h-12 w-12 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p>No content generated yet. Fill in the form and click "Generate Content" to get started.</p>
      </div>
    </div>

    <div v-else class="space-y-4">
      <div class="flex items-center justify-between border-b pb-4">
        <h2 class="text-xl font-bold">{{ activeContent.title }}</h2>
        <div class="flex gap-2">
          <button
            @click="copyToClipboard"
            class="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-md flex items-center gap-2"
          >
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            {{ copied ? 'Copied!' : 'Copy' }}
          </button>
          <button
            @click="handleDelete"
            class="px-3 py-1.5 text-sm bg-red-100 hover:bg-red-200 text-red-700 rounded-md flex items-center gap-2"
          >
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </button>
        </div>
      </div>

      <div class="prose prose-sm max-w-none markdown-content" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { marked } from 'marked'

export default {
  name: 'GeneratedContent',
  props: {
    activeContent: {
      type: Object,
      default: null,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: null,
    },
  },
  emits: ['delete'],
  setup(props, { emit }) {
    const copied = ref(false)

    const renderedContent = computed(() => {
      if (!props.activeContent) return ''
      const text = props.activeContent.generated_text || props.activeContent.content || ''
      return marked(text)
    })

    const copyToClipboard = async () => {
      if (!props.activeContent) return
      const text = props.activeContent.generated_text || props.activeContent.content || ''
      try {
        await navigator.clipboard.writeText(text)
        copied.value = true
        setTimeout(() => {
          copied.value = false
        }, 2000)
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    }

    const handleDelete = () => {
      if (confirm('Are you sure you want to delete this content?')) {
        emit('delete', props.activeContent.name)
      }
    }

    watch(() => props.activeContent, () => {
      copied.value = false
    })

    return {
      copied,
      renderedContent,
      copyToClipboard,
      handleDelete,
    }
  },
}
</script>
