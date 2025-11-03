<template>
  <div class="card p-6">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Fields</h2>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Field Types Panel -->
      <div class="lg:col-span-1">
        <h3 class="text-sm font-medium text-gray-700 mb-3">Field Types</h3>
        <div class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="category in FIELD_CATEGORIES"
            :key="category.name"
            class="mb-4"
          >
            <h4 class="text-xs font-semibold text-gray-500 uppercase mb-2">
              {{ category.label }}
            </h4>
            <div class="space-y-1">
              <button
                v-for="fieldType in getFieldTypesByCategory(category.name)"
                :key="fieldType.type"
                class="w-full text-left px-3 py-2 rounded-lg border border-gray-200 hover:border-primary-500 hover:bg-primary-50 transition-colors flex items-center"
                @click="addField(fieldType)"
              >
                <component :is="getIcon(fieldType.icon)" :size="16" class="mr-2 text-gray-600" />
                <span class="text-sm">{{ fieldType.label }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Fields Canvas -->
      <div class="lg:col-span-3">
        <div class="mb-4 flex justify-between items-center">
          <h3 class="text-sm font-medium text-gray-700">
            {{ fields.length }} {{ fields.length === 1 ? 'Field' : 'Fields' }}
          </h3>
        </div>

        <!-- Empty State -->
        <div v-if="!fields.length" class="text-center py-12 border-2 border-dashed border-gray-300 rounded-lg">
          <Layers :size="48" class="mx-auto text-gray-400 mb-2" />
          <p class="text-gray-500">Click a field type to add it</p>
        </div>

        <!-- Fields List -->
        <draggable
          v-else
          v-model="fields"
          item-key="field_name"
          handle=".drag-handle"
          class="space-y-2"
          @end="handleDragEnd"
        >
          <template #item="{ element, index }">
            <FieldItem
              :field="element"
              :index="index"
              @edit="editField"
              @delete="deleteField"
            />
          </template>
        </draggable>
      </div>
    </div>

    <!-- Field Configuration Modal -->
    <FieldConfigModal
      v-if="editingField"
      :field="editingField"
      :is-new="isNewField"
      @save="saveField"
      @cancel="cancelEdit"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import draggable from 'vuedraggable'
import { Layers } from 'lucide-vue-next'
import * as LucideIcons from 'lucide-vue-next'
import { FIELD_TYPES, FIELD_CATEGORIES, getFieldTypesByCategory } from '../utils/fieldTypes'
import FieldItem from './FieldItem.vue'
import FieldConfigModal from './FieldConfigModal.vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue'])

const fields = ref([...props.modelValue])
const editingField = ref(null)
const editingIndex = ref(-1)
const isNewField = ref(false)

watch(() => props.modelValue, (newVal) => {
  fields.value = [...newVal]
}, { deep: true })

watch(fields, (newVal) => {
  emit('update:modelValue', newVal)
}, { deep: true })

function getIcon(iconName) {
  const name = iconName.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('')
  return LucideIcons[name] || LucideIcons.FileText
}

function addField(fieldType) {
  const newField = {
    field_name: '',
    field_label: '',
    field_type: fieldType.type,
    required: false,
    unique: false,
    position: fields.value.length + 1,
    default_value: '',
    placeholder: '',
    help_text: '',
    options: null,
  }
  
  editingField.value = newField
  editingIndex.value = -1
  isNewField.value = true
}

function editField(field, index) {
  editingField.value = { ...field }
  editingIndex.value = index
  isNewField.value = false
}

function saveField(fieldData) {
  if (isNewField.value) {
    fields.value.push(fieldData)
  } else {
    fields.value[editingIndex.value] = fieldData
  }
  
  // Update positions
  fields.value.forEach((field, idx) => {
    field.position = idx + 1
  })
  
  cancelEdit()
}

function deleteField(index) {
  if (confirm('Are you sure you want to delete this field?')) {
    fields.value.splice(index, 1)
    
    // Update positions
    fields.value.forEach((field, idx) => {
      field.position = idx + 1
    })
  }
}

function cancelEdit() {
  editingField.value = null
  editingIndex.value = -1
  isNewField.value = false
}

function handleDragEnd() {
  // Update positions after drag
  fields.value.forEach((field, idx) => {
    field.position = idx + 1
  })
}
</script>
