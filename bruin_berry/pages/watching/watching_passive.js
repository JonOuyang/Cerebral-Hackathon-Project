function pauseLesson(event) {
    event.preventDefault();  // Prevent form from reloading the page
    localStorage.setItem('isBerryWatching', false)
}

function exit(event) {
    event.preventDefault();  // Prevent form from reloading the page
    localStorage.setItem('activeWatch', false)
}