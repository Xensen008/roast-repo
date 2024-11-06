/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            color: '#fff',
            maxWidth: 'none',
            a: {
              color: '#fff',
              '&:hover': {
                color: '#d1d5db',
              },
            },
            h1: { color: '#fff' },
            h2: { color: '#fff' },
            h3: { color: '#fff' },
            h4: { color: '#fff' },
            strong: { color: '#fff' },
            code: {
              color: '#fff',
              backgroundColor: 'rgb(0 0 0 / 0.3)',
              padding: '0.25rem',
              borderRadius: '0.25rem',
              fontWeight: '400',
            },
            pre: {
              backgroundColor: 'rgb(0 0 0 / 0.5)',
              color: '#fff',
            },
            blockquote: {
              color: '#d1d5db',
              borderLeftColor: '#374151',
            },
            'code::before': {
              content: '""'
            },
            'code::after': {
              content: '""'
            }
          }
        }
      },
      animation: {
        'gradient': 'gradient 8s linear infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          },
        },
        glow: {
          '0%': { 'box-shadow': '0 0 20px -10px rgba(147, 51, 234, 0.5)' },
          '100%': { 'box-shadow': '0 0 20px 10px rgba(147, 51, 234, 0.5)' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}