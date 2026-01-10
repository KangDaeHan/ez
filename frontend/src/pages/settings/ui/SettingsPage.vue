<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@shared/ui'

// Theme settings
const isDarkMode = ref(false)
const showLunarDate = ref(true)
const showHolidays = ref(true)

// Notification settings
const enableNotifications = ref(true)
const defaultReminderMinutes = ref(30)

// Widget settings
const defaultView = ref<'month' | 'week' | 'day'>('month')
const weekStartsOn = ref<0 | 1>(0) // 0 = Sunday, 1 = Monday

onMounted(() => {
  // Load settings from localStorage
  const savedSettings = localStorage.getItem('ez-calendar-settings')
  if (savedSettings) {
    const settings = JSON.parse(savedSettings)
    isDarkMode.value = settings.isDarkMode ?? false
    showLunarDate.value = settings.showLunarDate ?? true
    showHolidays.value = settings.showHolidays ?? true
    enableNotifications.value = settings.enableNotifications ?? true
    defaultReminderMinutes.value = settings.defaultReminderMinutes ?? 30
    defaultView.value = settings.defaultView ?? 'month'
    weekStartsOn.value = settings.weekStartsOn ?? 0
  }

  // Apply dark mode
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  }
})

function saveSettings() {
  const settings = {
    isDarkMode: isDarkMode.value,
    showLunarDate: showLunarDate.value,
    showHolidays: showHolidays.value,
    enableNotifications: enableNotifications.value,
    defaultReminderMinutes: defaultReminderMinutes.value,
    defaultView: defaultView.value,
    weekStartsOn: weekStartsOn.value,
  }
  localStorage.setItem('ez-calendar-settings', JSON.stringify(settings))
  alert('설정이 저장되었습니다.')
}

function toggleDarkMode() {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
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
            설정
          </h1>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-6 max-w-2xl">
      <div class="space-y-6">
        <!-- Display Settings -->
        <section class="widget p-6">
          <h2 class="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-4">
            화면 설정
          </h2>
          <div class="space-y-4">
            <!-- Dark Mode -->
            <!-- <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-slate-800 dark:text-slate-200">다크 모드</p>
                <p class="text-sm text-slate-500">어두운 테마를 사용합니다</p>
              </div>
              <button
                type="button"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  isDarkMode ? 'bg-primary-500' : 'bg-slate-300 dark:bg-slate-600'
                ]"
                @click="toggleDarkMode"
              >
                <span
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full shadow transition-transform',
                    isDarkMode ? 'translate-x-7' : 'translate-x-1'
                  ]"
                />
              </button>
            </div> -->

            <!-- Lunar Date -->
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-slate-800 dark:text-slate-200">음력 표시</p>
                <p class="text-sm text-slate-500">달력에 음력 날짜를 표시합니다</p>
              </div>
              <button
                type="button"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  showLunarDate ? 'bg-primary-500' : 'bg-slate-300 dark:bg-slate-600'
                ]"
                @click="showLunarDate = !showLunarDate"
              >
                <span
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full shadow transition-transform',
                    showLunarDate ? 'translate-x-7' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>

            <!-- Holidays -->
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-slate-800 dark:text-slate-200">공휴일 표시</p>
                <p class="text-sm text-slate-500">한국 공휴일을 표시합니다</p>
              </div>
              <button
                type="button"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  showHolidays ? 'bg-primary-500' : 'bg-slate-300 dark:bg-slate-600'
                ]"
                @click="showHolidays = !showHolidays"
              >
                <span
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full shadow transition-transform',
                    showHolidays ? 'translate-x-7' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>
          </div>
        </section>

        <!-- Calendar Settings -->
        <section class="widget p-6">
          <h2 class="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-4">
            달력 설정
          </h2>
          <div class="space-y-4">
            <!-- Default View -->
            <div>
              <p class="font-medium text-slate-800 dark:text-slate-200 mb-2">기본 보기</p>
              <div class="flex gap-2">
                <button
                  v-for="view in ['month', 'week', 'day'] as const"
                  :key="view"
                  type="button"
                  :class="[
                    'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    defaultView === view
                      ? 'bg-primary-500 text-white'
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'
                  ]"
                  @click="defaultView = view"
                >
                  {{ view === 'month' ? '월' : view === 'week' ? '주' : '일' }}
                </button>
              </div>
            </div>

            <!-- Week Start -->
            <div>
              <p class="font-medium text-slate-800 dark:text-slate-200 mb-2">주 시작일</p>
              <div class="flex gap-2">
                <button
                  type="button"
                  :class="[
                    'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    weekStartsOn === 0
                      ? 'bg-primary-500 text-white'
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'
                  ]"
                  @click="weekStartsOn = 0"
                >
                  일요일
                </button>
                <button
                  type="button"
                  :class="[
                    'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    weekStartsOn === 1
                      ? 'bg-primary-500 text-white'
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'
                  ]"
                  @click="weekStartsOn = 1"
                >
                  월요일
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Notification Settings -->
        <section class="widget p-6">
          <h2 class="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-4">
            알림 설정
          </h2>
          <div class="space-y-4">
            <!-- Enable Notifications -->
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-slate-800 dark:text-slate-200">알림 사용</p>
                <p class="text-sm text-slate-500">일정 알림을 받습니다</p>
              </div>
              <button
                type="button"
                :class="[
                  'relative w-14 h-8 rounded-full transition-colors',
                  enableNotifications ? 'bg-primary-500' : 'bg-slate-300 dark:bg-slate-600'
                ]"
                @click="enableNotifications = !enableNotifications"
              >
                <span
                  :class="[
                    'absolute top-1 w-6 h-6 bg-white rounded-full shadow transition-transform',
                    enableNotifications ? 'translate-x-7' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>

            <!-- Default Reminder -->
            <div>
              <p class="font-medium text-slate-800 dark:text-slate-200 mb-2">기본 알림 시간</p>
              <select
                v-model="defaultReminderMinutes"
                class="w-full px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary-500/20"
              >
                <option :value="5">5분 전</option>
                <option :value="10">10분 전</option>
                <option :value="15">15분 전</option>
                <option :value="30">30분 전</option>
                <option :value="60">1시간 전</option>
                <option :value="1440">1일 전</option>
              </select>
            </div>
          </div>
        </section>

        <!-- Save Button -->
        <div class="flex justify-end">
          <Button @click="saveSettings">
            설정 저장
          </Button>
        </div>
      </div>
    </main>
  </div>
</template>

