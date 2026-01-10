import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { scheduleApi, useScheduleStore, type ScheduleFormData } from '@entities/schedule'

export function useScheduleMutations() {
  const queryClient = useQueryClient()
  const scheduleStore = useScheduleStore()

  const createMutation = useMutation({
    mutationFn: (data: ScheduleFormData) => scheduleApi.createSchedule(data),
    onSuccess: (schedule) => {
      scheduleStore.addSchedule(schedule)
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
    },
    onError: (error) => {
      console.error('일정 생성 실패:', error)
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ScheduleFormData> }) =>
      scheduleApi.updateSchedule(id, data),
    onSuccess: (schedule) => {
      scheduleStore.updateSchedule(schedule)
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
    },
    onError: (error) => {
      console.error('일정 수정 실패:', error)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => scheduleApi.deleteSchedule(id),
    onSuccess: (_data, id) => {
      scheduleStore.removeSchedule(id)
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
    },
    onError: (error) => {
      console.error('일정 삭제 실패:', error)
    },
  })

  return {
    createSchedule: createMutation.mutateAsync,
    updateSchedule: updateMutation.mutateAsync,
    deleteSchedule: deleteMutation.mutateAsync,
    isCreating: createMutation.isPending,
    isUpdating: updateMutation.isPending,
    isDeleting: deleteMutation.isPending,
  }
}

