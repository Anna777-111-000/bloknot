console.log('MyNotes JS loaded');

document.addEventListener('DOMContentLoaded', function() {
    // Обработка категорий
    const categoryModal = document.getElementById('categoryModal');
    if (categoryModal) {
        categoryModal.addEventListener('shown.bs.modal', function() {
            document.querySelector('#categoryModal input[name="name"]').focus();
        });
    }

    // Подтверждение удаления категорий
    document.querySelectorAll('.delete-category').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Удалить эту категорию? Заметки не будут удалены, но потеряют связь с категорией.')) {
                e.preventDefault();
            }
        });
    });

    // Показать/скрыть кнопку удаления категории при наведении
    document.querySelectorAll('.category-badge').forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.querySelector('.delete-category').style.opacity = '1';
        });
        badge.addEventListener('mouseleave', function() {
            this.querySelector('.delete-category').style.opacity = '0';
        });
    });
});