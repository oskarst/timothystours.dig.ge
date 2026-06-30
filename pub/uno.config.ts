import { defineConfig, presetUno, presetWebFonts } from 'unocss'

export default defineConfig({
  theme: {
    colors: {
      bgPrimary: '#282b28',
      primary: '#723834',
      accent: '#d49a46',
      textLight: '#f4f4f4',
      textDark: '#282b28'
    }
  },
  presets: [
    presetUno(),
    presetWebFonts({
      provider: 'none', // using local fonts or system fonts
      fonts: {
        sans: ['Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
        serif: ['Georgia', 'serif']
      }
    })
  ],
  preflights: [
    {
      getCSS: () => `
        *, ::before, ::after {
          box-sizing: border-box;
        }
        .brush-edge-top { position: relative; }
        .brush-edge-top::before {
          content: ''; position: absolute; top: -19px; left: 50%; transform: translateX(-50%); width: 100vw; height: 20px;
          background-color: inherit;
          -webkit-mask-image: url('assets/brush.svg'); mask-image: url('assets/brush.svg');
          -webkit-mask-size: 1000px 20px; mask-size: 1000px 20px;
          -webkit-mask-repeat: repeat-x; mask-repeat: repeat-x;
          z-index: 10;
        }
        .brush-edge-bottom { position: relative; }
        .brush-edge-bottom::after {
          content: ''; position: absolute; bottom: -19px; left: 50%; transform: translateX(-50%); width: 100vw; height: 20px;
          background-color: inherit;
          -webkit-mask-image: url('assets/brush.svg'); mask-image: url('assets/brush.svg');
          -webkit-mask-size: 1000px 20px; mask-size: 1000px 20px;
          -webkit-mask-repeat: repeat-x; mask-repeat: repeat-x;
          z-index: 10;
          transform: translateX(-50%) rotate(180deg);
        }
        .box-edge-top { position: relative; }
        .box-edge-top::before {
          content: ''; position: absolute; top: -19px; left: 0; width: 100%; height: 20px;
          background-color: inherit;
          -webkit-mask-image: url('assets/brush.svg'); mask-image: url('assets/brush.svg');
          -webkit-mask-size: 1000px 20px; mask-size: 1000px 20px;
          -webkit-mask-repeat: repeat-x; mask-repeat: repeat-x;
          z-index: 10;
        }
        .box-edge-bottom { position: relative; }
        .box-edge-bottom::after {
          content: ''; position: absolute; bottom: -19px; left: 0; width: 100%; height: 20px;
          background-color: inherit;
          -webkit-mask-image: url('assets/brush.svg'); mask-image: url('assets/brush.svg');
          -webkit-mask-size: 1000px 20px; mask-size: 1000px 20px;
          -webkit-mask-repeat: repeat-x; mask-repeat: repeat-x;
          z-index: 10;
          transform: rotate(180deg);
        }
        .hero-slide {
          position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center;
          opacity: 0;
          transform: scale(1);
          transition: opacity 1s ease-in-out, transform 8s linear;
        }
        .hero-slide.active {
          opacity: 1;
          transform: scale(1.1);
        }
      `
    }
  ]
})
