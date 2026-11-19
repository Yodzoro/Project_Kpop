/*
let slideIndex = 1;

document.addEventListener('DOMContentLoaded', function() {
    showSlides(slideIndex);
});

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("main_selected_video");

    if (slides.length === 0) return;

    if (n > slides.length) {
        slideIndex = 1;
    }
    if (n < 1) {
        slideIndex = slides.length;
    }

    for (i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }

    slides[slideIndex - 1].classList.add("active");
}




let slideIndex = 1;

document.addEventListener('DOMContentLoaded', function () {
    showSlides(slideIndex);
});

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    const slides = document.getElementsByClassName("main_selected_video");

    if (slides.length === 0) return;

    if (n > slides.length) slideIndex = 1;
    if (n < 1) slideIndex = slides.length;

    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }

    const current = slides[slideIndex - 1];
    current.classList.add("active");

    // Загружаем видео только при первом показе слайда
    const iframe = current.querySelector("iframe");
    if (iframe && !iframe.getAttribute("src")) {
        iframe.setAttribute("src", iframe.dataset.src);
    }
}

*/

let slideIndex = 1;
const POSTER_AFTER_PLAY = 4000;  // сколько мс держать обложку ПОСЛЕ старта видео (пока исчезнет оверлей)
const POSTER_MAX_WAIT = 20000;   // страховка: убрать обложку в любом случае через это время

document.addEventListener('DOMContentLoaded', function () {
    showSlides(slideIndex);
});

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function hidePoster(iframe) {
    if (iframe._posterHidden) return;
    iframe._posterHidden = true;
    clearInterval(iframe._listenTimer);
    clearTimeout(iframe._fallbackTimer);

    const poster = iframe.parentElement.querySelector('.video_poster');
    if (poster) poster.classList.add('hidden');
}

// Просим плеер присылать нам события (статус воспроизведения)
function sendListening(iframe) {
    if (!iframe.contentWindow) return;
    iframe.contentWindow.postMessage(
        JSON.stringify({ event: 'listening', id: 1, channel: 'widget' }),
        'https://www.youtube.com'
    );
}

// Слушаем ответы от плееров: когда видео реально пошло, убираем обложку
window.addEventListener('message', function (e) {
    if (e.origin !== 'https://www.youtube.com') return;

    let data = e.data;
    if (typeof data === 'string') {
        try { data = JSON.parse(data); } catch (err) { return; }
    }
    if (!data) return;

    const playing =
        (data.event === 'onStateChange' && data.info === 1) ||
        (data.event === 'infoDelivery' && data.info && data.info.playerState === 1);
    if (!playing) return;

    // Определяем, от какого именно iframe пришло сообщение
    const iframe = Array.from(document.querySelectorAll('.video_frame'))
        .find(f => f.contentWindow === e.source);
    if (!iframe || iframe._playSeen) return;

    iframe._playSeen = true;
    setTimeout(() => hidePoster(iframe), POSTER_AFTER_PLAY);
});

function showSlides(n) {
    const slides = document.getElementsByClassName("main_selected_video");

    if (slides.length === 0) return;

    if (n > slides.length) slideIndex = 1;
    if (n < 1) slideIndex = slides.length;

    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }

    const current = slides[slideIndex - 1];
    current.classList.add("active");

    // Загружаем видео только при первом показе слайда
    const iframe = current.querySelector("iframe");
    if (iframe && !iframe.getAttribute("src")) {
        const sep = iframe.dataset.src.includes('?') ? '&' : '?';
        iframe.setAttribute(
            "src",
            iframe.dataset.src + sep + 'enablejsapi=1&origin=' + encodeURIComponent(location.origin)
        );

        // Пока плеер не ответил, повторяем запрос "слушай события"
        iframe._listenTimer = setInterval(() => sendListening(iframe), 500);

        // Страховка, если сообщение так и не придёт
        iframe._fallbackTimer = setTimeout(() => hidePoster(iframe), POSTER_MAX_WAIT);
    }
}