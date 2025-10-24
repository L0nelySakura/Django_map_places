document.addEventListener('DOMContentLoaded', function() {
    // Находим все inline-таблицы с фотографиями
    const inlineGroups = document.querySelectorAll('.inline-group');

    inlineGroups.forEach(function(group) {
        const tbody = group.querySelector('tbody');
        if (!tbody) return;

        // Делаем строки таблицы перетаскиваемыми
        new Sortable(tbody, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            onEnd: function(evt) {
                // Обновляем позиции после перетаскивания
                updatePositions(tbody);
            }
        });

        // Добавляем иконки для перетаскивания
        addDragHandles(tbody);
        // Инициализируем позиции
        updatePositions(tbody);
    });
});

function addDragHandles(tbody) {
    const rows = tbody.querySelectorAll('tr');
    rows.forEach(function(row, index) {
        // Пропускаем пустые строки для добавления новых фото
        if (row.classList.contains('empty-form')) return;

    });
}

function updatePositions(tbody) {
    const rows = tbody.querySelectorAll('tr:not(.empty-form)');
    rows.forEach(function(row, index) {
        const positionField = row.querySelector('input[id$="-position"]');
        if (positionField) {
            positionField.value = index + 1;
        }
    });
}