export type SchedulePriority = 'high' | 'medium' | 'low' | 'default'

export type ScheduleRepeatType = 'none' | 'daily' | 'weekly' | 'monthly' | 'yearly'

export interface Schedule {
  id: string
  title: string
  description?: string
  startDate: string // ISO 8601 format
  endDate?: string // ISO 8601 format
  allDay: boolean
  priority: SchedulePriority
  color?: string
  location?: string
  imageUrl?: string
  repeat: ScheduleRepeatType
  repeatEndDate?: string
  reminders: ScheduleReminder[]
  createdAt: string
  updatedAt: string
}

export interface ScheduleReminder {
  id: string
  type: 'notification' | 'email'
  minutesBefore: number
}

export interface ScheduleFormData {
  title: string
  description?: string
  startDate: string
  endDate?: string
  allDay: boolean
  priority: SchedulePriority
  color?: string
  location?: string
  image?: File
  repeat: ScheduleRepeatType
  repeatEndDate?: string
  reminders: Omit<ScheduleReminder, 'id'>[]
}

export interface ScheduleFilter {
  startDate?: string
  endDate?: string
  priority?: SchedulePriority[]
  search?: string
}

