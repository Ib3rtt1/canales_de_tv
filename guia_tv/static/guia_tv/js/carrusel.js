
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
