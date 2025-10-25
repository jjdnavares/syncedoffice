import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

// Disable Vite HMR in production
if (import.meta.env.PROD) {
  // Prevent Vite client from trying to connect
  if (window.__vite_plugin_react_preamble_installed__) {
    delete window.__vite_plugin_react_preamble_installed__
  }
}

const app = createApp(App)
const pinia = createPinia()

setConfig('resourceFetcher', frappeRequest)

app.use(pinia)
app.use(router)
app.use(resourcesPlugin)

app.component('Button', Button)
app.mount('#app')
