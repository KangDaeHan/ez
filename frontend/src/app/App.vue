<script setup lang="ts">
import { RouterView } from 'vue-router'
import { WeatherBackground, Toast } from '@/shared/ui'
import { useToast } from '@/shared/lib'

const { toasts, removeToast } = useToast()
</script>

<template>
  <div class="min-h-screen relative">
    <!-- 날씨 기반 배경 영상 -->
    <WeatherBackground />
    
    <!-- 메인 콘텐츠 -->
    <div class="relative z-10">
      <RouterView />
    </div>
    
    <!-- 전역 토스트 알림 -->
    <Toast :messages="toasts" @remove="removeToast" />
  </div>
</template>

