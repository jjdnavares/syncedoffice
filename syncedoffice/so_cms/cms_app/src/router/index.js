import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/cms',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/cms/content-types',
      },
      {
        path: 'content-types',
        name: 'ContentTypes',
        component: () => import('../views/ContentTypeList.vue'),
      },
      {
        path: 'content-types/new',
        name: 'NewContentType',
        component: () => import('../views/ContentTypeEditor.vue'),
      },
      {
        path: 'content-types/:name',
        name: 'EditContentType',
        component: () => import('../views/ContentTypeEditor.vue'),
      },
      {
        path: 'components',
        name: 'Components',
        component: () => import('../views/ComponentList.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
