window.onload = function() {
    const webcamButton = document.querySelector('.scan-button:nth-child(2)');
    const uploadButton = document.querySelector('.scan-button:nth-child(1)');
    const webcamFeedElement = document.getElementById('webcam-feed');
    const webcamVideo = document.getElementById('webcam-video');
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';

    // Function to handle webcam stream
    function startWebcam() {
        console.log("Webcam button clicked. Attempting to start webcam...");

        // Check if webcam feed element exists
        if (webcamFeedElement && webcamVideo) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    console.log("Webcam stream successfully acquired.");
                    webcamVideo.srcObject = stream;
                    webcamVideo.style.display = "block"; // Show the webcam feed
                    webcamFeedElement.innerHTML = ""; // Clear placeholder text
                })
                .catch(error => {
                    console.error("Error accessing webcam:", error);
                    webcamFeedElement.innerHTML = "Error accessing webcam: " + error.message;
                });
        } else {
            console.error("Webcam feed element not found");
        }
    }

    // Function to handle image upload
    function handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.src = e.target.result;
                img.onload = function() {
                    // Call your function to process the uploaded image here
                    processUploadedImage(img);
                };
            };
            reader.readAsDataURL(file);
        }
    }

    // Function to process uploaded image
    function processUploadedImage(image) {
        console.log("Processing uploaded image...");
        // Add your image processing logic here (e.g., passing to backend for OCR and detection)
        alert("Image processing functionality to be implemented.");
    }

    // Event listener for upload button
    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });

    // Event listener for file input change (image selection)
    fileInput.addEventListener('change', handleImageUpload);

    // Event listener for webcam button
    webcamButton.addEventListener('click', startWebcam);

    // Display the webcam feed placeholder text initially
    webcamFeedElement.innerHTML = "<p class='text-muted'>Webcam feed will appear here.</p>";
};
