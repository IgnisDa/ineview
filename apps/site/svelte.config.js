import preprocess from 'svelte-preprocess';
import adapter from '@sveltejs/adapter-static';
import Unocss from 'unocss/vite';
import { presetUno } from 'unocss';
import presetWind from '@unocss/preset-wind';
import presetMini from '@unocss/preset-mini';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  preprocess: preprocess(),

  kit: {
    adapter: adapter({
      pages: '../../dist/apps/site',
    }),
    vite: {
      plugins: [
        Unocss({
          presets: [presetUno(), presetWind(), presetMini()],
        }),
      ],
    },
  },
};

export default config;
