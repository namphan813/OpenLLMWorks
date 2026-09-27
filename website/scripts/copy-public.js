import {
    cpSync,
    existsSync,
} from "node:fs";

import {
    resolve,
} from "node:path";


const publicDir = resolve("public");
const distDir = resolve("dist");


if (existsSync(publicDir)) {
    cpSync(
        publicDir,
        distDir,
        {
            recursive: true,
            force: true,
        },
    );
}