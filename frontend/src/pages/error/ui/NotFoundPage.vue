<script setup lang="ts">
import { Button } from '@shared/ui'
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="text-center">
      <div class="mb-8">
        <h1 class="text-9xl font-bold text-primary-500/20">404</h1>
        <h2 class="text-2xl font-bold text-slate-800 dark:text-slate-100 -mt-8">
          페이지를 찾을 수 없습니다
        </h2>
        <p class="mt-4 text-slate-600 dark:text-slate-400">
          요청하신 페이지가 존재하지 않거나 이동되었을 수 있습니다.
        </p>
      </div>
      
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <Button @click="$router.push('/')">
          홈으로 돌아가기
        </Button>
        <Button
          variant="outline"
          @click="$router.back()"
        >
          이전 페이지
        </Button>
      </div>
    </div>
  </div>
</template>

