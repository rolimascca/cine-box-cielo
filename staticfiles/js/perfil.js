document.addEventListener('DOMContentLoaded', function () {
    // Efecto para el avatar
    const avatar = document.querySelector('.avatar');
    const avatarEdit = document.querySelector('.avatar-edit');

    avatarEdit.addEventListener('click', function (e) {
        e.preventDefault();
        alert('Funcionalidad para cambiar avatar estará disponible pronto!');
    });

    // Animación para las tarjetas
    const cards = document.querySelectorAll('.profile-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease';

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });
});