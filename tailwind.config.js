// tailwind.config.js
module.exports = {
  content: ['./templates/**/*.html', './app/**/*.js'], // Ensure this points to your HTML and JS files
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
};
