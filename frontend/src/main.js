// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' // 这一点非常重要，没有它就没有样式！

const app = createApp(App)


app.use(ElementPlus) // 告诉 Vue 使用 Element Plus
app.mount('#app')