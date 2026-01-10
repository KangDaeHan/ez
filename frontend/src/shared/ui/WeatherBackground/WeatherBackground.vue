<script setup lang="ts">
import { useWeather } from '@/shared/lib/useWeather'

const { videoUrl, weatherDescription, temperature, humidity, weatherMain, isLoading } = useWeather()
</script>

<template>
  <div class="weather-background">
    <!-- 비디오 배경 -->
    <video
      v-if="!isLoading && videoUrl"
      :key="videoUrl"
      class="video-bg"
      autoplay
      muted
      loop
      playsinline
    >
      <source :src="videoUrl" type="video/mp4" />
    </video>
    
    <!-- 오버레이 (가독성을 위한 반투명 레이어) -->
    <div class="video-overlay" />
    
    <!-- 날씨 정보 배지 -->
    <div class="weather-badge" v-if="!isLoading && temperature !== null">
      <div class="weather-icon">
        <span v-if="weatherMain === 'Clear'">☀️</span>
        <span v-else-if="weatherMain === 'Clouds'">☁️</span>
        <span v-else-if="weatherMain === 'Rain' || weatherMain === 'Drizzle'">🌧️</span>
        <span v-else-if="weatherMain === 'Thunderstorm'">⛈️</span>
        <span v-else-if="weatherMain === 'Snow'">❄️</span>
        <span v-else-if="weatherMain === 'Mist' || weatherMain === 'Fog' || weatherMain === 'Haze'">🌫️</span>
        <span v-else>🌤️</span>
      </div>
      <div class="weather-info">
        <div class="weather-stats">
          <span class="temperature">{{ temperature }}°C</span>
        </div>
        <div class="description">
          <span>{{ weatherDescription }}</span> &nbsp;
          <span class="humidity">💧 {{ humidity }}%</span>
        </div>
      </div>
    </div>
    
    <!-- 로딩 상태 -->
    <div class="weather-badge loading" v-else-if="isLoading">
      <div class="loading-spinner" />
      <span>날씨 로딩 중...</span>
    </div>
  </div>
</template>

<style scoped>
.weather-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.video-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.85) 0%,
    rgba(255, 255, 255, 0.75) 50%,
    rgba(255, 255, 255, 0.85) 100%
  );
  backdrop-filter: blur(2px);
}

:global(.dark) .video-overlay {
  background: linear-gradient(
    135deg,
    rgba(15, 23, 42, 0.9) 0%,
    rgba(15, 23, 42, 0.8) 50%,
    rgba(15, 23, 42, 0.9) 100%
  );
}

.weather-badge {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  z-index: 100;
  animation: slideIn 0.5s ease-out;
}

:global(.dark) .weather-badge {
  background: rgba(30, 41, 59, 0.9);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.weather-icon {
  font-size: 28px;
  line-height: 1;
}

.weather-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.weather-stats {
  /* align-items: center; */
}

.temperature {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

:global(.dark) .temperature {
  color: #f1f5f9;
}

.humidity {
  font-size: 13px;
  font-weight: 500;
  color: #3b82f6;
  opacity: 0.9;
}

:global(.dark) .humidity {
  color: #60a5fa;
}

.description {
  font-size: 12px;
  color: #64748b;
  text-transform: capitalize;
}

:global(.dark) .description {
  color: #94a3b8;
}

.weather-badge.loading {
  gap: 8px;
  font-size: 12px;
  color: #64748b;
}

:global(.dark) .weather-badge.loading {
  color: #94a3b8;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e2e8f0;
  border-top-color: #ec771d;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

:global(.dark) .loading-spinner {
  border-color: #475569;
  border-top-color: #f09442;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 모바일 반응형 */
@media (max-width: 640px) {
  .weather-badge {
    bottom: 10px;
    right: 10px;
    padding: 8px 12px;
    border-radius: 12px;
  }

  .weather-icon {
    font-size: 22px;
  }

  .temperature {
    font-size: 14px;
  }

  .humidity {
    font-size: 11px;
  }

  .description {
    font-size: 10px;
  }
}
</style>

