export interface ToastMessage {
  id: string
  type: 'info' | 'success' | 'warning' | 'error' | 'notification'
  title: string
  message?: string
  duration?: number
}
