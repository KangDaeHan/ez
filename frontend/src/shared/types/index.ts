// Common API response types
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export interface ApiError {
  message: string
  code: string
  details?: Record<string, string[]>
}

// Date related types
export type CalendarViewType = 'month' | 'week' | 'day'

export interface DateRange {
  start: Date
  end: Date
}

// Common component props
export interface BaseComponentProps {
  class?: string
}

