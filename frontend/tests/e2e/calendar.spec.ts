import { test, expect } from '@playwright/test'

test.describe('Calendar Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should display calendar widget', async ({ page }) => {
    // 달력 위젯이 표시되는지 확인
    await expect(page.locator('.widget')).toBeVisible()
  })

  test('should display current month', async ({ page }) => {
    const currentDate = new Date()
    const monthYear = `${currentDate.getFullYear()}년 ${currentDate.getMonth() + 1}월`
    await expect(page.getByText(monthYear)).toBeVisible()
  })

  test('should navigate to previous month', async ({ page }) => {
    const currentDate = new Date()
    const prevMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1)
    const prevMonthYear = `${prevMonth.getFullYear()}년 ${prevMonth.getMonth() + 1}월`

    // 이전 달 버튼 클릭
    await page.getByRole('button', { name: /이전/i }).or(page.locator('button:has(svg)')).first().click()
    
    await expect(page.getByText(prevMonthYear)).toBeVisible()
  })

  test('should open new schedule form', async ({ page }) => {
    // 새 일정 버튼 클릭
    await page.getByRole('button', { name: /새 일정/i }).click()

    // 일정 폼 모달이 표시되는지 확인
    await expect(page.getByText('새 일정')).toBeVisible()
    await expect(page.getByLabel('제목')).toBeVisible()
  })

  test('should navigate to settings', async ({ page }) => {
    // 설정 버튼 클릭
    await page.getByRole('button').filter({ has: page.locator('svg') }).last().click()
    
    // 설정 페이지로 이동 확인
    await expect(page).toHaveURL(/.*settings/)
  })
})

test.describe('Schedule Management', () => {
  test('should create a new schedule', async ({ page }) => {
    await page.goto('/')

    // 새 일정 버튼 클릭
    await page.getByRole('button', { name: /새 일정/i }).click()

    // 폼 입력
    await page.getByLabel('제목').fill('테스트 일정')
    await page.getByPlaceholder('일정에 대한 설명을 입력하세요').fill('테스트 설명입니다.')

    // 저장 버튼 클릭
    await page.getByRole('button', { name: '저장' }).click()

    // 모달이 닫히는지 확인
    await expect(page.getByText('새 일정')).not.toBeVisible()
  })
})

