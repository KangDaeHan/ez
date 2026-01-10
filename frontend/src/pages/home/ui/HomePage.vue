<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { CalendarWidget } from '@widgets/calendar'
import { ScheduleForm, useScheduleMutations } from '@features/schedule/manage'
import { useScheduleStore, type ScheduleFormData } from '@entities/schedule'
import { Button } from '@shared/ui'
import { initNotificationScheduler, useToast, initTitleNotification, cleanupTitleNotification, showTitleNotification, initServerTimeSync, cleanupServerTimeSync, useServerTime } from '@shared/lib'

const router = useRouter()
const scheduleStore = useScheduleStore()
const { createSchedule } = useScheduleMutations()

const isScheduleFormOpen = ref(false)
const selectedDate = ref(new Date())

// 알림 스케줄러 초기화
let cleanupScheduler: (() => void) | undefined

onMounted(async () => {
  // 서버 시간 동기화 시작
  initServerTimeSync()
  
  // 알림 권한 요청
  if ('Notification' in window && Notification.permission === 'default') {
    await Notification.requestPermission()
  }
  
  // 탭 타이틀 알림 초기화
  initTitleNotification()
  
  // 알림 스케줄러 시작
  cleanupScheduler = initNotificationScheduler(() => scheduleStore.schedules)

  // 개발 환경에서 테스트용 함수 노출
  if (import.meta.env.DEV) {
    const { notification: showToast, success, warning, error } = useToast()
    
    (window as any).testNotification = () => {
      // 인앱 토스트 알림 (항상 작동)
      showToast('📅 테스트 알림', '알림 기능이 정상적으로 작동합니다! 🎉', 8000)
      console.log('✅ 인앱 토스트 알림이 발생했습니다.')
      
      // 탭 타이틀 알림
      showTitleNotification('테스트 알림')
      console.log('✅ 탭 타이틀 알림이 발생했습니다.')
      
      // 브라우저 네이티브 알림
      if (Notification.permission === 'granted') {
        new Notification('📅 테스트 알림', {
          body: '알림 기능이 정상적으로 작동합니다! 🎉',
          icon: '/favicon.svg',
        })
        console.log('✅ 브라우저 알림도 발생했습니다.')
      } else {
        console.log('⚠️ 브라우저 알림 권한이 없습니다. 권한 상태:', Notification.permission)
        warning('브라우저 알림 권한 필요', '브라우저 알림을 받으려면 권한을 허용해주세요.')
        Notification.requestPermission()
      }
    }
    
    (window as any).testToast = (type: string = 'notification') => {
      switch (type) {
        case 'success':
          success('성공!', '작업이 완료되었습니다.')
          break
        case 'warning':
          warning('주의', '확인이 필요한 사항이 있습니다.')
          break
        case 'error':
          error('오류', '문제가 발생했습니다.')
          break
        default:
          showToast('📅 일정 알림', '30분 후에 "팀 회의"가 시작됩니다. 📍 회의실 A', 10000)
      }
      console.log(`✅ ${type} 토스트가 표시되었습니다.`)
    }
    
    (window as any).checkNotificationStatus = () => {
      const { isSynced, timeOffset, lastSyncTime, syncError, getServerTime } = useServerTime()
      
      console.log('📋 알림 상태 체크:')
      console.log('  - 브라우저 지원:', 'Notification' in window)
      console.log('  - 권한 상태:', Notification.permission)
      console.log('  - 등록된 일정 수:', scheduleStore.schedules.length)
      
      const settings = JSON.parse(localStorage.getItem('ez-calendar-settings') || '{}')
      console.log('  - 알림 활성화:', settings.enableNotifications !== false)
      console.log('  - 기본 알림 시간:', settings.defaultReminderMinutes || 30, '분 전')
      
      console.log('\n🕐 서버 시간 동기화 상태:')
      console.log('  - 동기화 완료:', isSynced.value)
      console.log('  - 시간 차이:', `${timeOffset.value}ms (${(timeOffset.value / 1000).toFixed(1)}초)`)
      console.log('  - 마지막 동기화:', lastSyncTime.value?.toLocaleString() || '없음')
      console.log('  - 동기화 오류:', syncError.value || '없음')
      console.log('  - 로컬 시간:', new Date().toLocaleString())
      console.log('  - 서버 시간:', getServerTime().toLocaleString())
      
      if (syncError.value) {
        console.log('\n⚠️ 서버 시간 동기화 문제 해결 방법:')
        console.log('  1. 백엔드 서버가 실행 중인지 확인: http://localhost:8000')
        console.log('  2. API 엔드포인트 확인: http://localhost:8000/api/v1/system/time')
        console.log('  3. window.syncServerTime() 으로 수동 동기화 시도')
      }
    }
    
    (window as any).syncServerTime = async () => {
      const { syncWithServer, getServerTime } = useServerTime()
      console.log('🔄 서버 시간 동기화 중...')
      const result = await syncWithServer()
      if (result) {
        console.log('✅ 동기화 성공!')
        console.log('  - 로컬 시간:', new Date().toLocaleString())
        console.log('  - 서버 시간:', getServerTime().toLocaleString())
      } else {
        console.log('❌ 동기화 실패')
      }
    }
    
    (window as any).testTitleNotification = (message?: string) => {
      showTitleNotification(message || '새 일정 알림')
      console.log('✅ 탭 타이틀 알림이 표시되었습니다.')
      console.log('💡 다른 탭으로 이동하면 깜빡이는 효과를 확인할 수 있습니다.')
    }
    
    console.log('🔔 알림 테스트 함수가 준비되었습니다:')
    console.log('  - window.testNotification() : 전체 알림 테스트 (토스트 + 브라우저 + 탭 타이틀)')
    console.log('  - window.testToast(type) : 토스트만 테스트 (type: notification/success/warning/error)')
    console.log('  - window.testTitleNotification(msg) : 탭 타이틀 알림 테스트')
    console.log('  - window.checkNotificationStatus() : 알림 및 서버 시간 상태 확인')
    console.log('  - window.syncServerTime() : 서버 시간 수동 동기화')
  }
})

onUnmounted(() => {
  if (cleanupScheduler) {
    cleanupScheduler()
  }
  cleanupTitleNotification()
  cleanupServerTimeSync()
})

function handleDateClick(date: Date) {
  selectedDate.value = date
}

function handleScheduleClick(scheduleId: string) {
  router.push(`/schedule/${scheduleId}`)
}

function openNewScheduleForm() {
  isScheduleFormOpen.value = true
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
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center shadow-lg shadow-primary-500/25">
            <svg
              class="w-6 h-6 text-white"
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
          </div>
          <h1 class="text-xl font-bold text-slate-800 dark:text-slate-100">
            EZ Calendar
          </h1>
        </div>
        
        <div class="flex items-center gap-3">
          <Button
            variant="primary"
            @click="openNewScheduleForm"
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
          
          <button
            type="button"
            class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            @click="$router.push('/settings')"
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
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Calendar Widget -->
        <div class="lg:col-span-2">
          <CalendarWidget
            :show-lunar="true"
            :show-holidays="true"
            @date-click="handleDateClick"
            @schedule-click="handleScheduleClick"
          />
        </div>

        <!-- Side Panel - Today's Schedules -->
        <div class="space-y-4">
          <div class="widget p-4">
            <h2 class="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-4">
              선택된 날짜의 일정
            </h2>
            
            <div
              v-if="scheduleStore.schedulesForSelectedDate.length === 0"
              class="text-center py-8 text-slate-500"
            >
              <svg
                class="w-12 h-12 mx-auto mb-3 text-slate-300"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <p>일정이 없습니다</p>
              <Button
                variant="outline"
                size="sm"
                class="mt-3"
                @click="openNewScheduleForm"
              >
                일정 추가하기
              </Button>
            </div>

            <ul
              v-else
              class="space-y-2"
            >
              <li
                v-for="schedule in scheduleStore.schedulesForSelectedDate"
                :key="schedule.id"
                class="p-3 rounded-lg bg-slate-50 dark:bg-slate-700/50 hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer transition-colors"
                @click="handleScheduleClick(schedule.id)"
              >
                <div class="flex items-start gap-3">
                  <div
                    class="w-2 h-2 mt-2 rounded-full"
                    :class="{
                      'bg-red-500': schedule.priority === 'high',
                      'bg-yellow-500': schedule.priority === 'medium',
                      'bg-green-500': schedule.priority === 'low',
                      'bg-slate-400': schedule.priority === 'default'
                    }"
                  />
                  <div class="flex-1 min-w-0">
                    <h3 class="font-medium text-slate-800 dark:text-slate-100 truncate">
                      {{ schedule.title }}
                    </h3>
                    <p
                      v-if="schedule.description"
                      class="text-sm text-slate-500 truncate mt-1"
                    >
                      {{ schedule.description }}
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
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

