function generateLayerPanel() {
    const layerList = document.querySelector('.layer-list');
    const svgElement = document.querySelector('.zoom-layer svg');
    layerList.innerHTML = '';
    const mainContainer = svgElement.querySelector('g');
    if (!mainContainer) {console.error("Ошибка: Главный <g> внутри <svg> не найден!");return;}
    const layers = mainContainer.querySelectorAll(':scope > g');
    layers.forEach((layer, index) => {
        const layerNumber = index + 1;
        const layerDisplayName = (layer.className.baseVal || layer.getAttribute('class')).match(/\S+/)?.[0] || 'NoName';
        const targetForStyle = layer.querySelector('path, rect, circle, polygon, text, use') || layer;
        const computedStyle = window.getComputedStyle(targetForStyle);
        const hexColor = rgbToHex(computedStyle.fill) || '#ffffff';
        const isVisible = (computedStyle.display !== 'none') ? 'active' : '';
        const row = document.createElement('div');
        row.className = 'layer-row';
        row.innerHTML = `<input type="color" class="layer-color-input" value="${hexColor}">
            <div class="layer-visible ${isVisible}"></div>
            <div class="layer-up" title="Move Up">▲</div>
            <div class="layer-down" title="Move Down">▼</div>
            <div class="layer-name">${layerDisplayName}</div>
            <div class="layer-delete">×</div>`;
        row.querySelector('.layer-color-input').addEventListener('input', (e) => {
            const newColor = e.target.value;
            layer.style.fill = newColor;
        });
        row.querySelector('.layer-visible').addEventListener('click', (e) => {
            const isNowVisible = e.target.classList.toggle('active');
            layer.style.display = isNowVisible ? 'inline' : 'none';
        });
        row.querySelector('.layer-delete').addEventListener('click', () => {
            layer.remove();
            row.remove();
        });
        row.querySelector('.layer-up').addEventListener('click', () => {
            const nextLayer = layer.nextElementSibling;
            const prevRow = row.previousElementSibling;
            if (nextLayer && prevRow) {
                nextLayer.after(layer);
                prevRow.before(row);
            }
        });
        row.querySelector('.layer-down').addEventListener('click', () => {
            const prevLayer = layer.previousElementSibling;
            const nextRow = row.nextElementSibling;
            if (prevLayer && nextRow) {
                prevLayer.before(layer);
                nextRow.after(row);
            }
        });
        layerList.prepend(row);
    });
}
function rgbToHex(rgbString) {
    if (!rgbString || rgbString === 'none') return '#ffffff';
    if (rgbString.startsWith('#')) return rgbString;
    const match = rgbString.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    if (!match) return '#ffffff';
    const r = parseInt(match[1], 10).toString(16).padStart(2, '0');
    const g = parseInt(match[2], 10).toString(16).padStart(2, '0');
    const b = parseInt(match[3], 10).toString(16).padStart(2, '0');
    return `#${r}${g}${b}`;
}
window.addEventListener("svg-loaded", generateLayerPanel);
if (document.querySelector(".zoom-layer svg")) {generateLayerPanel();}