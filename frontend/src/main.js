import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from "axios";

import 'bootstrap/dist/css/bootstrap.min.css'
import 'element-plus/dist/index.css'

import '@/assets/bs-custom.scss'
import '@/assets/main.css'

import ApiPlugin from './plugins/api'
import Notify from './plugins/notify'

const app = createApp(App)

app.use(ApiPlugin)

app.use(createPinia())
app.use(router)

axios.interceptors.response.use(function (resp) {
    resp.success = resp.data.success
    resp.result = resp.data.result
    if (!resp.success) {
        resp.errors = resp.data.errors
    }
    return resp
}, function (error) {
    let status = error.response.status
    if (status === 404) {
        Notify.error('Ошибка 404')
    } else if (status > 500) {
        Notify.error('Ошибка сервера. код: ' + status)
    } else {
        Notify.error('Ошибка запроса. код: ' + status)
    }

    return Promise.reject(error)
})

document.title = 'Optimazer'

app.mount('#app')
