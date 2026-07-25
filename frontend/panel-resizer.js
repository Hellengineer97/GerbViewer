function initPanelResizers() {
    const leftPanel = document.querySelector(".panel-left");
    const rightPanel = document.querySelector(".panel-right");

    if (leftPanel) setupResizer(leftPanel, "right");
    if (rightPanel) setupResizer(rightPanel, "left");
}

function setupResizer(panel, direction) {
    const resizer = panel.querySelector(`.resizer-${direction}`);
    if (!resizer) return;
    resizer.addEventListener("mousedown", (event) => {
        event.preventDefault();
        resizer.classList.add("dragging");
        const startWidth = panel.getBoundingClientRect().width;
        const startX = event.clientX;
        function onMouseMove(moveEvent) {
            const deltaX = moveEvent.clientX - startX;
            let newWidth;
            if (direction === "right") {
                newWidth = startWidth + deltaX;
            } else {
                newWidth = startWidth - deltaX;
            }
            panel.style.width = `${newWidth}px`;
        }
        function onMouseUp() {
            resizer.classList.remove("dragging");
            window.removeEventListener("mousemove", onMouseMove);
            window.removeEventListener("mouseup", onMouseUp);
        }
        window.addEventListener("mousemove", onMouseMove);
        window.addEventListener("mouseup", onMouseUp);
    });
}
window.addEventListener("load", initPanelResizers);
