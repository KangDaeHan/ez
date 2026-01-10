/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef7ee',
          100: '#fdedd6',
          200: '#f9d7ac',
          300: '#f5ba78',
          400: '#f09442',
          500: '#ec771d',
          600: '#dd5c13',
          700: '#b74512',
          800: '#923817',
          900: '#763016',
          950: '#401609',
        },
        secondary: {
          50: '#f6f7f9',
          100: '#eceef2',
          200: '#d5dae2',
          300: '#b1bac9',
          400: '#8795ab',
          500: '#687890',
          600: '#536077',
          700: '#444e61',
          800: '#3b4352',
          900: '#343a46',
          950: '#23272f',
        },
        accent: {
          50: '#eefbf4',
          100: '#d6f5e3',
          200: '#b0eacb',
          300: '#7dd9ad',
          400: '#48c18a',
          500: '#26a66e',
          600: '#188658',
          700: '#146b49',
          800: '#13553b',
          900: '#114632',
          950: '#08271c',
        },
      },
      fontFamily: {
        sans: ['Pretendard', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        'widget': '1rem',
        'widget-lg': '1.5rem',
      },
      boxShadow: {
        'widget': '0 4px 20px -2px rgba(0, 0, 0, 0.1)',
        'widget-hover': '0 8px 30px -4px rgba(0, 0, 0, 0.15)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
    },
  },
  plugins: [],
}

