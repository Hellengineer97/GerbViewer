(async function () {
    // 1. Находим именно этот текущий тег <script>, где выполняется код
    const currentScript = document.currentScript;

    // 2. Читаем из него путь к файлу, указанный в data-src="map.svg"
    const svgPath = currentScript.getAttribute('data-src');

    if (!svgPath) {
        console.error('Ошибка: не указан атрибут data-src у скрипта загрузки SVG.');
        return;
    }

    try {
        // 3. Скачиваем SVG-файл
        const response = await fetch(svgPath);
        if (!response.ok) throw new Error(`Статус ответа браузера: ${response.status}`);
        const svgText = await response.text();

        // 4. Создаем временный контейнер, чтобы превратить текст в реальные HTML-теги
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');
        const svgElement = svgDoc.documentElement;

        // 5. Заменяем тег <script> на полученный SVG-элемент
        currentScript.parentNode.replaceChild(svgElement, currentScript);

        // 6. Создаем кастомное событие, чтобы другие скрипты (например, кнопки) узнали, что SVG загружен
        window.dispatchEvent(new Event('svg-loaded'));

    } catch (error) {
        console.error('Не удалось внедрить SVG файл:', error);
        const errorNode = document.createTextNode(`[Ошибка загрузки SVG: ${error.message}]`);
        currentScript.parentNode.replaceChild(errorNode, currentScript);
    }
})();
