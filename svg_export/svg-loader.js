/**
 * Автономный загрузчик интерактивных SVG-плат.
 * 
 * На месте своего вызова находит тег <script>, считывает путь к файлу
 * из атрибута `data-src`, асинхронно скачивает SVG через HTTP GET запрос,
 * превращает текст в живые HTML-теги и полностью заменяет собой этот скрипт.
 * В конце генерирует глобальное событие 'svg-loaded' для старта остальной логики.
 * 
 * пример
 * <script src="svg-loader.js" data-src="BoardView.svg"></script>
 */
(async function () {
    const currentScript = document.currentScript;
    const svgPath = currentScript.getAttribute('data-src');
    const response = await fetch(svgPath);
    const svgText = await response.text();
    currentScript.parentNode.replaceChild(new DOMParser().parseFromString(svgText, 'image/svg+xml').documentElement, currentScript);
    window.dispatchEvent(new Event('svg-loaded'));
})();
