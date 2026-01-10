<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@shared/lib/cn'

interface Props {
  modelValue?: string | number
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'date' | 'time' | 'datetime-local'
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  error?: string
  label?: string
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  modelValue: '',
  disabled: false,
  readonly: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  'blur': [event: FocusEvent]
  'focus': [event: FocusEvent]
}>()

const inputId = computed(() => props.id || `input-${Math.random().toString(36).slice(2, 9)}`)

const inputClasses = computed(() =>
  cn(
    'w-full px-4 py-2 rounded-lg border transition-all duration-200',
    'bg-white dark:bg-slate-800',
    'text-slate-900 dark:text-slate-100',
    'placeholder:text-slate-400 dark:placeholder:text-slate-500',
    'focus:outline-none focus:ring-2 focus:ring-offset-0',
    props.error
      ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20'
      : 'border-slate-300 dark:border-slate-600 focus:border-primary-500 focus:ring-primary-500/20',
    props.disabled && 'opacity-50 cursor-not-allowed bg-slate-100 dark:bg-slate-900'
  )
)

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', props.type === 'number' ? Number(target.value) : target.value)
}
</script>

<template>
  <div class="w-full">
    <label
      v-if="label"
      :for="inputId"
      class="block mb-1.5 text-sm font-medium text-slate-700 dark:text-slate-300"
    >
      {{ label }}
    </label>
    <input
      :id="inputId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :class="inputClasses"
      @input="handleInput"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    />
    <p
      v-if="error"
      class="mt-1.5 text-sm text-red-500"
    >
      {{ error }}
    </p>
  </div>
</template>

