import react from '@vitejs/plugin-react'
import path from 'path'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            '^/api/2/.*': {
                target: 'http://127.0.0.1:8001',
                changeOrigin: true,
                xfwd: true,
                secure: false,
            },
        },
    },

    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
            '@tabler/icons-react':
                '@tabler/icons-react/dist/esm/icons/index.mjs',
        },
    },
})
