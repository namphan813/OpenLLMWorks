import {
    readFileSync,
    writeFileSync,
} from "node:fs";

import {
    resolve,
} from "node:path";

import {
    getPublicWorksArticles,
} from "../src/content/works/articles.js";


const SITE_URL = "https://openllmworks.com";

const coreRoutes = [
    "/",
    "/hardware",
    "/compare",
    "/methodology",
    "/works",
];


function buildUrl(path) {
    return `${SITE_URL}${path}`;
}


function buildUrlEntry(url) {
    return [
        "    <url>",
        `        <loc>${url}</loc>`,
        "    </url>",
    ].join("\n");
}


const hardwarePath = resolve(
    "../database/generated/hardware.json",
);

const sitemapPath = resolve(
    "dist/sitemap.xml",
);

const hardwareData = JSON.parse(
    readFileSync(hardwarePath, "utf8"),
);

const hardwareRoutes = hardwareData.hardware.map(
    (hardware) => `/hardware/${hardware.variantId}`,
);

const worksRoutes = getPublicWorksArticles().map(
    (article) => `/works/${article.slug}`,
);

const routes = [
    ...coreRoutes,
    ...hardwareRoutes,
    ...worksRoutes,
];

const uniqueRoutes = [...new Set(routes)];

const sitemap = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...uniqueRoutes.map(
        (route) => buildUrlEntry(buildUrl(route)),
    ),
    "</urlset>",
    "",
].join("\n");

writeFileSync(
    sitemapPath,
    sitemap,
    "utf8",
);

console.log(
    `Generated sitemap with ${uniqueRoutes.length} URLs.`,
);