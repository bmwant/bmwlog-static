import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    outDir: 'source/css',
    emptyOutDir: false,
    rollupOptions: {
      input: resolve(__dirname, 'source/scss/theme.scss'),
      output: {
        assetFileNames: '[name][extname]',
      },
    },
    cssMinify: true,
  },
  css: {
    preprocessorOptions: {
      scss: {
        silenceDeprecations: ['import', 'global-builtin'],
      },
    },
  },
});
