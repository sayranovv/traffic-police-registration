import './assets/main.css'
import { router } from './router.js'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { createApp } from 'vue'
import App from './App.vue'


createApp(App).use(router).use(autoAnimatePlugin).mount('#app')
