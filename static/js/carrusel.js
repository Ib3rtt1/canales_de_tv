
const carrusel = document.getElementById('carouselVertical');

function scrollUp() {
    carrusel.scrollBy({
        top: -200, // Cantidad de píxeles para desplazar hacia arriba
        behavior: 'smooth'
    });

    if (carrusel.scrollTop === 0) {
        carrusel.scrollTop = carrusel.scrollHeight / 2; // Reinicia al final si llega al tope
    }
}

function scrollDown() {
    carrusel.scrollBy({
        top: 200, // Cantidad de píxeles para desplazar hacia abajo
        behavior: 'smooth'
    });

    // Si llega al final, vuelve al principio
    if (carrusel.scrollTop >= carrusel.scrollHeight / 2) {
        carrusel.scrollTop = 0;
    }
}

// Al cargar la página, coloca el scroll en el punto medio para habilitar el efecto infinito
window.onload = function () {
    carrusel.scrollTop = carrusel.scrollHeight / 2;
}

// carrusel.js

function loadIframe(videoUrl) {
    const iframe = document.getElementById('videoIframe');
    iframe.src = videoUrl; // Cambia la URL del iframe
    const videoModal = new bootstrap.Modal(document.getElementById('videoModal'));
    videoModal.show(); // Muestra el modal
}

// Al cerrar el modal, reinicia el video
const videoModal = document.getElementById('videoModal');
videoModal.addEventListener('hidden.bs.modal', function () {
    const iframe = videoModal.querySelector('iframe');
    iframe.src = ''; // Reinicia el iframe
});


