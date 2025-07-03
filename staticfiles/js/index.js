// Configuración inicial
document.addEventListener("DOMContentLoaded", function () {
    // Elementos del DOM
    const heroSection = document.getElementById('cineHero');
    const mainReserveBtn = document.getElementById('mainReserveBtn');
    const imageData = JSON.parse(document.getElementById('imageUrls').textContent);
    let currentImageIndex = 0;

    // Efecto de transición de imágenes en el hero
    function updateHeroImage() {
        if (imageData.length > 0) {
            heroSection.style.backgroundImage = `linear-gradient(rgba(4,30,66,0.7), rgba(4,30,66,0.3)), url(${imageData[currentImageIndex].url})`;
            mainReserveBtn.setAttribute('data-slug', imageData[currentImageIndex].slug);
        }
    }

    // Cambiar imagen cada 8 segundos (como Cineplanet)
    function rotateHeroImages() {
        if (imageData.length > 1) {
            currentImageIndex = (currentImageIndex + 1) % imageData.length;
            updateHeroImage();
        }
    }

    // Inicializar
    updateHeroImage();
    setInterval(rotateHeroImages, 8000);

    // Efecto hover en tarjetas de sala
    const salaCards = document.querySelectorAll('.cine-sala-card');
    salaCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
            card.style.boxShadow = '0 15px 30px rgba(0,0,0,0.2)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
    });

    // Click en botón principal
    mainReserveBtn.addEventListener('click', function () {
        const slug = this.getAttribute('data-slug');
        if (slug) {
            window.location.href = `/salas/${slug}/`;
        }
    });

    // Animación de scroll suave
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Tracking de eventos
    function trackEvent(action, category, label) {
        if (typeof dataLayer !== 'undefined') {
            dataLayer.push({
                'event': 'customEvent',
                'eventCategory': category,
                'eventAction': action,
                'eventLabel': label
            });
        }
    }

    // Trackear clicks importantes
    mainReserveBtn.addEventListener('click', () => {
        trackEvent('click', 'Reservas', 'Hero Banner Button');
    });

    document.querySelectorAll('.cine-sala-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const salaName = this.closest('.cine-sala-card').querySelector('h3').textContent;
            trackEvent('click', 'Reservas', `Sala: ${salaName}`);
        });
    });

    // Mostrar mensaje en consola
    console.log('%cCINEBOX 🎬', 'color: #e51937; font-size: 18px; font-weight: bold;');
    console.log('Sitio cargado correctamente | v1.0.0');
});