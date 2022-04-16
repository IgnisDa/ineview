import adapter from '@sveltejs/adapter-node';
import presetMini from '@unocss/preset-mini';
import presetWind from '@unocss/preset-wind';
import preprocess from 'svelte-preprocess';
import { presetUno } from 'unocss';
import Unocss from 'unocss/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  preprocess: preprocess(),
  kit: {
    adapter: adapter({ out: '../../dist/apps/admin-site' }),
    vite: {
      ssr: { noExternal: ['carbon-components-svelte'] },
      plugins: [
        Unocss({
          presets: [presetUno(), presetWind(), presetMini()],
        }),
      ],
    },
  },
};

export default config;
