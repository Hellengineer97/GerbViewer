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
                    sendGbrToBackend(this.files[0], layerType);
                }
                this.value = '';
            };
            gbrInput.click();
        });
    });
}
async function sendGbrToBackend(file, layerType) {
    const formData = new FormData();
    formData.append('gbr_file', file);
    formData.append('layer_type', layerType);

    try {
        console.log(`Отправка: ${file.name}, Тип: ${layerType}`);
        const response = await fetch('/upload-gbr', { method: 'POST', body: formData });

        if (!response.ok) throw new Error(`Ошибка сервера: ${response.status}`);

        const result = await response.json();
        console.log('Успешно отправлено:', result);
        alert('Файл и тип слоя успешно переданы на бэкенд!');
    } catch (error) {
        console.error('Ошибка при отправке:', error);
        alert('Не удалось отправить данные.');
    }
}
document.addEventListener('DOMContentLoaded', function() {initGbrTransformUploader();});
