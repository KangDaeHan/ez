<script setup lang="ts">
import { computed } from 'vue'
import { cn, getDay } from '@shared/lib'
import type { Schedule } from '@entities/schedule'

interface DayInfo {
  isToday: boolean
  isCurrentMonth: boolean
  isWeekend: boolean
  holiday: string | null
  lunar: string | null
  schedules: Schedule[]
  isSelected: boolean
}

interface Props {
  date: Date
  info: DayInfo
  compact?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  click: []
  'schedule-click': [scheduleId: string]
}>()

const dayNumber = computed(() => props.date.getDate())
const dayOfWeek = computed(() => getDay(props.date))

const dayClasses = computed(() =>
  cn(
    'calendar-day cursor-pointer',
    props.info.isToday && 'today',
    props.info.isSelected && 'selected',
    !props.info.isCurrentMonth && 'other-month',
    props.info.isWeekend && dayOfWeek.value === 0 && 'weekend',
    props.info.holiday && 'holiday',
    props.compact && 'min-h-[60px]'
  )
)

const numberClasses = computed(() =>
  cn(
    'text-sm font-medium',
    props.info.isToday && 'bg-primary-500 text-white rounded-full w-7 h-7 flex items-center justify-center',
    !props.info.isToday && dayOfWeek.value === 0 && 'text-red-500',
    !props.info.isToday && dayOfWeek.value === 6 && 'text-blue-500',
    !props.info.isCurrentMonth && 'text-slate-400'
  )
)

const visibleSchedules = computed(() => {
  const max = props.compact ? 2 : 3
  return props.info.schedules.slice(0, max)
})

const remainingCount = computed(() => {
  const max = props.compact ? 2 : 3
  return Math.max(0, props.info.schedules.length - max)
})

function getPriorityClass(priority: string) {
  return `priority-${priority}`
}
</script>

<template>
  <div
    :class="dayClasses"
    @click="emit('click')"
  >
    <!-- Day Number -->
    <div class="flex items-center justify-between w-full px-1">
      <span :class="numberClasses">
        {{ dayNumber }}
      </span>
      <span
        v-if="info.lunar && !compact"
        class="text-[10px] text-slate-400"
      >
        {{ info.lunar }}
      </span>
    </div>

    <!-- Holiday Name -->
    <div
      v-if="info.holiday"
      class="w-full px-1 mt-0.5"
    >
      <span class="text-[10px] text-red-500 truncate block">
        {{ info.holiday }}
      </span>
    </div>

    <!-- Schedules -->
    <div class="flex flex-col gap-0.5 w-full mt-1 px-0.5">
      <div
        v-for="schedule in visibleSchedules"
        :key="schedule.id"
        :class="cn('schedule-item', getPriorityClass(schedule.priority))"
        :style="schedule.color ? { backgroundColor: schedule.color } : undefined"
        @click.stop="emit('schedule-click', schedule.id)"
      >
        {{ schedule.title }}
        <span 
          v-if="schedule.imageUrl"
          :class="cn('has-img')"
        >
        </span>
      </div>
      
      <div
        v-if="remainingCount > 0"
        class="text-[10px] text-slate-500 px-1"
      >
        +{{ remainingCount }}개 더보기
      </div>
    </div>
  </div>
</template>

