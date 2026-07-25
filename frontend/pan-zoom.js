import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

let container, zoomLayer, zoomBehavior, debounceTimer;

function initPanZoom() {
    container = d3.select("#canvas-container");
    zoomLayer = d3.select(".zoom-layer");
    zoomBehavior = d3.zoom()
        .scaleExtent([0.1, 100])
        .on("start", () => {
            zoomLayer.style("will-change", "transform");
            clearTimeout(debounceTimer);
        })
        .on("zoom", (event) => {
            zoomLayer.style("transform", `translate(${event.transform.x}px, ${event.transform.y}px) scale(${event.transform.k})`);
        })
        .on("end", () => {
            debounceTimer = setTimeout(() => {
                zoomLayer.style("will-change", "auto");
                const currentStyle = zoomLayer.style("transform");
                zoomLayer.style("transform", currentStyle + " translateZ(0.001px)");
            }, 200);
        });
    container.call(zoomBehavior);
    centerView();
}
function centerView() {
    const containerEl = document.getElementById("canvas-container");
    const svgElement = document.querySelector(".zoom-layer svg");

    if (!containerEl || !svgElement) return;

    const width = containerEl.clientWidth;
    const height = containerEl.clientHeight;

    const viewBox = svgElement.viewBox.baseVal;
    const boardWidth = viewBox.width || 400;
    const boardHeight = viewBox.height || 300;

    const scale = 0.85 / Math.max(boardWidth / width, boardHeight / height);
    const translateX = (width - boardWidth * scale) / 2;
    const translateY = (height - boardHeight * scale) / 2;
}
window.addEventListener("svg-loaded", initPanZoom);
window.addEventListener("resize", () => {
    if (container) centerView();
});
if (document.querySelector(".zoom-layer svg")) {initPanZoom();}