async function pauseLesson() {
    localStorage.setItem('isBerryWatching', false)

}

function exit(event) {
    event.preventDefault();  // Prevent form from reloading the page
    localStorage.setItem('activeWatch', false)
}
