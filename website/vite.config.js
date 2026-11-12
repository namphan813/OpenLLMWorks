import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

import { createReadStream, existsSync, statSync } from "node:fs";
import { extname, resolve, sep } from "node:path";

function serveWebsitePublic() {
    const publicRoot = resolve(import.meta.dirname, "public");

    const contentTypes = {
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".png": "image/png",
        ".webp": "image/webp",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".txt": "text/plain; charset=utf-8",
        ".xml": "application/xml",
    };

    return {
        name: "serve-website-public",
        apply: "serve",

        configureServer(server) {
            server.middlewares.use((req, res, next) => {
                if (req.method !== "GET" && req.method !== "HEAD") {
                    return next();
                }

                let pathname;

                try {
                    pathname = decodeURIComponent(
                        new URL(req.url, "http://localhost").pathname,
                    );
                } catch {
                    return next();
                }

                const filePath = resolve(publicRoot, "." + pathname);

                if (
                    filePath !== publicRoot &&
                    !filePath.startsWith(publicRoot + sep)
                ) {
                    return next();
                }

                if (!existsSync(filePath) || !statSync(filePath).isFile()) {
                    return next();
                }

                res.setHeader(
                    "Content-Type",
                    contentTypes[extname(filePath).toLowerCase()] ??
                        "application/octet-stream",
                );

                if (req.method === "HEAD") {
                    res.end();
                    return;
                }

                createReadStream(filePath).pipe(res);
            });
        },
    };
}

export default defineConfig({
    plugins: [
        react(),
        serveWebsitePublic(),
    ],

    // Serve the Publisher's generated output as the website's public data.
    publicDir: "../database/generated",
});
