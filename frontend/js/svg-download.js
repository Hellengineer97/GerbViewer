document.addEventListener('DOMContentLoaded', () => {
    const downloadBtn = document.getElementById('download-svg-btn');
    if (!downloadBtn) return;
    downloadBtn.addEventListener('click', () => {
        const svgElement = document.querySelector('.zoom-layer svg');
        if (!svgElement) {alert("Ошибка: SVG не найден!");return;}
        const svgString = new XMLSerializer().serializeToString(svgElement);
        const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
        const downloadUrl = URL.createObjectURL(blob);
        const downloadLink = document.createElement('a');
        downloadLink.href = downloadUrl;
        downloadLink.download = 'boardview.svg';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        URL.revokeObjectURL(downloadUrl);
    });
});
