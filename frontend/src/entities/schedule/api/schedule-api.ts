import { apiClient } from '@shared/api'
import type { Schedule, ScheduleFormData, ScheduleFilter } from '../model/types'
import type { ApiResponse, PaginatedResponse } from '@shared/types'

const BASE_PATH = '/schedules'

export const scheduleApi = {
  // 일정 목록 조회
  async getSchedules(params?: ScheduleFilter): Promise<PaginatedResponse<Schedule>> {
    return apiClient.get<PaginatedResponse<Schedule>>(BASE_PATH, { params })
  },

  // 일정 상세 조회
  async getSchedule(id: string): Promise<Schedule> {
    const response = await apiClient.get<ApiResponse<Schedule>>(`${BASE_PATH}/${id}`)
    return response.data
  },

  // 일정 생성
  async createSchedule(data: ScheduleFormData): Promise<Schedule> {
    // 빈 문자열을 제거하고 유효한 값만 전송
    const cleanData = Object.fromEntries(
      Object.entries(data).filter(([key, value]) => {
        if (key === 'image') return false // 이미지는 별도 처리
        if (key === 'reminders') return true // reminders는 항상 포함
        return value !== undefined && value !== ''
      })
    )

    if (data.image) {
      const formData = new FormData()
      Object.entries(data).forEach(([key, value]) => {
        if (key === 'image' && value instanceof File) {
          formData.append('image', value)
        } else if (key === 'reminders') {
          formData.append(key, JSON.stringify(value))
        } else if (value !== undefined && value !== '') {
          formData.append(key, String(value))
        }
      })
      const response = await apiClient.upload<ApiResponse<Schedule>>(`${BASE_PATH}/upload`, formData)
      return response.data
    }

    const response = await apiClient.post<ApiResponse<Schedule>>(BASE_PATH, cleanData)
    return response.data
  },

  // 일정 수정
  async updateSchedule(id: string, data: Partial<ScheduleFormData>): Promise<Schedule> {
    // 빈 문자열을 제거하고 유효한 값만 전송
    const cleanData = Object.fromEntries(
      Object.entries(data).filter(([key, value]) => {
        if (key === 'image') return false
        if (key === 'reminders') return true
        return value !== undefined && value !== ''
      })
    )

    if (data.image) {
      const formData = new FormData()
      Object.entries(data).forEach(([key, value]) => {
        if (key === 'image' && value instanceof File) {
          formData.append('image', value)
        } else if (key === 'reminders') {
          formData.append(key, JSON.stringify(value))
        } else if (value !== undefined && value !== '') {
          formData.append(key, String(value))
        }
      })
      const response = await apiClient.upload<ApiResponse<Schedule>>(
        `${BASE_PATH}/${id}`,
        formData
      )
      return response.data
    }

    const response = await apiClient.put<ApiResponse<Schedule>>(`${BASE_PATH}/${id}`, cleanData)
    return response.data
  },

  // 일정 삭제
  async deleteSchedule(id: string): Promise<void> {
    await apiClient.delete(`${BASE_PATH}/${id}`)
  },

  // 날짜 범위로 일정 조회
  async getSchedulesByDateRange(startDate: string, endDate: string): Promise<Schedule[]> {
    const response = await apiClient.get<ApiResponse<Schedule[]>>(`${BASE_PATH}/range`, {
      params: { startDate, endDate },
    })
    return response.data
  },
}

