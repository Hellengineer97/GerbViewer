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
    const svgElement = document.querySelector('svg');

    // --- БЛОК БИБЛИОТЕКИ SVG-PAN-ZOOM С УМНОЙ ОПТИМИЗАЦИЕЙ ---
    if (typeof svgPanZoom !== 'undefined' && svgElement) {
        let renderTimer = null;

        // Функция временного снижения качества для плавной работы без лагов
        const setFastRendering = () => {
            svgElement.style.shapeRendering = 'optimizeSpeed';

            // Сбрасываем таймер, пока идет активный зум или перетаскивание
            if (renderTimer) clearTimeout(renderTimer);

            // Возвращаем идеальную четкость через 250мс после полной остановки
            renderTimer = setTimeout(() => {
                svgElement.style.shapeRendering = 'geometricPrecision';
            }, 500);
        };

        // Инициализируем панзум и передаем управление качеством во внутренние хуки
        svgPanZoom(svgElement, {
            zoomEnabled: true,
            panEnabled: true,
            controlIconsEnabled: false,
            mouseWheelZoomEnabled: true,
            fit: true,
            center: true,

            // Библиотека сама безопасно вызывает оптимизацию, не конфликтуя с мышью
            onPan: setFastRendering,
            onZoom: setFastRendering
        });

    } else {
        console.warn('Библиотека svg-pan-zoom не найдена.');
    }
    // --- КОНЕЦ БЛОКА ИНТЕГРАЦИИ ---

    // Логика кликов по контактам и дорожкам платы
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

// Запуск инициализации всей логики платы
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMultiSelect);
} else {
    initMultiSelect();
}
