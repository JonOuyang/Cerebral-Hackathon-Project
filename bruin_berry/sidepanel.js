const readingBottomCircle = document.getElementById('readingBottomCircle');

async function readFunction(event) {
    event.preventDefault();  // Prevent form from reloading the page

    // const imageInput = document.getElementById('image');
    // const imageFile = imageInput.files[0];

    // let imageFile;

    // chrome.tabs.captureVisibleTab(null, {format: "png"}, function(dataUrl) {
    //   imageFile = dataUrl;
    // });

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.windows.update(tabs[0].windowId, { focused: true });
    });

    let imageFile = chrome.tabs.captureVisibleTab();

    if (!imageFile) {
        alert("Error encountered attempting to obtain image file");
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload-image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred.');
        }

        const result = await response.json();
        console.log('Server response:', result);  // Debugging line

        alert(result.result || 'Upload unsuccessful!');
    } catch (error) {
        console.error('Error:', error);  // Logs error in console for debugging
        alert(`Upload failed: ${error.message}`);
    }
}

readingBottomCircle.addEventListener('click', readFunction);




const watchTopCircle = document.getElementById('watchTopCircle');
  
async function watchFunction() {
  console.log('watchFunction')
  localStorage.setItem('activeWatch', true)
  localStorage.setItem('isBerryWatching', true)

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  //take screenshot + analyze
  while (localStorage.getItem('activeWatch') == true) {
  if (localStorage.getItem('isBerryWatching') == true) { console.log('taking screenshot') }
  await sleep(2000); // Wait for 2 seconds
  }
}

  watchTopCircle.addEventListener('click', watchFunction);
