const startLessonInitButton = document.getElementById("startLessonInit");

async function startLessonInitialize() {
    localStorage.setItem('isBerryWatching', true)

    console.log('watching main js')

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
    
      //take screenshot + analyze
    await sleep(2000); // Wait for 15 seconds
    document.querySelector('video').pause();
    alert('video paused')
}

startLessonInitButton.addEventListener("click", async () => { await startLessonInitialize(); });