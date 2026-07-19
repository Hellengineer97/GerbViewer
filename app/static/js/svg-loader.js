/**
 * Автономный загрузчик интерактивной SVG-платы через API Flask.
 *
 * На месте своего вызова находит тег <script>, асинхронно запрашивает
 * динамический SVG-шаблон с бэкенда через эндпоинт `/api/get-svg`,
 * получает SVG документ и полностью заменяет ими себя.
 * В конце генерирует глобальное событие 'svg-loaded' для старта остальной логики.
 * 
 * пример
 * <script src="svg-loader.js"></script>
 */
(async function () {
    const currentScript = document.currentScript;
    const response = await fetch('/api/get-svg');
    const svgText = await response.text();
    const svgElement = new DOMParser().parseFromString(svgText, 'image/svg+xml').documentElement;
    currentScript.parentNode.replaceChild(svgElement, currentScript);
    window.dispatchEvent(new Event('svg-loaded'));
})();
