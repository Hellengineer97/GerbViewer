// Номера слоев, которыми мы управляем
const layersToControl = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];

// Ждем, пока первый скрипт полностью скачает и внедрит SVG карту на страницу
window.addEventListener('svg-loaded', () => {
    const controlsPanel = document.getElementById('controls-panel');
    if (!controlsPanel) return;

    layersToControl.forEach(num => {
        const layer = document.querySelector(`.layer${num}`);

        if (layer) {
            const btn = document.createElement('button');
            btn.className = 'toggle-btn';
            btn.innerText = `Слой ${num}: Вкл`;

            btn.addEventListener('click', () => {
                const isHidden = window.getComputedStyle(layer).display === 'none';

                if (isHidden) {
                    layer.style.display = 'block';
                    btn.innerText = `Слой ${num}: Вкл`;
                    btn.classList.remove('layer-disabled');
                } else {
                    layer.style.display = 'none';
                    btn.innerText = `Слой ${num}: Выкл`;
                    btn.classList.add('layer-disabled');
                }
            });

            controlsPanel.appendChild(btn);
        }
    });
});
