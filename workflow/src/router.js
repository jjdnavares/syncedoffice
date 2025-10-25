import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'WorkflowList',
    component: () => import('@/pages/WorkflowList.vue'),
  },
  {
    path: '/workflow/:name',
    name: 'WorkflowEditor',
    component: () => import('@/pages/WorkflowEditor.vue'),
  },
]

let router = createRouter({
  history: createWebHistory('/workflow'),
  routes,
})

export default router
