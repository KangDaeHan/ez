<script setup lang="ts">
import { cn } from '@shared/lib'
import { Button } from '@shared/ui'

interface Props {
  monthYear: string
  compact?: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  prev: []
  next: []
  today: []
}>()
</script>

<template>
  <div :class="cn('flex items-center justify-between mb-4', compact && 'mb-2')">
    <h2 :class="cn('text-xl font-bold text-slate-800 dark:text-slate-100', compact && 'text-base')">
      {{ monthYear }}
    </h2>
    
    <div class="flex items-center gap-2">
      <Button
        variant="ghost"
        :size="compact ? 'sm' : 'md'"
        @click="emit('today')"
      >
        오늘
      </Button>
      
      <div class="flex items-center">
        <button
          type="button"
          class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
          @click="emit('prev')"
        >
          <svg
            class="w-5 h-5 text-slate-600 dark:text-slate-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>
        
        <button
          type="button"
          class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
          @click="emit('next')"
        >
          <svg
            class="w-5 h-5 text-slate-600 dark:text-slate-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

