import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@pages/home/ui/HomePage.vue'),
    meta: { title: '홈' },
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: () => import('@pages/calendar/ui/CalendarPage.vue'),
    meta: { title: '달력' },
  },
  {
    path: '/calendar/:view',
    name: 'CalendarView',
    component: () => import('@pages/calendar/ui/CalendarPage.vue'),
    meta: { title: '달력' },
  },
  {
    path: '/schedule/:id',
    name: 'ScheduleDetail',
    component: () => import('@pages/schedule/ui/ScheduleDetailPage.vue'),
    meta: { title: '일정 상세' },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@pages/settings/ui/SettingsPage.vue'),
    meta: { title: '설정' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@pages/error/ui/NotFoundPage.vue'),
    meta: { title: '페이지를 찾을 수 없습니다' },
  },
]

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { el: to.hash }
    }
    return { top: 0 }
  },
})

// Navigation guards
router.beforeEach((to, _from, next) => {
  // Update document title
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} | EZ Calendar` : 'EZ Calendar'
  next()
})

