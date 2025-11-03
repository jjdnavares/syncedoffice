<template>
  <div class="card p-6 hover:shadow-md transition-shadow cursor-pointer" @click="$emit('edit', contentType)">
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center">
        <div class="w-10 h-10 rounded-lg bg-primary-100 flex items-center justify-center mr-3">
          <component v-if="iconComponent" :is="iconComponent" :size="20" class="text-primary-600" />
          <FileText v-else :size="20" class="text-primary-600" />
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900">{{ contentType.display_name }}</h3>
          <p class="text-sm text-gray-500">{{ contentType.api_id }}</p>
        </div>
      </div>
      <button
        class="text-gray-400 hover:text-red-600 transition-colors"
        @click.stop="$emit('delete', contentType)"
      >
        <Trash2 :size="18" />
      </button>
    </div>

    <p v-if="contentType.description" class="text-sm text-gray-600 mb-4 line-clamp-2">
      {{ contentType.description }}
    </p>

    <div class="flex items-center justify-between text-sm">
      <div class="flex items-center text-gray-500">
        <Layers :size="16" class="mr-1" />
        <span>{{ fieldCount }} fields</span>
      </div>
      <div class="flex items-center space-x-2">
        <span
          class="px-2 py-1 rounded-full text-xs font-medium"
          :class="contentType.is_published ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
        >
          {{ contentType.is_published ? 'Published' : 'Draft' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FileText, Trash2, Layers } from 'lucide-vue-next'
import * as LucideIcons from 'lucide-vue-next'

const props = defineProps({
  contentType: {
    type: Object,
    required: true,
  },
})

defineEmits(['edit', 'delete'])

const fieldCount = computed(() => {
  return props.contentType.fields?.length || 0
})

const iconComponent = computed(() => {
  if (!props.contentType.icon) return null
  
  // Convert icon name to PascalCase component name
  const iconName = props.contentType.icon
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join('')
  
  return LucideIcons[iconName] || null
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
