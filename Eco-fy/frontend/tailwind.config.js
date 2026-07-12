/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: '#fdf7ff',
        'surface-dim': '#ded8e0',
        'surface-bright': '#fdf7ff',
        'surface-container-lowest': '#ffffff',
        'surface-container-low': '#f8f2fa',
        'surface-container': '#f2ecf4',
        'surface-container-high': '#ece6ee',
        'surface-container-highest': '#e6e0e9',
        'on-surface': '#1d1b20',
        'on-surface-variant': '#494551',
        'inverse-surface': '#322f35',
        'inverse-on-surface': '#f5eff7',
        outline: '#7a7582',
        'outline-variant': '#cbc4d2',
        'surface-tint': '#6750a4',
        primary: '#4f378a',
        'on-primary': '#ffffff',
        'primary-container': '#6750a4',
        'on-primary-container': '#e0d2ff',
        'inverse-primary': '#cfbcff',
        secondary: '#63597c',
        'on-secondary': '#ffffff',
        'secondary-container': '#e1d4fd',
        'on-secondary-container': '#645a7d',
        tertiary: '#765b00',
        'on-tertiary': '#ffffff',
        'tertiary-container': '#c9a74d',
        'on-tertiary-container': '#503d00',
        error: '#ba1a1a',
        'on-error': '#ffffff',
        'error-container': '#ffdad6',
        'on-error-container': '#93000a',
        background: '#fdf7ff',
        'on-background': '#1d1b20',
        
        // Brand & Style accents
        'brand-green': '#355C4D',
        'brand-olive': '#7A8B68',
        'brand-sand': '#D8C7A3',
        'canvas': '#F6F6F3',
        'sidebar': '#ECEBE7',
        'border-color': '#E3E4E6'
      },
      fontFamily: {
        sans: ['"Hanken Grotesk"', 'sans-serif'],
      },
      borderRadius: {
        'button': '12px',
        'card': '18px',
        'input': '8px',
      },
      spacing: {
        'base': '4px',
        'xs': '8px',
        'sm': '12px',
        'md': '24px',
        'lg': '40px',
        'xl': '64px',
      }
    },
  },
  plugins: [],
}
