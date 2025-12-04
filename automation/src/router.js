import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // Home - redirect to workflow
  {
    path: '/',
    redirect: '/workflow',
  },
  // Workflow routes
  {
    path: '/workflow',
    name: 'WorkflowList',
    component: () => import('@/pages/WorkflowList.vue'),
  },
  {
    path: '/workflow/:name',
    name: 'WorkflowEditor',
    component: () => import('@/pages/WorkflowEditor.vue'),
  },
  // Writer routes
  {
    path: '/writer',
    component: () => import('@/pages/writer/WriterLayout.vue'),
    children: [
      {
        path: '',
        name: 'Writer',
        component: () => import('@/pages/writer/WriterPage.vue'),
      },
      {
        path: 'history',
        name: 'WriterHistory',
        component: () => import('@/pages/writer/HistoryPage.vue'),
      },
    ],
  },
]

let router = createRouter({
  history: createWebHistory('/automation'),
  routes,
})

export default router
