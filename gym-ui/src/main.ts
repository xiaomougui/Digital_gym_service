import './assets/all.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate)

app.use(router)
app.use(pinia)
app.use(ElementPlus)
app.mount('#app')
