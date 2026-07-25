function generateLayerPanel() {
    console.log("=== Старт функции generateLayerPanel ===");

    const layerList = document.querySelector('.layer-list');
    if (!layerList) {
        console.error("Ошибка: Элемент '.layer-list' не найден в HTML!");
        return;
    }

    // Ищем SVG строго внутри контейнера .zoom-layer
    const svgElement = document.querySelector('.zoom-layer svg');
    if (!svgElement) {
        console.error("Ошибка: Тег <svg> внутри '.zoom-layer' не найден!");
        return;
    }
    console.log("Тег <svg> успешно обнаружен.");

    layerList.innerHTML = ''; // Очищаем панель перед сборкой

    const styleElement = svgElement.querySelector('style');
    const styleText = styleElement ? styleElement.textContent : '';
    console.log("Текст извлеченных стилей SVG:", styleText.trim());

    function getColorFromStyle(className) {
        const regex = new RegExp(`\\.${className}\\b[^}]*fill:\\s*(#[0-9a-fA-F]{3,8}|[a-zA-Z]+)`);
        const match = styleText.match(regex);
        const result = match ? match[1] : '#ffffff';
        return result;
    }

    function getVisibilityFromStyle(className) {
        const regex = new RegExp(`\\.${className}\\b[^}]*display:\\s*([^;\\s}]+)`);
        const match = styleText.match(regex);
        const displayValue = match ? match[1] : 'inline';
        return displayValue !== 'none';
    }

    const mainContainer = svgElement.querySelector('g');
    if (!mainContainer) {
        console.error("Ошибка: Главный <g> внутри <svg> не найден!");
        return;
    }

    const layers = mainContainer.querySelectorAll(':scope > g');
    console.log(`Найдено слоев для обработки: ${layers.length}`);

    layers.forEach((layer, index) => {
        const layerClass = layer.className.baseVal || layer.getAttribute('class');
        if (!layerClass) return;

        const layerNumber = layerClass.replace(/\D/g, '') || '0';
        const hexColor = getColorFromStyle(layerClass);
        const isVisible = getVisibilityFromStyle(layerClass);

        const activeClass = isVisible ? 'active' : '';
        const layerDisplayName = `Layer ${layerNumber}`;

        const row = document.createElement('div');
        row.className = 'layer-row';
        row.dataset.layerClass = layerClass;

        row.innerHTML = `
            <input type="color" class="layer-color-input" value="${hexColor}">
            <div class="layer-visible ${activeClass}"></div>
            <input type="number" class="layer-number-input" value="${layerNumber}" min="0" max="99">
            <div class="layer-name">${layerDisplayName}</div>
            <div class="layer-upload" title="Upload data to layer">⭡</div>
            <div class="layer-delete">×</div>
        `;

        layerList.appendChild(row);
    });

    console.log("=== Финиш: Панель слоев успешно сгенерирована ===");
}

// МЕХАНИЗМ АВТОПРОВЕРКИ (Ждем появления SVG в DOM)
const checkSvgInterval = setInterval(() => {
    console.log("Проверка наличия SVG в .zoom-layer...");

    if (document.querySelector(".zoom-layer svg")) {
        console.log("SVG появился! Останавливаем проверку и запускаем генерацию.");
        clearInterval(checkSvgInterval); // Выключаем таймер, чтобы не спамить
        generateLayerPanel();            // Запускаем сборку панели
    }
}, 100); // Проверяем каждые 100 миллисекунд
