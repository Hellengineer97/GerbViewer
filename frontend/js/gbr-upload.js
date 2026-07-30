function initGbrTransformUploader() {
    const containerBtn = document.getElementById('gbr-upload-container');
    const gbrInput = document.getElementById('gbr-upload-input');
    containerBtn.addEventListener('click', function(e) {
        if (e.target.classList.contains('gbr-option-item')) return;
        e.stopPropagation();
        this.classList.toggle('expanded');
    });
    document.addEventListener('click', () => {containerBtn.classList.remove('expanded');});
    containerBtn.querySelectorAll('.gbr-option-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.stopPropagation();
            const layerType = this.getAttribute('data-type');
            containerBtn.classList.remove('expanded');
            gbrInput.onchange = null;
            gbrInput.onchange = function() {
                if (this.files && this.files[0]) {
                    addGbrToQueue(this.files[0], layerType);
                }
                this.value = '';
            };
            gbrInput.click();
        });
    });
}
function addGbrToQueue(file, layerType) {
    // Находим наш новый изолированный контейнер для очереди файлов
    const queueContainer = document.querySelector('.upload-queue-list');
    if (!queueContainer) return;

    // Оставляем последние 15 символов имени файла для компактного отображения
    const maxLen = 15;
    const shortName = file.name.length > maxLen
        ? '...' + file.name.slice(-maxLen)
        : file.name;

    // Создаем элемент плашки
    const row = document.createElement('div');
    row.className = 'layer-row gbr-queue-row';

    // Пишем полный путь/имя файла в title всей плашки
    row.title = file.name;

    // ЗАПИСЫВАЕМ ДАННЫЕ В СВОБОДНЫЕ АТРИБУТЫ (будут видны в HTML-коде):
    row.setAttribute('data-src', file.name);          // Полный путь/имя файла
    row.setAttribute('data-layer-type', layerType);   // Тип слоя (например, SilkTop)

    // Дополнительно консервируем сам объект файла внутри DOM-элемента для отправки
    row._gbrFile = file;

    // Собираем верстку: тип слоя идет прямо в бэдж, а в названии — короткое имя
    row.innerHTML = `
        <div class="gbr-queue-badge">${layerType}</div>
        <div class="layer-name">${shortName}</div>
        <div class="layer-delete" title="Удалить из очереди">×</div>
    `;

    // Логика удаления: при клике на крестик плашка просто стирает сама себя
    row.querySelector('.layer-delete').addEventListener('click', function() {
        row.remove();
    });

    // Вставляем готовую плашку в контейнер очереди
    queueContainer.appendChild(row);
}
document.addEventListener('DOMContentLoaded', function() {initGbrTransformUploader();});
