const startButton = document.getElementById("startButton");

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function startLesson() {
    localStorage.setItem('isBerryWatching', true)

    console.log('watching active js')
    
    //take screenshot + analyze
    await sleep(2000) // Wait for 15 seconds
    console.log('p2')
    document.querySelector('video').pause();
    alert('video paused')
}


startButton.addEventListener("click", async () => { await startLesson(); });