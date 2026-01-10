import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import { router } from '@app/router'
import { vueQueryOptions } from '@shared/config/query-client'
import App from '@app/App.vue'

import '@app/styles/index.css'

const app = createApp(App)

// Pinia Store
const pinia = createPinia()
app.use(pinia)

// Vue Query
app.use(VueQueryPlugin, vueQueryOptions)

// Router
app.use(router)

app.mount('#app')

