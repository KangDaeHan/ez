import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Button from './Button.vue'

describe('Button', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, {
      slots: {
        default: '버튼 텍스트',
      },
    })
    expect(wrapper.text()).toContain('버튼 텍스트')
  })

  it('emits click event when clicked', async () => {
    const wrapper = mount(Button)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('does not emit click when disabled', async () => {
    const wrapper = mount(Button, {
      props: {
        disabled: true,
      },
    })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeFalsy()
  })

  it('shows loading spinner when loading', () => {
    const wrapper = mount(Button, {
      props: {
        loading: true,
      },
      slots: {
        default: '로딩 중',
      },
    })
    expect(wrapper.find('svg.animate-spin').exists()).toBe(true)
  })

  it('applies variant classes correctly', () => {
    const wrapper = mount(Button, {
      props: {
        variant: 'danger',
      },
    })
    expect(wrapper.classes()).toContain('bg-red-500')
  })

  it('applies size classes correctly', () => {
    const wrapper = mount(Button, {
      props: {
        size: 'sm',
      },
    })
    expect(wrapper.classes()).toContain('px-3')
  })
})

