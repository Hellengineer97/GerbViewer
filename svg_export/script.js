let selectedNets = new Set();

function updateHighlights() {
    document.querySelectorAll('.highlight').forEach(el => {
        el.classList.remove('highlight');
    });
    
    selectedNets.forEach(netClass => {
        document.querySelectorAll('.' + netClass).forEach(el => {
            el.classList.add('highlight');
        });
    });
}

function initMultiSelect() {
    const paths = document.querySelectorAll('path[class^="net"]');
    
    paths.forEach(path => {
        path.style.cursor = 'pointer';
        
        path.addEventListener('click', function(e) {
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

// Запуск
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMultiSelect);
} else {
    initMultiSelect();
}