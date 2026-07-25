function initSVGUpLoader() {
    const uploadBtn = document.getElementById("upload-btn");
    const fileInput = document.getElementById("svg-upload-input");
    const zoomLayerEl = document.querySelector(".zoom-layer");
    if (!uploadBtn || !fileInput || !zoomLayerEl) return;
    uploadBtn.addEventListener("click", () => {
        fileInput.click();
    });
    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (processEvent) => {
            zoomLayerEl.innerHTML = processEvent.target.result;
            window.dispatchEvent(new Event("svg-loaded"));
        };
        reader.readAsText(file);
    });
}
document.addEventListener("DOMContentLoaded", initSVGUpLoader);
