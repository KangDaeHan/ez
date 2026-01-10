import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Schedule, ScheduleFilter } from './types'
import { isSameDay, parseISO } from '@shared/lib'

export const useScheduleStore = defineStore('schedule', () => {
  // State
  const schedules = ref<Schedule[]>([])
  const selectedSchedule = ref<Schedule | null>(null)
  const selectedDate = ref<Date>(new Date())
  const filter = ref<ScheduleFilter>({})
  const isLoading = ref(false)

  // Getters
  const filteredSchedules = computed(() => {
    let result = [...schedules.value]

    if (filter.value.search) {
      const searchLower = filter.value.search.toLowerCase()
      result = result.filter(
        (s) =>
          s.title.toLowerCase().includes(searchLower) ||
          s.description?.toLowerCase().includes(searchLower)
      )
    }

    if (filter.value.priority?.length) {
      result = result.filter((s) => filter.value.priority!.includes(s.priority))
    }

    if (filter.value.startDate) {
      const start = parseISO(filter.value.startDate)
      result = result.filter((s) => parseISO(s.startDate) >= start)
    }

    if (filter.value.endDate) {
      const end = parseISO(filter.value.endDate)
      result = result.filter((s) => parseISO(s.startDate) <= end)
    }

    return result.sort(
      (a, b) => parseISO(a.startDate).getTime() - parseISO(b.startDate).getTime()
    )
  })

  const schedulesForSelectedDate = computed(() => {
    return filteredSchedules.value.filter((schedule) =>
      isSameDay(parseISO(schedule.startDate), selectedDate.value)
    )
  })

  const getSchedulesForDate = (date: Date) => {
    return filteredSchedules.value.filter((schedule) =>
      isSameDay(parseISO(schedule.startDate), date)
    )
  }

  // Actions
  function setSelectedDate(date: Date) {
    selectedDate.value = date
  }

  function setSelectedSchedule(schedule: Schedule | null) {
    selectedSchedule.value = schedule
  }

  function setFilter(newFilter: ScheduleFilter) {
    filter.value = { ...filter.value, ...newFilter }
  }

  function clearFilter() {
    filter.value = {}
  }

  function setSchedules(newSchedules: Schedule[]) {
    schedules.value = newSchedules
  }

  function addSchedule(schedule: Schedule) {
    schedules.value.push(schedule)
  }

  function updateSchedule(updatedSchedule: Schedule) {
    const index = schedules.value.findIndex((s) => s.id === updatedSchedule.id)
    if (index !== -1) {
      schedules.value[index] = updatedSchedule
    }
  }

  function removeSchedule(scheduleId: string) {
    schedules.value = schedules.value.filter((s) => s.id !== scheduleId)
  }

  function setLoading(loading: boolean) {
    isLoading.value = loading
  }

  return {
    // State
    schedules,
    selectedSchedule,
    selectedDate,
    filter,
    isLoading,
    // Getters
    filteredSchedules,
    schedulesForSelectedDate,
    getSchedulesForDate,
    // Actions
    setSelectedDate,
    setSelectedSchedule,
    setFilter,
    clearFilter,
    setSchedules,
    addSchedule,
    updateSchedule,
    removeSchedule,
    setLoading,
  }
})

