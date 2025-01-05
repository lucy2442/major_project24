// Get DOM elements
const uploadImageBtn = document.getElementById("uploadImageBtn");
const liveWebcamBtn = document.getElementById("liveWebcamBtn");
const imageUploadSection = document.getElementById("imageUploadSection");
const webcamSection = document.getElementById("webcamSection");
const vehicleImage = document.getElementById("vehicleImage");
const uploadedImage = document.getElementById("uploadedImage");
const webcam = document.getElementById("webcam");
const captureBtn = document.getElementById("captureBtn");
const canvas = document.getElementById("canvas");

// Show Image Upload Section
uploadImageBtn.addEventListener("click", () => {
    imageUploadSection.classList.remove("d-none");
    webcamSection.classList.add("d-none");
});

// Show Webcam Section
liveWebcamBtn.addEventListener("click", () => {
    webcamSection.classList.remove("d-none");
    imageUploadSection.classList.add("d-none");
    startWebcam();
});

// Handle Image Upload
vehicleImage.addEventListener("change", () => {
    const file = vehicleImage.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            uploadedImage.src = reader.result;
        };
        reader.readAsDataURL(file);
    }
});

// Start Webcam
function startWebcam() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                webcam.srcObject = stream;
            })
            .catch((err) => {
                console.error("Error accessing webcam: ", err);
            });
    } else {
        alert("Webcam is not supported in this browser.");
    }
}

// Capture Webcam Image
captureBtn.addEventListener("click", () => {
    const context = canvas.getContext("2d");
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    context.drawImage(webcam, 0, 0, canvas.width, canvas.height);
    const capturedImage = canvas.toDataURL("image/png");

    // Show captured image
    uploadedImage.src = capturedImage;
});
