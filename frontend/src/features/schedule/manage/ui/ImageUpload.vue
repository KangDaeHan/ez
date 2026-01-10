<script setup lang="ts">
import { ref, computed } from 'vue'
import { getImageUrl } from '@shared/lib'

interface Props {
  preview?: string | null
}

const props = defineProps<Props>()

// 이미지 URL 처리 (서버 URL 또는 Data URL)
const displayUrl = computed(() => {
  if (!props.preview) return null
  // Data URL인 경우 그대로 사용
  if (props.preview.startsWith('data:')) return props.preview
  // 서버 URL인 경우 전체 URL로 변환
  return getImageUrl(props.preview)
})

const emit = defineEmits<{
  change: [file: File | null]
}>()

const fileInputRef = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)

function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files?.length) {
    const file = input.files[0]
    if (isValidImage(file)) {
      emit('change', file)
    }
  }
}

function handleDrop(event: DragEvent) {
  event.preventDefault()
  isDragging.value = false

  const files = event.dataTransfer?.files
  if (files?.length) {
    const file = files[0]
    if (isValidImage(file)) {
      emit('change', file)
    }
  }
}

function handleDragOver(event: DragEvent) {
  event.preventDefault()
  isDragging.value = true
}

function handleDragLeave() {
  isDragging.value = false
}

function isValidImage(file: File): boolean {
  const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  if (!validTypes.includes(file.type)) {
    alert('이미지 파일만 업로드 가능합니다. (JPG, PNG, GIF, WEBP)')
    return false
  }
  if (file.size > 5 * 1024 * 1024) {
    alert('파일 크기는 5MB 이하여야 합니다.')
    return false
  }
  return true
}

function openFilePicker() {
  fileInputRef.value?.click()
}

function removeImage() {
  emit('change', null)
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}
</script>

<template>
  <div>
    <label class="block mb-1.5 text-sm font-medium text-slate-700 dark:text-slate-300">
      이미지
    </label>
    
    <!-- Preview -->
    <div
      v-if="displayUrl"
      class="relative group"
    >
      <img
        :src="displayUrl"
        alt="미리보기"
        class="w-full h-48 object-cover rounded-lg"
      />
      <button
        type="button"
        class="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
        @click="removeImage"
      >
        <svg
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>

    <!-- Upload Area -->
    <div
      v-if="!displayUrl"
      :class="[
        'border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer',
        isDragging
          ? 'border-primary-500 bg-primary-50 dark:bg-primary-950'
          : 'border-slate-300 dark:border-slate-600 hover:border-primary-400'
      ]"
      @click="openFilePicker"
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
    >
      <svg
        class="mx-auto h-12 w-12 text-slate-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 48 48"
      >
        <path
          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <p class="mt-2 text-sm text-slate-600 dark:text-slate-400">
        클릭하거나 이미지를 드래그하여 업로드
      </p>
      <p class="mt-1 text-xs text-slate-500">
        PNG, JPG, GIF, WEBP (최대 5MB)
      </p>
    </div>

    <input
      ref="fileInputRef"
      type="file"
      accept="image/*"
      class="hidden"
      @change="handleFileSelect"
    />
  </div>
</template>

