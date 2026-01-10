<script setup lang="ts">
import { watch } from 'vue'
import type { ToastMessage } from './types'

const props = defineProps<{
  messages: ToastMessage[]
}>()

const emit = defineEmits<{
  remove: [id: string]
}>()

function getIcon(type: ToastMessage['type']) {
  switch (type) {
    case 'success': return '✅'
    case 'warning': return '⚠️'
    case 'error': return '❌'
    case 'notification': return '🔔'
    default: return 'ℹ️'
  }
}

function getBgClass(type: ToastMessage['type']) {
  switch (type) {
    case 'success': return 'bg-green-500'
    case 'warning': return 'bg-yellow-500'
    case 'error': return 'bg-red-500'
    case 'notification': return 'bg-primary-500'
    default: return 'bg-blue-500'
  }
}

// 자동 제거 타이머
watch(() => props.messages, (messages) => {
  messages.forEach((msg) => {
    if (msg.duration !== 0) {
      setTimeout(() => {
        emit('remove', msg.id)
      }, msg.duration || 5000)
    }
  })
}, { deep: true })
</script>

<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[9999] flex flex-col gap-3 pointer-events-none">
      <TransitionGroup name="toast">
        <div
          v-for="toast in messages"
          :key="toast.id"
          class="pointer-events-auto max-w-sm w-full bg-white dark:bg-slate-800 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden animate-slide-in"
        >
          <div class="flex items-start gap-3 p-4">
            <!-- Icon -->
            <div
              :class="[
                'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-white text-lg',
                getBgClass(toast.type)
              ]"
            >
              {{ getIcon(toast.type) }}
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p class="font-semibold text-slate-800 dark:text-slate-100 truncate">
                {{ toast.title }}
              </p>
              <p
                v-if="toast.message"
                class="text-sm text-slate-600 dark:text-slate-400 mt-0.5 line-clamp-2"
              >
                {{ toast.message }}
              </p>
            </div>
            
            <!-- Close Button -->
            <button
              type="button"
              class="flex-shrink-0 p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
              @click="emit('remove', toast.id)"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- Progress Bar -->
          <div
            v-if="toast.duration !== 0"
            class="h-1 bg-slate-100 dark:bg-slate-700"
          >
            <div
              :class="['h-full', getBgClass(toast.type)]"
              :style="{ animation: `shrink ${toast.duration || 5000}ms linear forwards` }"
            />
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-enter-active {
  animation: slide-in 0.3s ease-out;
}

.toast-leave-active {
  animation: slide-out 0.3s ease-in forwards;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slide-out {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

@keyframes shrink {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

.animate-slide-in {
  animation: slide-in 0.3s ease-out;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
