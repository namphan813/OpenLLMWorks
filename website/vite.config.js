import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],

    // Serve the Publisher's generated output as the website's public data.
    publicDir: "../database/generated",
});