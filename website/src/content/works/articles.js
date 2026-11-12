const worksArticles = {
    "runner-v0-4-2-amd-vulkan-support": {
        slug: "runner-v0-4-2-amd-vulkan-support",
        type: "Development Update",
        status: "Published",
        visibility: "public",
        featured: false,
        title: "OpenLLMWorks Runner v0.4.2: Expanding GPU Benchmarking Beyond NVIDIA",
        description:
            "Runner v0.4.2-beta.1 introduces experimental AMD/Vulkan support " +
            "and expands OpenLLMWorks beyond NVIDIA/CUDA benchmarking.",
        question:
            "How does Runner v0.4.2-beta.1 expand GPU compatibility?",
        sections: [
            {
                heading: "A new milestone for OpenLLMWorks",
                paragraphs: [
                    "Released November 12, 2026, OpenLLMWorks Runner " +
                        "v0.4.2-beta.1 introduces experimental AMD GPU " +
                        "support through Vulkan.",
                    "Until now, OpenLLMWorks Runner primarily focused " +
                        "on NVIDIA GPUs using CUDA. This release marks " +
                        "our first step toward supporting a broader " +
                        "range of graphics hardware.",
                ],
            },
            {
                heading: "Our first validated AMD GPU",
                paragraphs: [
                    "The AMD Radeon RX 6700 XT is the first AMD GPU " +
                        "validated using the packaged Windows Runner.",
                    "Testing covered Vulkan device detection and " +
                        "selection, benchmark asset verification, " +
                        "three benchmark runs, result validation, " +
                        "and submission ZIP packaging.",
                    "RX 6700 XT benchmark results have also been " +
                        "published through the OpenLLMWorks " +
                        "submission pipeline and are available " +
                        "on the public leaderboards.",
                ],
            },
            {
                heading: "One protocol, multiple backends",
                paragraphs: [
                    "Runner v0.4.2-beta.1 introduces multi-backend " +
                        "accelerator detection and selection, allowing " +
                        "users to identify the GPU and backend intended " +
                        "for benchmarking.",
                    "Benchmark Protocol v1.0 remains unchanged. " +
                        "The standardized Qwen3-4B-Q4_K_M workload, " +
                        "PP512 and TG128 measurements, and three-run " +
                        "averaging methodology continue to provide " +
                        "a consistent basis for hardware comparisons.",
                    "Using the same protocol across backends helps " +
                        "preserve methodological consistency, although " +
                        "backend implementations and drivers can also " +
                        "influence observed performance.",
                ],
            },
            {
                heading: "NVIDIA compatibility remains intact",
                paragraphs: [
                    "The packaged v0.4.2-beta.1 Windows executable " +
                        "also completed end-to-end validation on an " +
                        "NVIDIA RTX A3000 Laptop GPU using CUDA.",
                    "This confirms that the existing NVIDIA " +
                        "benchmarking workflow continues to operate " +
                        "alongside the new experimental Vulkan backend.",
                ],
            },
            {
                heading: "What's next for GPU compatibility?",
                paragraphs: [
                    "AMD/Vulkan support remains experimental. " +
                        "Although the Radeon RX 6700 XT has passed " +
                        "validation, broader AMD GPU coverage " +
                        "requires additional testing.",
                    "Intel/Vulkan compatibility is also under " +
                        "investigation. Intel graphics devices may " +
                        "appear during accelerator detection, but " +
                        "successful benchmarking has not yet been " +
                        "validated.",
                    "Future development will focus on expanding " +
                        "hardware coverage, refining GPU identification, " +
                        "and improving benchmark evidence and telemetry.",
                ],
            },
            {
                heading: "Download Runner v0.4.2-beta.1",
                paragraphs: [
                    "The Windows Runner is available from the " +
                        "OpenLLMWorks GitHub Releases page. Visit " +
                        "https://github.com/namphan813/OpenLLMWorks/releases/tag/v0.4.2-beta.1 " +
                        "to download the executable and review the " +
                        "release notes.",
                ],
            },
        ],
        note: {
            heading: "Experimental backend support",
            body:
                "NVIDIA/CUDA remains supported and validated. " +
                "AMD/Vulkan is experimental and currently validated " +
                "on the Radeon RX 6700 XT. Intel/Vulkan remains " +
                "unvalidated.",
        },
    },
    "runner-v0-4-1-windows-compatibility": {
        slug: "runner-v0-4-1-windows-compatibility",
        type: "Development Update",
        status: "Published",
        visibility: "public",
        featured: false,
        title: "OpenLLMWorks Runner v0.4.1: Improving Windows Compatibility",
        description:
            "Runner v0.4.1-beta.1 improves Windows HTTPS compatibility, " +
            "console usability, and hardware reporting.",
        question:
            "What's new in Runner v0.4.1-beta.1, and how was the " +
            "release validated?",
        sections: [
            {
                heading: "Improving Windows download reliability",
                image: "/images/works/runner-https-certificate-error.png",
                imageAlt:
                    "OpenLLMWorks Runner showing an HTTPS certificate " +
                    "verification failure while downloading CUDA dependencies.",
                caption:
                    "Earlier Runner build: HTTPS certificate verification " +
                    "prevented CUDA runtime provisioning and stopped the benchmark.",
                paragraphs: [
                    "OpenLLMWorks Runner v0.4.1-beta.1 is a maintenance " +
                        "release focused on improving the Windows " +
                        "benchmarking experience.",
                    "During testing, we identified an HTTPS certificate " +
                        "verification issue that could prevent the " +
                        "standalone Runner from downloading its CUDA " +
                        "runtime dependencies. The Runner now uses " +
                        "improved Windows certificate trust handling " +
                        "to address the observed failure.",
                ],
            },
            {
                heading: "A clearer benchmarking experience",
                paragraphs: [
                    "This release also improves console readability, " +
                        "progress reporting, and hardware metadata " +
                        "collection. Additional system, memory, and " +
                        "graphics hardware information provides more " +
                        "context for interpreting benchmark results.",
                    "Benchmark Protocol v1.0 remains unchanged, " +
                        "preserving comparability with previously " +
                        "published results.",
                ],
            },
            {
                heading: "Validated from download to leaderboard",
                paragraphs: [
                    "We tested the publicly released Windows " +
                        "executable on an NVIDIA GeForce RTX 4060 " +
                        "Laptop GPU. The downloaded executable's " +
                        "SHA-256 checksum matched the locally " +
                        "validated build.",
                    "The Runner completed both benchmark workloads, " +
                        "uploaded its submission, passed validation, " +
                        "and progressed through maintainer approval " +
                        "to publication on the public OpenLLMWorks " +
                        "leaderboard.",
                    "This end-to-end test verifies more than a " +
                        "successful benchmark run: it demonstrates " +
                        "the production submission and publication " +
                        "workflow using the released Runner.",
                ],
            },
            {
                heading: "Get Runner v0.4.1-beta.1",
                paragraphs: [
                    "The latest beta release is available through " +
                        "the Download Runner link in the OpenLLMWorks " +
                        "website navigation. Development continues " +
                        "as we expand hardware coverage and improve " +
                        "the benchmarking platform.",
                ],
            },
        ],
    },
    "how-far-back-can-modern-local-ai-go": {
        slug: "how-far-back-can-modern-local-ai-go",
        type: "Experiment",
        status: "In Progress",
        visibility: "private",
        featured: true,
        title: "How far back can modern local AI go?",
        description:
            "An OpenLLMWorks experiment exploring how older " +
            "consumer GPUs handle a modern local AI workload.",
        question:
            "How useful is older hardware for running a modern " +
            "local AI workload, and where does performance begin " +
            "to break down?",
        sections: [
            {
                heading: "Why we're testing this",
                paragraphs: [
                    "Local AI hardware discussions tend to focus " +
                        "on current GPUs. OpenLLMWorks is also " +
                        "interested in the hardware people already " +
                        "own, including older consumer cards that " +
                        "predate today's local AI ecosystem.",
                    "This experiment will use the standard " +
                        "OpenLLMWorks benchmark protocol to examine " +
                        "how far back modern local AI workloads " +
                        "remain practical.",
                ],
            },
            {
                heading: "What we're measuring",
                paragraphs: [
                    "Results will be grounded in validated " +
                        "OpenLLMWorks benchmark data, including " +
                        "prompt processing and token generation " +
                        "performance under the frozen benchmark " +
                        "methodology.",
                ],
            },
        ],
        note: {
            heading: "Experiment in progress",
            body:
                "This article framework is live while the " +
                "underlying experiment is still being developed. " +
                "Findings will be added only after supporting " +
                "benchmark results have been validated and " +
                "published.",
        },
    },

    "what-do-pp512-and-tg128-mean": {
        slug: "what-do-pp512-and-tg128-mean",
        type: "Research Note",
        status: "Published",
        visibility: "public",
        featured: false,
        title: "What do PP512 and TG128 actually mean?",
        description:
            "Understanding the two performance measurements behind " +
            "an OpenLLMWorks local AI benchmark.",
        question:
            "What do PP512 and TG128 measure, and how do those " +
            "numbers translate into the experience of using a " +
            "local language model?",
        summary: {
            heading: "The short version",
            intro:
                "OpenLLMWorks measures two different parts of a " +
                "local AI workload. A simple way to think about " +
                "them is reading versus writing.",
            items: [
                {
                    label: "PP512",
                    title: "Prompt Processing",
                    body:
                        "How quickly the system processes the " +
                        "information you give the model. Think of " +
                        "it as how quickly the model can read its " +
                        "input.",
                },
                {
                    label: "TG128",
                    title: "Token Generation",
                    body:
                        "How quickly the system generates new " +
                        "output. Think of it as how quickly the " +
                        "model can write its response.",
                },
            ],
        },
        sections: [
            {
                heading: "Two numbers, two parts of the experience",
                paragraphs: [
                    "Gaming benchmarks have an advantage: most " +
                        "people already have an intuitive sense of " +
                        "what frame rate means. The difference " +
                        "between 30, 60, and 120 frames per second " +
                        "can be connected to an experience people " +
                        "have actually seen and felt.",
                    "Local AI performance is commonly measured in " +
                        "tokens per second, but that number can be " +
                        "less intuitive. It also hides an important " +
                        "detail: using a language model involves " +
                        "more than one kind of work.",
                    "OpenLLMWorks measures two of those phases " +
                        "separately. PP512 represents prompt " +
                        "processing performance, while TG128 " +
                        "represents token generation performance.",
                ],
            },
            {
                heading: "PP512: processing what you give the model",
                paragraphs: [
                    "PP512 measures prompt processing using a " +
                        "512-token input. This is the work the model " +
                        "does to process the context it has been " +
                        "given before producing new output.",
                    "In practical use, this phase matters when you " +
                        "paste text into a chat, provide a document " +
                        "for analysis, include conversation history, " +
                        "or otherwise give the model context that it " +
                        "needs to process.",
                    "A higher PP512 result means the benchmarked " +
                        "system processed that fixed prompt workload " +
                        "at a higher token rate. It does not tell us " +
                        "how quickly the model will generate its " +
                        "answer. That is what the second measurement " +
                        "is for.",
                ],
            },
            {
                heading: "TG128: generating what the model gives back",
                paragraphs: [
                    "TG128 measures token generation while the model " +
                        "produces 128 new tokens. This is the phase " +
                        "that most directly resembles watching an " +
                        "AI response appear on screen.",
                    "When generation performance is low, individual " +
                        "tokens arrive more slowly. As the rate " +
                        "increases, responses appear more quickly " +
                        "and interaction can feel more immediate.",
                    "A higher TG128 result therefore means the " +
                        "benchmarked system generated the fixed " +
                        "output workload at a higher token rate. It " +
                        "does not describe how quickly a large input " +
                        "was processed before generation began.",
                ],
            },
            {
                heading: "Why one score is not enough",
                paragraphs: [
                    "Prompt processing and token generation are " +
                        "different workloads. A GPU can perform " +
                        "relatively well in one phase without showing " +
                        "the same advantage in the other.",
                    "That is why OpenLLMWorks publishes PP512 and " +
                        "TG128 separately instead of combining them " +
                        "into a single performance score. A combined " +
                        "number would be simpler, but it could hide " +
                        "differences that affect how a system behaves " +
                        "during real use.",
                    "Two GPUs with similar overall impressions on " +
                        "paper can therefore produce different " +
                        "experiences depending on how much time a " +
                        "workload spends processing input versus " +
                        "generating output.",
                ],
            },
            {
                heading: "From benchmark numbers to real-world use",
                paragraphs: [
                    "PP512 and TG128 are controlled measurements, " +
                        "not universal predictions of application " +
                        "speed. Real workloads vary in prompt length, " +
                        "output length, model configuration, software " +
                        "stack, available memory, and other factors.",
                    "Their value is consistency. By running the same " +
                        "workload under the same OpenLLMWorks " +
                        "protocol, we can compare hardware using a " +
                        "common reference point.",
                    "As the OpenLLMWorks dataset grows, we can use " +
                        "those measurements alongside representative " +
                        "real-world scenarios to better understand " +
                        "what different performance ranges actually " +
                        "feel like.",
                ],
            },
        ],
        note: {
            heading: "A benchmark is a reference point",
            body:
                "OpenLLMWorks uses PP512 and TG128 to make hardware " +
                "comparisons reproducible. They should be read as " +
                "two complementary measurements of a local AI " +
                "workload rather than a single verdict on whether " +
                "a GPU is good or bad.",
        },
    },
};


export function getWorksArticle(slug) {
    return worksArticles[slug] ?? null;
}


export function getWorksArticles() {
    return Object.values(worksArticles);
}


export function getPublicWorksArticles() {
    return getWorksArticles().filter(
        (article) => article.visibility === "public",
    );
}


export function getFeaturedWorksArticle() {
    return (
        getWorksArticles().find(
            (article) => article.featured,
        ) ?? null
    );
}


export default worksArticles;
