<template>
  <div class="w-full">
    <label v-if="label" :for="id" class="label">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    <select
      :id="id"
      :value="modelValue"
      :required="required"
      :disabled="disabled"
      class="input"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="" disabled>{{ placeholder || 'Select an option' }}</option>
      <option
        v-for="option in options"
        :key="getOptionValue(option)"
        :value="getOptionValue(option)"
      >
        {{ getOptionLabel(option) }}
      </option>
    </select>
    <p v-if="helpText" class="mt-1 text-sm text-gray-500">{{ helpText }}</p>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  id: String,
  label: String,
  modelValue: [String, Number],
  options: {
    type: Array,
    required: true,
  },
  placeholder: String,
  required: Boolean,
  disabled: Boolean,
  error: String,
  helpText: String,
  valueKey: {
    type: String,
    default: 'value',
  },
  labelKey: {
    type: String,
    default: 'label',
  },
})

defineEmits(['update:modelValue'])

function getOptionValue(option) {
  return typeof option === 'object' ? option[props.valueKey] : option
}

function getOptionLabel(option) {
  return typeof option === 'object' ? option[props.labelKey] : option
}
</script>
