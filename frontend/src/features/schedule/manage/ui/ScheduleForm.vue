<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Button, Input, Modal } from '@shared/ui'
import type { ScheduleFormData, Schedule, SchedulePriority, ScheduleRepeatType } from '@entities/schedule'
import { formatDate } from '@shared/lib'
import ImageUpload from './ImageUpload.vue'

interface Props {
  modelValue: boolean
  schedule?: Schedule | null
  initialDate?: Date
}

const props = withDefaults(defineProps<Props>(), {
  schedule: null,
  initialDate: () => new Date(),
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [data: ScheduleFormData]
  'delete': [scheduleId: string]
}>()

const isEditing = computed(() => !!props.schedule)
const modalTitle = computed(() => (isEditing.value ? '일정 수정' : '새 일정'))

// Form state
const formData = ref<ScheduleFormData>({
  title: '',
  description: '',
  startDate: formatDate(props.initialDate, "yyyy-MM-dd'T'HH:mm"),
  endDate: '',
  allDay: false,
  priority: 'default',
  color: '',
  location: '',
  repeat: 'none',
  repeatEndDate: '',
  reminders: [],
})

const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)

const priorities: { value: SchedulePriority; label: string; color: string }[] = [
  { value: 'high', label: '높음', color: 'bg-red-500' },
  { value: 'medium', label: '보통', color: 'bg-yellow-500' },
  { value: 'low', label: '낮음', color: 'bg-green-500' },
  { value: 'default', label: '없음', color: 'bg-slate-400' },
]

const repeatOptions: { value: ScheduleRepeatType; label: string }[] = [
  { value: 'none', label: '반복 안함' },
  { value: 'daily', label: '매일' },
  { value: 'weekly', label: '매주' },
  { value: 'monthly', label: '매월' },
  { value: 'yearly', label: '매년' },
]

const reminderOptions: { value: number; label: string }[] = [
  { value: 0, label: '일정 시작 시' },
  { value: 5, label: '5분 전' },
  { value: 10, label: '10분 전' },
  { value: 15, label: '15분 전' },
  { value: 30, label: '30분 전' },
  { value: 60, label: '1시간 전' },
  { value: 120, label: '2시간 전' },
  { value: 1440, label: '1일 전' },
]

// 알림 추가
function addReminder() {
  // 기본 30분 전 알림 추가
  formData.value.reminders.push({
    type: 'notification',
    minutesBefore: 30,
  })
}

// 알림 삭제
function removeReminder(index: number) {
  formData.value.reminders.splice(index, 1)
}

// Validation
const errors = ref<Record<string, string>>({})

function validate(): boolean {
  errors.value = {}

  if (!formData.value.title.trim()) {
    errors.value.title = '제목을 입력해주세요'
  }

  if (!formData.value.startDate) {
    errors.value.startDate = '시작 날짜를 선택해주세요'
  }

  return Object.keys(errors.value).length === 0
}

// Event handlers
function handleImageChange(file: File | null) {
  imageFile.value = file
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
  } else {
    imagePreview.value = null
  }
}

function handleSubmit() {
  if (!validate()) return

  emit('submit', {
    ...formData.value,
    image: imageFile.value || undefined,
  })
  closeModal()
}

function handleDelete() {
  if (props.schedule && confirm('이 일정을 삭제하시겠습니까?')) {
    emit('delete', props.schedule.id)
    closeModal()
  }
}

function closeModal() {
  emit('update:modelValue', false)
}

function resetForm() {
  formData.value = {
    title: '',
    description: '',
    startDate: formatDate(props.initialDate, "yyyy-MM-dd'T'HH:mm"),
    endDate: '',
    allDay: false,
    priority: 'default',
    color: '',
    location: '',
    repeat: 'none',
    repeatEndDate: '',
    reminders: [],
  }
  imageFile.value = null
  imagePreview.value = null
  errors.value = {}
}

// Watch for schedule prop changes (editing mode)
watch(
  () => props.schedule,
  (schedule) => {
    if (schedule) {
      formData.value = {
        title: schedule.title,
        description: schedule.description || '',
        startDate: schedule.startDate,
        endDate: schedule.endDate || '',
        allDay: schedule.allDay,
        priority: schedule.priority,
        color: schedule.color || '',
        location: schedule.location || '',
        repeat: schedule.repeat,
        repeatEndDate: schedule.repeatEndDate || '',
        reminders: schedule.reminders.map((r) => ({
          type: r.type,
          minutesBefore: r.minutesBefore,
        })),
      }
      imagePreview.value = schedule.imageUrl || null
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

// Reset when modal closes
watch(
  () => props.modelValue,
  (isOpen) => {
    if (!isOpen) {
      resetForm()
    }
  }
)
</script>

<template>
  <Modal
    :model-value="modelValue"
    :title="modalTitle"
    size="xl"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <form
      class="space-y-4"
      @submit.prevent="handleSubmit"
    >
      <!-- Title -->
      <Input
        v-model="formData.title"
        label="제목"
        placeholder="일정 제목을 입력하세요"
        :error="errors.title"
      />

      <!-- Description -->
      <div>
        <label class="block mb-1.5 text-sm font-medium text-slate-700 dark:text-slate-300">
          설명
        </label>
        <textarea
          v-model="formData.description"
          rows="3"
          class="w-full px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
          placeholder="일정에 대한 설명을 입력하세요"
        />
      </div>

      <!-- Date & Time -->
      <div class="grid grid-cols-2 gap-4">
        <Input
          v-model="formData.startDate"
          type="datetime-local"
          label="시작"
          :error="errors.startDate"
        />
        <Input
          v-model="formData.endDate"
          type="datetime-local"
          label="종료"
        />
      </div>

      <!-- All Day -->
      <label class="flex items-center gap-2 cursor-pointer">
        <input
          v-model="formData.allDay"
          type="checkbox"
          class="w-4 h-4 rounded border-slate-300 text-primary-500 focus:ring-primary-500"
        />
        <span class="text-sm text-slate-700 dark:text-slate-300">종일</span>
      </label>

      <!-- Location -->
      <Input
        v-model="formData.location"
        label="장소"
        placeholder="장소를 입력하세요"
      />

      <!-- Priority -->
      <div>
        <label class="block mb-1.5 text-sm font-medium text-slate-700 dark:text-slate-300">
          우선순위
        </label>
        <div class="flex gap-2">
          <button
            v-for="priority in priorities"
            :key="priority.value"
            type="button"
            :class="[
              'px-3 py-1.5 rounded-lg text-sm font-medium transition-all',
              formData.priority === priority.value
                ? `${priority.color} text-white`
                : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'
            ]"
            @click="formData.priority = priority.value"
          >
            {{ priority.label }}
          </button>
        </div>
      </div>

      <!-- Repeat -->
      <div>
        <label class="block mb-1.5 text-sm font-medium text-slate-700 dark:text-slate-300">
          반복
        </label>
        <select
          v-model="formData.repeat"
          class="w-full px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500"
        >
          <option
            v-for="option in repeatOptions"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Reminders -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <label class="text-sm font-medium text-slate-700 dark:text-slate-300">
            알림
          </label>
          <button
            type="button"
            class="text-sm text-primary-500 hover:text-primary-600 font-medium"
            @click="addReminder"
          >
            + 알림 추가
          </button>
        </div>
        
        <div v-if="formData.reminders.length === 0" class="text-sm text-slate-500 py-2">
          알림이 없습니다. 알림을 추가하면 일정 시작 전에 알려드립니다.
        </div>
        
        <div class="space-y-2">
          <div
            v-for="(reminder, index) in formData.reminders"
            :key="index"
            class="flex items-center gap-2"
          >
            <select
              v-model="reminder.minutesBefore"
              class="flex-1 px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20"
            >
              <option
                v-for="option in reminderOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
            <button
              type="button"
              class="p-2 text-slate-400 hover:text-red-500 transition-colors"
              @click="removeReminder(index)"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Image Upload -->
      <ImageUpload
        :preview="imagePreview"
        @change="handleImageChange"
      />

      <!-- Color Picker -->
      <div>
        <label class="block mb-1.5 text-sm font-medium text-slate-700 dark:text-slate-300">
          색상
        </label>
        <input
          v-model="formData.color"
          type="color"
          class="w-12 h-10 rounded cursor-pointer"
        />
      </div>
    </form>

    <template #footer>
      <div class="flex justify-between">
        <Button
          v-if="isEditing"
          variant="danger"
          @click="handleDelete"
        >
          삭제
        </Button>
        <div class="flex gap-2 ml-auto">
          <Button
            variant="ghost"
            @click="closeModal"
          >
            취소
          </Button>
          <Button @click="handleSubmit">
            {{ isEditing ? '수정' : '저장' }}
          </Button>
        </div>
      </div>
    </template>
  </Modal>
</template>

