<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useScheduleStore, scheduleApi, type Schedule, type ScheduleFormData } from '@entities/schedule'
import { ScheduleForm, useScheduleMutations } from '@features/schedule/manage'
import { Button } from '@shared/ui'
import { formatKoreanDate, getImageUrl } from '@shared/lib'

const route = useRoute()
const router = useRouter()
const scheduleStore = useScheduleStore()
const { updateSchedule, deleteSchedule } = useScheduleMutations()

const scheduleId = computed(() => route.params.id as string)
const schedule = ref<Schedule | null>(null)
const isLoading = ref(true)
const isEditFormOpen = ref(false)
const error = ref<string | null>(null)

const priorityLabels: Record<string, string> = {
  high: '높음',
  medium: '보통',
  low: '낮음',
  default: '없음',
}

const repeatLabels: Record<string, string> = {
  none: '반복 안함',
  daily: '매일',
  weekly: '매주',
  monthly: '매월',
  yearly: '매년',
}

// 이미지 URL 변환
const scheduleImageUrl = computed(() => getImageUrl(schedule.value?.imageUrl))

onMounted(async () => {
  try {
    isLoading.value = true
    schedule.value = await scheduleApi.getSchedule(scheduleId.value)
  } catch (err) {
    error.value = '일정을 불러오는데 실패했습니다.'
    console.error(err)
  } finally {
    isLoading.value = false
  }
})

async function handleEditSubmit(data: ScheduleFormData) {
  try {
    await updateSchedule({ id: scheduleId.value, data })
    schedule.value = await scheduleApi.getSchedule(scheduleId.value)
    isEditFormOpen.value = false
  } catch (err) {
    console.error('일정 수정 실패:', err)
  }
}

async function handleDelete() {
  try {
    await deleteSchedule(scheduleId.value)
    router.push('/')
  } catch (err) {
    console.error('일정 삭제 실패:', err)
  }
}
</script>

<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="sticky top-0 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
      <div class="container mx-auto px-4 h-16 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <button
            type="button"
            class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            @click="$router.back()"
          >
            <svg
              class="w-6 h-6 text-slate-600 dark:text-slate-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </button>
          <h1 class="text-xl font-bold text-slate-800 dark:text-slate-100">
            일정 상세
          </h1>
        </div>

        <div
          v-if="schedule"
          class="flex items-center gap-2"
        >
          <Button
            variant="outline"
            @click="isEditFormOpen = true"
          >
            수정
          </Button>
          <Button
            variant="danger"
            @click="handleDelete"
          >
            삭제
          </Button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-6 max-w-2xl">
      <!-- Loading -->
      <div
        v-if="isLoading"
        class="widget p-8 text-center"
      >
        <div class="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full mx-auto" />
        <p class="mt-4 text-slate-500">로딩 중...</p>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="widget p-8 text-center text-red-500"
      >
        <p>{{ error }}</p>
        <Button
          variant="outline"
          class="mt-4"
          @click="$router.push('/')"
        >
          홈으로 돌아가기
        </Button>
      </div>

      <!-- Schedule Detail -->
      <div
        v-else-if="schedule"
        class="widget overflow-hidden"
      >
        <!-- Image -->
        <div
          v-if="scheduleImageUrl"
          class="relative h-64"
        >
          <img
            :src="scheduleImageUrl"
            :alt="schedule.title"
            class="w-full h-full object-cover"
          />
        </div>

        <div class="p-6 space-y-6">
          <!-- Title & Priority -->
          <div class="flex items-start justify-between gap-4">
            <h2 class="text-2xl font-bold text-slate-800 dark:text-slate-100">
              {{ schedule.title }}
            </h2>
            <span
              :class="[
                'px-3 py-1 text-sm font-medium rounded-full',
                {
                  'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200': schedule.priority === 'high',
                  'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-200': schedule.priority === 'medium',
                  'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-200': schedule.priority === 'low',
                  'bg-slate-100 text-slate-800 dark:bg-slate-700 dark:text-slate-200': schedule.priority === 'default',
                }
              ]"
            >
              {{ priorityLabels[schedule.priority] }}
            </span>
          </div>

          <!-- Description -->
          <p
            v-if="schedule.description"
            class="text-slate-600 dark:text-slate-400"
          >
            {{ schedule.description }}
          </p>

          <!-- Details -->
          <div class="space-y-4 pt-4 border-t border-slate-200 dark:border-slate-700">
            <!-- Date -->
            <div class="flex items-center gap-3">
              <svg
                class="w-5 h-5 text-slate-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <div>
                <p class="text-slate-800 dark:text-slate-200">
                  {{ formatKoreanDate(new Date(schedule.startDate)) }}
                </p>
                <p
                  v-if="schedule.endDate"
                  class="text-sm text-slate-500"
                >
                  ~ {{ formatKoreanDate(new Date(schedule.endDate)) }}
                </p>
              </div>
            </div>

            <!-- Location -->
            <div
              v-if="schedule.location"
              class="flex items-center gap-3"
            >
              <svg
                class="w-5 h-5 text-slate-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
              <span class="text-slate-800 dark:text-slate-200">
                {{ schedule.location }}
              </span>
            </div>

            <!-- Repeat -->
            <div
              v-if="schedule.repeat !== 'none'"
              class="flex items-center gap-3"
            >
              <svg
                class="w-5 h-5 text-slate-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              <span class="text-slate-800 dark:text-slate-200">
                {{ repeatLabels[schedule.repeat] }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Edit Form Modal -->
    <ScheduleForm
      v-if="schedule"
      v-model="isEditFormOpen"
      :schedule="schedule"
      @submit="handleEditSubmit"
      @delete="handleDelete"
    />
  </div>
</template>

