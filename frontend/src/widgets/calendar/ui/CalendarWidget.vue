<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useScheduleStore } from '@entities/schedule'
import { cn, formatMonthYear, getCalendarDays, navigateMonth, isToday, isSameMonth, isWeekend, getHolidayName, formatLunarDate } from '@shared/lib'
import CalendarDay from './CalendarDay.vue'
import CalendarHeader from './CalendarHeader.vue'

interface Props {
  showLunar?: boolean
  showHolidays?: boolean
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showLunar: true,
  showHolidays: true,
  compact: false,
})

const emit = defineEmits<{
  'date-click': [date: Date]
  'schedule-click': [scheduleId: string]
}>()

const scheduleStore = useScheduleStore()

const currentDate = ref(new Date())
const selectedDate = computed(() => scheduleStore.selectedDate)

const calendarDays = computed(() => getCalendarDays(currentDate.value))
const monthYear = computed(() => formatMonthYear(currentDate.value))

const weekDays = ['일', '월', '화', '수', '목', '금', '토']

function handlePrevMonth() {
  currentDate.value = navigateMonth(currentDate.value, 'prev')
}

function handleNextMonth() {
  currentDate.value = navigateMonth(currentDate.value, 'next')
}

function handleToday() {
  currentDate.value = new Date()
  scheduleStore.setSelectedDate(new Date())
}

function handleDateClick(date: Date) {
  scheduleStore.setSelectedDate(date)
  emit('date-click', date)
}

function handleScheduleClick(scheduleId: string) {
  emit('schedule-click', scheduleId)
}

function getDayInfo(date: Date) {
  return {
    isToday: isToday(date),
    isCurrentMonth: isSameMonth(date, currentDate.value),
    isWeekend: isWeekend(date),
    holiday: props.showHolidays ? getHolidayName(date) : null,
    lunar: props.showLunar ? formatLunarDate(date) : null,
    schedules: scheduleStore.getSchedulesForDate(date),
    isSelected: selectedDate.value ? isToday(date) && isToday(selectedDate.value) : false,
  }
}

// Sync with store's selected date
watch(
  () => scheduleStore.selectedDate,
  (newDate) => {
    if (newDate && !isSameMonth(newDate, currentDate.value)) {
      currentDate.value = newDate
    }
  }
)
</script>

<template>
  <div :class="cn('widget p-4', compact && 'p-2')">
    <!-- Header -->
    <CalendarHeader
      :month-year="monthYear"
      :compact="compact"
      @prev="handlePrevMonth"
      @next="handleNextMonth"
      @today="handleToday"
    />

    <!-- Week Days Header -->
    <div class="grid grid-cols-7 mb-2">
      <div
        v-for="(day, index) in weekDays"
        :key="day"
        :class="cn(
          'text-center text-sm font-medium py-2',
          index === 0 && 'text-red-500',
          index === 6 && 'text-blue-500',
          index > 0 && index < 6 && 'text-slate-600 dark:text-slate-400'
        )"
      >
        {{ day }}
      </div>
    </div>

    <!-- Calendar Grid -->
    <div class="grid grid-cols-7 border-l border-t border-slate-200 dark:border-slate-700">
      <CalendarDay
        v-for="day in calendarDays"
        :key="day.toISOString()"
        :date="day"
        :info="getDayInfo(day)"
        :compact="compact"
        @click="handleDateClick(day)"
        @schedule-click="handleScheduleClick"
      />
    </div>
  </div>
</template>

