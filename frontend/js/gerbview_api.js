// gerbview_api.js
const API_BASE = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {
    initRenderButton('render-svg-btn', '/render');
    initRenderButton('generate-net-btn', '/generate_net');
});

function initRenderButton(buttonId, endpoint) {
    const btn = document.getElementById(buttonId);
    if (!btn) return;

    const originalText = btn.textContent;

    btn.addEventListener('click', async () => {
        const queueRows = document.querySelectorAll('.upload-queue-list .gbr-queue-row');
        if (queueRows.length === 0) {
            alert('Очередь пуста. Добавьте GBR-файлы.');
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Rendering...';

        const formData = new FormData();

        queueRows.forEach((row) => {
            const file = row._gbrFile;
            const layerType = row.getAttribute('data-layer-type');
            formData.append('files', file, file.name);
            formData.append('types', layerType);
        });

        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText || response.statusText}`);
            }

            const svgText = await response.text();
            injectSvg(svgText);

        } catch (err) {
            console.error(`Request to ${endpoint} failed:`, err);
            alert('Ошибка: ' + err.message);
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    });
}

function injectSvg(svgText) {
    const zoomLayer = document.querySelector('.zoom-layer');
    if (!zoomLayer) {
        console.error('zoom-layer не найден');
        return;
    }
    zoomLayer.innerHTML = svgText;
    window.dispatchEvent(new CustomEvent('svg-loaded'));
}