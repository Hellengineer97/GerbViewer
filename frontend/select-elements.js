let selectedNets = new Set();
function updateHighlights() {
    document.querySelectorAll('.highlight').forEach(el => {
        el.classList.remove('highlight');
        if (el._originalParent) {
            el._originalParent.appendChild(el);
        }
    });
    selectedNets.forEach(netClass => {
        document.querySelectorAll('.' + netClass).forEach(el => {
            el.classList.add('highlight');
            const layerGroup = el.parentElement;
            if (layerGroup) {
                const mainContainer = layerGroup.parentElement;
                if (mainContainer) {
                    if (!el._originalParent) {
                        el._originalParent = layerGroup;
                    }
                    mainContainer.appendChild(el);
                }
            }
        });
    });
}
function initMultiSelect() {
    const paths = document.querySelectorAll('path[class^="net"]');
    const svgElement = document.querySelector('svg');
    paths.forEach(path => {
        path.style.cursor = 'pointer';
        path.addEventListener('click', function (e) {
            const netClass = Array.from(this.classList).find(cls => cls.startsWith('net'));
            if (!netClass) return;
            if (e.ctrlKey || e.metaKey) {
                if (selectedNets.has(netClass)) {
                    selectedNets.delete(netClass);
                } else {
                    selectedNets.add(netClass);
                }
            } else {
                selectedNets.clear();
                selectedNets.add(netClass);
            }

            updateHighlights();
            e.stopPropagation();
        });
    });
    console.log('Boardview script loaded. Paths found:', paths.length);
}
window.addEventListener('svg-loaded', () => {
    initMultiSelect();
});
