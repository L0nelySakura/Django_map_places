// JavaScript для предварительного просмотра фотографий в админке
function previewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            // Находим ближайшую ячейку с превью
            var row = input.closest('tr');
            var previewCell = row.querySelector('.field-preview');
            
            if (previewCell) {
                previewCell.innerHTML = '<img src="' + e.target.result + '" style="max-height: 60px; max-width: 80px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />';
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Добавляем обработчик для всех полей загрузки файлов
document.addEventListener('DOMContentLoaded', function() {
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            previewImage(this);
        });
    });
});
