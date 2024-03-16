import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server: {
        host: '0.0.0.0',
        port: 8000,
        proxy: {
            '/api': {
                target: 'http://0.0.0.0:8001',
                changeOrigin: true,
                secure: false,
            },
            '/media': {
                target: 'http://0.0.0.0:8001',
                changeOrigin: true,
                secure: false,
            },
        }
    },
})
