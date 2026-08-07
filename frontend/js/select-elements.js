let selectedNets = new Set();

function getOrCreateHighlightLayer(svgMain) {
    if (!svgMain) return null;
    const transformGroup = svgMain.querySelector('g[transform^="matrix"]');
    if (!transformGroup) return null;
    let layer = transformGroup.querySelector('#selected-items');
    if (!layer) {
        const styles = 'pointer-events: none; fill: #ff7300; stroke: red; stroke-width: 0.1px;';
        transformGroup.insertAdjacentHTML('beforeend', `<g id="selected-items" style="${styles}"></g>`);
        layer = transformGroup.querySelector('#selected-items');
    }
    return layer;
}
function updateHighlights() {
    const svgMain = document.querySelector('svg');
    const highlightLayer = getOrCreateHighlightLayer(svgMain);
    if (highlightLayer) {
        highlightLayer.innerHTML = '';
    }
    if (selectedNets.size === 0) return;
    selectedNets.forEach(netClass => {
        const originalElements = document.querySelectorAll('.' + netClass);

        originalElements.forEach(el => {
            if (highlightLayer) {
                const clone = el.cloneNode(true);
                highlightLayer.appendChild(clone);
            }
        });
    });
}
function initMultiSelect() {
    const svgElement = document.querySelector('svg');
    if (!svgElement) return;
    const paths = svgElement.querySelectorAll('path[class]');
    paths.forEach(path => path.style.cursor = 'pointer');
    svgElement.addEventListener('click', function (e) {
        const clickedPath = e.target.closest('path');
        let netClass = clickedPath ? clickedPath.getAttribute('class') : null;
        if (netClass) netClass = netClass.trim();
        const isMeta = e.ctrlKey || e.metaKey;
        if (netClass) {
            if (isMeta) {
                if (selectedNets.has(netClass)) {
                    selectedNets.delete(netClass);
                } else {
                    selectedNets.add(netClass);
                }
            } else {
                if (selectedNets.has(netClass) && selectedNets.size === 1) {
                    selectedNets.clear();
                } else {
                    selectedNets.clear();
                    selectedNets.add(netClass);
                }
            }
            updateHighlights();
        }
        else {
            if (isMeta) {
                return;
            } else {
                if (selectedNets.size > 0) {
                    selectedNets.clear();
                    updateHighlights();
                }
            }
        }
    });

    console.log('Boardview script loaded. Paths found:', paths.length);
}
window.addEventListener('svg-loaded', () => { initMultiSelect(); });
