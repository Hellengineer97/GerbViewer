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
                // Форсируем перекомпозицию GPU-слоя в WebKit/Blink,
                // иначе растр не перерисовывается после зума
                const currentStyle = zoomLayer.style("transform");
                zoomLayer.style("transform", currentStyle + " translateZ(0.001px)");
            }, 200);
        });

    container.call(zoomBehavior);
}

window.addEventListener("svg-loaded", initPanZoom);

if (document.querySelector(".zoom-layer svg")) {
    initPanZoom();
}