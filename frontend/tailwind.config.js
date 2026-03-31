/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: "#0d0d1a",
        card: "#13131f",
        border: "#1e1e3a",
        accent: "#6c63ff",
        teal: "#3ecfcf",
      },
    },
  },
  plugins: [],
}