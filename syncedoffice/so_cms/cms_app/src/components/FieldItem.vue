<template>
  <div class="card p-4 hover:shadow-md transition-shadow">
    <div class="flex items-center justify-between">
      <div class="flex items-center flex-1">
        <!-- Drag Handle -->
        <button class="drag-handle mr-3 text-gray-400 hover:text-gray-600 cursor-move">
          <GripVertical :size="20" />
        </button>

        <!-- Field Info -->
        <div class="flex-1">
          <div class="flex items-center">
            <h4 class="text-sm font-medium text-gray-900">
              {{ field.field_label || field.field_name || 'Untitled Field' }}
            </h4>
            <span v-if="field.required" class="ml-2 text-xs text-red-500">*</span>
            <span v-if="field.unique" class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded">
              Unique
            </span>
          </div>
          <div class="flex items-center mt-1 text-xs text-gray-500">
            <span class="mr-3">{{ field.field_name }}</span>
            <span class="px-2 py-0.5 bg-gray-100 rounded">{{ field.field_type }}</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center space-x-2">
        <button
          class="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
          @click="$emit('edit', field, index)"
        >
          <Edit2 :size="16" />
        </button>
        <button
          class="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
          @click="$emit('delete', index)"
        >
          <Trash2 :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { GripVertical, Edit2, Trash2 } from 'lucide-vue-next'

defineProps({
  field: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    required: true,
  },
})

defineEmits(['edit', 'delete'])
</script>
