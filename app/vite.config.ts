import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  // GitHub Pages serves the app under /<repo>/; relative base works for both
  base: './',
  plugins: [react(), tailwindcss()],
})
