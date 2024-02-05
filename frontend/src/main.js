import './scss/app.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const store = createPinia()

const app = createApp(App)
    .use(router)
    .use(store)

app.mount('#app')
