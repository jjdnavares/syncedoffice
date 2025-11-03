import { createRouter, createWebHistory } from 'vue-router'
import WriterPage from './pages/WriterPage.vue'
import HistoryPage from './pages/HistoryPage.vue'

const routes = [
  {
    path: '/',
    name: 'Writer',
    component: WriterPage,
  },
  {
    path: '/history',
    name: 'History',
    component: HistoryPage,
  },
]

const router = createRouter({
  history: createWebHistory('/so_writer'),
  routes,
})

export default router
