<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CalendarWidget } from '@widgets/calendar'
import { ScheduleForm, useScheduleMutations } from '@features/schedule/manage'
import type { ScheduleFormData } from '@entities/schedule'
import { Button } from '@shared/ui'
import type { CalendarViewType } from '@shared/types'

const route = useRoute()
const router = useRouter()
const { createSchedule } = useScheduleMutations()

const viewType = computed<CalendarViewType>(() => {
  const view = route.params.view as string
  if (['month', 'week', 'day'].includes(view)) {
    return view as CalendarViewType
  }
  return 'month'
})

const isScheduleFormOpen = ref(false)
const selectedDate = ref(new Date())

function handleDateClick(date: Date) {
  selectedDate.value = date
}

function handleScheduleClick(scheduleId: string) {
  router.push(`/schedule/${scheduleId}`)
}

function changeView(view: CalendarViewType) {
  router.push(`/calendar/${view}`)
}

async function handleScheduleSubmit(data: ScheduleFormData) {
  try {
    await createSchedule(data)
    isScheduleFormOpen.value = false
  } catch (error) {
    console.error('일정 생성 실패:', error)
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
            @click="$router.push('/')"
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
            달력
          </h1>
        </div>

        <!-- View Toggle -->
        <div class="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 p-1 rounded-lg">
          <button
            v-for="view in ['month', 'week', 'day'] as CalendarViewType[]"
            :key="view"
            type="button"
            :class="[
              'px-4 py-1.5 text-sm font-medium rounded-md transition-all',
              viewType === view
                ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
            ]"
            @click="changeView(view)"
          >
            {{ view === 'month' ? '월' : view === 'week' ? '주' : '일' }}
          </button>
        </div>

        <Button
          variant="primary"
          @click="isScheduleFormOpen = true"
        >
          <svg
            class="w-5 h-5 mr-1"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 4v16m8-8H4"
            />
          </svg>
          새 일정
        </Button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-6">
      <!-- Month View -->
      <CalendarWidget
        v-if="viewType === 'month'"
        :show-lunar="true"
        :show-holidays="true"
        @date-click="handleDateClick"
        @schedule-click="handleScheduleClick"
      />

      <!-- Week View (TODO: Implement WeekWidget) -->
      <div
        v-else-if="viewType === 'week'"
        class="widget p-8 text-center text-slate-500"
      >
        <p class="text-lg">주간 보기는 준비 중입니다.</p>
        <p class="text-sm mt-2">곧 업데이트될 예정입니다.</p>
      </div>

      <!-- Day View (TODO: Implement DayWidget) -->
      <div
        v-else-if="viewType === 'day'"
        class="widget p-8 text-center text-slate-500"
      >
        <p class="text-lg">일간 보기는 준비 중입니다.</p>
        <p class="text-sm mt-2">곧 업데이트될 예정입니다.</p>
      </div>
    </main>

    <!-- Schedule Form Modal -->
    <ScheduleForm
      v-model="isScheduleFormOpen"
      :initial-date="selectedDate"
      @submit="handleScheduleSubmit"
    />
  </div>
</template>

