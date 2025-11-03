<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex min-h-screen items-center justify-center p-4">
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="$emit('cancel')"></div>

      <!-- Modal -->
      <div class="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">
            {{ isNew ? 'Add Field' : 'Edit Field' }}
          </h3>
          <button @click="$emit('cancel')" class="text-gray-400 hover:text-gray-600">
            <X :size="20" />
          </button>
        </div>

        <!-- Body -->
        <div class="p-6 space-y-4">
          <!-- Field Name -->
          <BaseInput
            v-model="formData.field_name"
            label="Field Name"
            placeholder="e.g., title"
            required
            :error="errors.field_name"
            help-text="Internal name (snake_case)"
          />

          <!-- Field Label -->
          <BaseInput
            v-model="formData.field_label"
            label="Field Label"
            placeholder="e.g., Title"
            required
            :error="errors.field_label"
            help-text="Display label for this field"
          />

          <!-- Field Type -->
          <BaseSelect
            v-model="formData.field_type"
            label="Field Type"
            :options="fieldTypeOptions"
            value-key="type"
            label-key="label"
            required
            disabled
          />

          <!-- Placeholder -->
          <BaseInput
            v-model="formData.placeholder"
            label="Placeholder"
            placeholder="Enter placeholder text..."
          />

          <!-- Help Text -->
          <div>
            <label class="label">Help Text</label>
            <textarea
              v-model="formData.help_text"
              rows="2"
              class="input"
              placeholder="Additional information for content editors..."
            ></textarea>
          </div>

          <!-- Default Value -->
          <BaseInput
            v-model="formData.default_value"
            label="Default Value"
            placeholder="Enter default value..."
          />

          <!-- Validation Options -->
          <div class="grid grid-cols-2 gap-4">
            <div class="flex items-center">
              <input
                v-model="formData.required"
                type="checkbox"
                id="required"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <label for="required" class="ml-2 text-sm text-gray-700">
                Required
              </label>
            </div>

            <div class="flex items-center">
              <input
                v-model="formData.unique"
                type="checkbox"
                id="unique"
                class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <label for="unique" class="ml-2 text-sm text-gray-700">
                Unique
              </label>
            </div>
          </div>

          <!-- Text Field Validation -->
          <div v-if="['Text', 'Long Text'].includes(formData.field_type)" class="grid grid-cols-2 gap-4">
            <BaseInput
              v-model.number="formData.min_length"
              type="number"
              label="Min Length"
              placeholder="0"
            />
            <BaseInput
              v-model.number="formData.max_length"
              type="number"
              label="Max Length"
              placeholder="255"
            />
          </div>

          <!-- Regex Pattern -->
          <BaseInput
            v-if="['Text', 'Email', 'URL'].includes(formData.field_type)"
            v-model="formData.regex_pattern"
            label="Regex Pattern"
            placeholder="e.g., ^[a-z0-9-]+$"
            help-text="Custom validation pattern"
          />

          <!-- Enumeration Options -->
          <div v-if="formData.field_type === 'Enumeration'">
            <label class="label">Enum Values (one per line)</label>
            <textarea
              v-model="enumValues"
              rows="4"
              class="input"
              placeholder="option1&#10;option2&#10;option3"
            ></textarea>
          </div>

          <!-- Relation Options -->
          <div v-if="formData.field_type === 'Relation'">
            <BaseInput
              v-model="relationTarget"
              label="Target Content Type"
              placeholder="e.g., Blog"
              help-text="Name of the content type to link to"
            />
          </div>

          <!-- Component Options -->
          <div v-if="formData.field_type === 'Component'">
            <BaseInput
              v-model="componentRef"
              label="Component Reference"
              placeholder="e.g., SEO"
              help-text="Name of the component to use"
            />
          </div>
        </div>

        <!-- Footer -->
        <div class="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex justify-end space-x-3">
          <BaseButton variant="secondary" @click="$emit('cancel')">
            Cancel
          </BaseButton>
          <BaseButton @click="handleSave">
            {{ isNew ? 'Add Field' : 'Save Changes' }}
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { X } from 'lucide-vue-next'
import { FIELD_TYPES } from '../utils/fieldTypes'
import BaseButton from './BaseButton.vue'
import BaseInput from './BaseInput.vue'
import BaseSelect from './BaseSelect.vue'

const props = defineProps({
  field: {
    type: Object,
    required: true,
  },
  isNew: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['save', 'cancel'])

const formData = ref({ ...props.field })
const errors = ref({})

// Computed for special field types
const enumValues = ref('')
const relationTarget = ref('')
const componentRef = ref('')

// Initialize special field options
if (formData.value.options) {
  const options = typeof formData.value.options === 'string' 
    ? JSON.parse(formData.value.options) 
    : formData.value.options

  if (formData.value.field_type === 'Enumeration' && options.values) {
    enumValues.value = options.values.join('\n')
  } else if (formData.value.field_type === 'Relation' && options.target) {
    relationTarget.value = options.target
  } else if (formData.value.field_type === 'Component' && options.component) {
    componentRef.value = options.component
  }
}

const fieldTypeOptions = computed(() => FIELD_TYPES)

// Auto-generate field_name from field_label
watch(() => formData.value.field_label, (newVal) => {
  if (props.isNew && newVal && !formData.value.field_name) {
    formData.value.field_name = newVal
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_+|_+$/g, '')
  }
})

function validateForm() {
  errors.value = {}

  if (!formData.value.field_name) {
    errors.value.field_name = 'Field name is required'
  } else if (!/^[a-z][a-z0-9_]*$/.test(formData.value.field_name)) {
    errors.value.field_name = 'Field name must be snake_case (lowercase, underscores only)'
  }

  if (!formData.value.field_label) {
    errors.value.field_label = 'Field label is required'
  }

  return Object.keys(errors.value).length === 0
}

function handleSave() {
  if (!validateForm()) {
    return
  }

  // Build options object based on field type
  let options = null

  if (formData.value.field_type === 'Enumeration' && enumValues.value) {
    options = {
      values: enumValues.value.split('\n').filter(v => v.trim())
    }
  } else if (formData.value.field_type === 'Relation' && relationTarget.value) {
    options = {
      target: relationTarget.value
    }
  } else if (formData.value.field_type === 'Component' && componentRef.value) {
    options = {
      component: componentRef.value
    }
  }

  const fieldData = {
    ...formData.value,
    options: options ? JSON.stringify(options) : null
  }

  emit('save', fieldData)
}
</script>
