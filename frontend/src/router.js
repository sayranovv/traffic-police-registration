import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: () => import('@/components/ReportGenerator.vue') },
        { path: '/edit', component: () => import('@/components/EditDatabase.vue') },
    ],
})