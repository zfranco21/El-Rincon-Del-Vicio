/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.html"],
    theme: {
    screens: {

      'celu': {'min': '100px', 'max': '640px'},

      'tablet': {'min': '640px', 'max': '1024px'},
      // => @media (min-width: 640px) { ... }

      'pc': {'min': '1000px', 'max': '1280px'},
      // => @media (min-width: 1024px) { ... }

      'tv': {'min': '1280px', 'max': '2500px'},
      // => @media (min-width: 1280px) { ... }
    },
    extend: {},
  },
  plugins: [],
}