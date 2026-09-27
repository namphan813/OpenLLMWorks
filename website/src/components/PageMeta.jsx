import { useEffect } from "react";


const SITE_URL = "https://openllmworks.com";


function setMetaContent(selector, content) {
    const element = document.querySelector(selector);

    if (element) {
        element.setAttribute("content", content);
    }
}


function PageMeta({
    title,
    description,
    canonical,
}) {
    useEffect(() => {
        const canonicalUrl =
            `${SITE_URL}${canonical}`;

        document.title = title;

        setMetaContent(
            'meta[name="description"]',
            description,
        );

        setMetaContent(
            'meta[property="og:title"]',
            title,
        );

        setMetaContent(
            'meta[property="og:description"]',
            description,
        );

        setMetaContent(
            'meta[property="og:url"]',
            canonicalUrl,
        );

        setMetaContent(
            'meta[name="twitter:title"]',
            title,
        );

        setMetaContent(
            'meta[name="twitter:description"]',
            description,
        );

        const canonicalElement =
            document.querySelector(
                'link[rel="canonical"]',
            );

        if (canonicalElement) {
            canonicalElement.setAttribute(
                "href",
                canonicalUrl,
            );
        }
    }, [
        title,
        description,
        canonical,
    ]);

    return null;
}


export default PageMeta;