/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./django/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
    "./django/**/forms.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("flowbite/plugin")],
};
