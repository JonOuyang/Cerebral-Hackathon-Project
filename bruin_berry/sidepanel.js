document.addEventListener('DOMContentLoaded', () => {
    const watchingButton = document.getElementById('watching');
    const readingButton = document.getElementById('reading');

    watchingButton.addEventListener('click', () => {
        window.location.href = 'pages/watching/watching_main.html';
    });

    readingButton.addEventListener('click', () => {
        window.location.href = 'pages/reading/reading_passive.html';
    });
});
