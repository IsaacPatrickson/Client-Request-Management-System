// === Utility: Resize SVG to match viewport ===
function updateViewBoxToViewport(svg) {
    const width = window.innerWidth;
    const height = window.innerHeight;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
}

// === Easing Function (with optional delay at the beginning) ===
function easeInOutCubic(t) {
    const delay = 0.4; // 0.0–1.0 range for pause
    if (t < delay) return 0;
    t = (t - delay) / (1 - delay);
    return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// === DOM References ===
const svg = document.getElementById('pieces');
const polygon1 = document.getElementById('path1');
const polygon2 = document.getElementById('path2');

// === Animation State ===
let startTime = null;
const duration = 1400;
const delayPolygon2 = 300;

let currentPointsStart1 = [], currentPointsEnd1 = [];
let currentPointsStart2 = [], currentPointsEnd2 = [];

// === Helper Functions ===
function interpolatePoints(start, end, t) {
    return start.map((p, i) => [
        p[0] + (end[i][0] - p[0]) * t,
        p[1] + (end[i][1] - p[1]) * t
    ]);
}

function pointsToString(points) {
    return points.map(p => p.join(',')).join(' ');
}

// === Main Animation Loop ===
function animate(timestamp) {
    if (!startTime) startTime = timestamp;
    const elapsed = timestamp - startTime;
    const t = Math.min(elapsed / duration, 1);
    const easedT = easeInOutCubic(t);

    // Polygon 1 - Starts immediately
    const interpolated1 = interpolatePoints(currentPointsStart1, currentPointsEnd1, easedT);
    polygon1.setAttribute('points', pointsToString(interpolated1));

    // Polygon 2 - starts after delay
    let t2 = (elapsed - delayPolygon2) / duration;
    t2 = Math.max(0, Math.min(t2, 1));  // Clamp between 0 and 1
    const easedT2 = easeInOutCubic(t2);
    const interpolated2 = interpolatePoints(currentPointsStart2, currentPointsEnd2, easedT2);
    polygon2.setAttribute('points', pointsToString(interpolated2));

    if (elapsed < duration + delayPolygon2) {
        requestAnimationFrame(animate);
    }
}

// === Setup Animation on Load ===
function setupAndAnimate() {
    startTime = null;
    const width = window.innerWidth;
    const height = window.innerHeight;
    updateViewBoxToViewport(svg);

    currentPointsStart1 = [
        [0, 0],
        [900, 550],
        [900, 550],
        [350, height],
        [0, height]
    ];

    currentPointsEnd1 = [
        [0, 0],
        [width, height],
        [width, height],
        [width, height],
        [0, height]
    ];

    currentPointsStart2 = [
        [0, 0],
        [450, 248],
        [1000, 550],
        [1000, 550],
        [400, height],
        [0, height]
    ];

    currentPointsEnd2 = [
        [0, 0],
        [width * 0.2, 0],
        [width * 0.75, height],
        [width * 0.75, height],
        [width * 0.75, height],
        [0, height]
    ];

    polygon1.setAttribute('points', pointsToString(currentPointsStart1));
    polygon2.setAttribute('points', pointsToString(currentPointsStart2));

    requestAnimationFrame(animate);
}

// === Animate Again on Resize ===
function animateOnResize() {
    startTime = null;
    const width = window.innerWidth;
    const height = window.innerHeight;
    updateViewBoxToViewport(svg);

    const parsePoints = el =>
        el.getAttribute('points')
            .trim()
            .split(' ')
            .map(pt => pt.split(',').map(Number));

    currentPointsStart1 = parsePoints(polygon1);
    currentPointsStart2 = parsePoints(polygon2);

    currentPointsEnd1 = [
        [0, 0],
        [width, height],
        [width, height],
        [width * 0.4, height],
        [0, height]
    ];

    currentPointsEnd2 = [
        [0, 0],
        [width * 0.2, 0],
        [width * 0.75, height],
        [width * 0.75, height],
        [width * 0.75, height],
        [0, height]
    ];

    requestAnimationFrame(animate);
}

// === Event Listeners ===
window.addEventListener('load', setupAndAnimate);
window.addEventListener('resize', animateOnResize);
