import {
    motion,
    useMotionValue,
    useReducedMotion,
    useSpring,
    useTransform,
} from "motion/react";
import { Link } from "react-router-dom";


const nodes = [
    { x: 10, y: 30, delay: 0.05, strength: 8 },
    { x: 22, y: 68, delay: 0.12, strength: 12 },
    { x: 36, y: 22, delay: 0.19, strength: 10 },
    { x: 48, y: 57, delay: 0.26, strength: 14 },
    { x: 63, y: 31, delay: 0.33, strength: 11 },
    { x: 75, y: 70, delay: 0.4, strength: 13 },
    { x: 88, y: 40, delay: 0.47, strength: 9 },
];


function DataNode({
    node,
    index,
    pointerX,
    pointerY,
    reducedMotion,
}) {
    const offsetX = useTransform(
        pointerX,
        [-1, 0, 1],
        reducedMotion
            ? [0, 0, 0]
            : [-node.strength, 0, node.strength],
    );

    const offsetY = useTransform(
        pointerY,
        [-1, 0, 1],
        reducedMotion
            ? [0, 0, 0]
            : [-node.strength, 0, node.strength],
    );

    const x = useSpring(offsetX, {
        stiffness: 90,
        damping: 18,
    });

    const y = useSpring(offsetY, {
        stiffness: 90,
        damping: 18,
    });

    return (
        <motion.span
            className="works-not-found-node"
            style={{
                left: `${node.x}%`,
                top: `${node.y}%`,
                x,
                y,
            }}
            initial={{
                opacity: 0,
                scale: 0,
            }}
            animate={{
                opacity: 1,
                scale: 1,
            }}
            transition={{
                delay: node.delay,
                duration: 0.35,
            }}
        />
    );
}


function WorksNotFound() {
    const reducedMotion = useReducedMotion();

    const pointerX = useMotionValue(0);
    const pointerY = useMotionValue(0);

    const lostOffsetX = useTransform(
        pointerX,
        [-1, 0, 1],
        reducedMotion ? [0, 0, 0] : [-24, 0, 24],
    );

    const lostOffsetY = useTransform(
        pointerY,
        [-1, 0, 1],
        reducedMotion ? [0, 0, 0] : [-20, 0, 20],
    );

    const lostX = useSpring(lostOffsetX, {
        stiffness: 75,
        damping: 16,
    });

    const lostY = useSpring(lostOffsetY, {
        stiffness: 75,
        damping: 16,
    });

    function handlePointerMove(event) {
        if (reducedMotion) {
            return;
        }

        const bounds =
            event.currentTarget.getBoundingClientRect();

        const x =
            ((event.clientX - bounds.left) /
                bounds.width) *
                2 -
            1;

        const y =
            ((event.clientY - bounds.top) /
                bounds.height) *
                2 -
            1;

        pointerX.set(x);
        pointerY.set(y);
    }

    function handlePointerLeave() {
        pointerX.set(0);
        pointerY.set(0);
    }

    return (
        <div className="works-not-found">
            <motion.div
                className="works-not-found-visual"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
                onPointerMove={handlePointerMove}
                onPointerLeave={handlePointerLeave}
                aria-hidden="true"
            >
                <div className="works-not-found-grid" />

                {nodes.map((node, index) => (
                    <DataNode
                        key={index}
                        node={node}
                        index={index}
                        pointerX={pointerX}
                        pointerY={pointerY}
                        reducedMotion={reducedMotion}
                    />
                ))}

                <motion.span
                    className={
                        "works-not-found-node " +
                        "works-not-found-node--lost"
                    }
                    style={{
                        x: lostX,
                        y: lostY,
                    }}
                    initial={{
                        opacity: 0,
                        scale: 0,
                    }}
                    animate={{
                        opacity: 1,
                        scale: reducedMotion
                            ? 1
                            : [1, 1.35, 1],
                    }}
                    transition={{
                        opacity: {
                            delay: 0.6,
                            duration: 0.35,
                        },
                        scale: {
                            delay: 0.9,
                            duration: 2.4,
                            repeat: reducedMotion
                                ? 0
                                : Infinity,
                            ease: "easeInOut",
                        },
                    }}
                />
            </motion.div>

            <motion.div
                className="works-not-found-content"
                initial={{
                    opacity: 0,
                    y: reducedMotion ? 0 : 18,
                }}
                animate={{
                    opacity: 1,
                    y: 0,
                }}
                transition={{
                    delay: 0.25,
                    duration: 0.5,
                    ease: [0.22, 1, 0.36, 1],
                }}
            >
                <p className="works-eyebrow">
                    404 / RESULT NOT FOUND
                </p>

                <h1>
                    This experiment wandered outside the dataset.
                </h1>

                <p>
                    The Works entry you're looking for doesn't
                    exist, hasn't been published yet, or is still
                    somewhere in the lab.
                </p>

                <div className="works-not-found-actions">
                    <Link
                        className="works-not-found-primary"
                        to="/works"
                    >
                        ← Return to The Works
                    </Link>

                    <Link
                        className="works-not-found-secondary"
                        to="/hardware"
                    >
                        Browse Hardware
                    </Link>
                </div>
            </motion.div>
        </div>
    );
}


export default WorksNotFound;