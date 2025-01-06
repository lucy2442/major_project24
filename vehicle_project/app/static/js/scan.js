document.addEventListener("DOMContentLoaded", () => {
    const webcamVideo = document.getElementById("webcam-video");
    const canvas = document.getElementById("webcam-canvas");
    const resultText = document.getElementById("result-text");
    const webcamBtn = document.getElementById("webcam-btn");
    const stopBtn = document.getElementById("stop-btn");  // Button to stop webcam

    let webcamStream;
    let isProcessing = false;  // Prevent multiple requests

    webcamBtn.addEventListener("click", async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });
                webcamVideo.srcObject = webcamStream;
                webcamVideo.style.display = "block";
                processFrames();
            } catch (err) {
                resultText.textContent = "Error accessing webcam: " + err.message;
            }
        } else {
            resultText.textContent = "Your browser does not support webcam access.";
        }
    });

    // Stop webcam stream when stop button is clicked
    stopBtn.addEventListener("click", () => {
        if (webcamStream) {
            webcamStream.getTracks().forEach(track => track.stop());
            webcamVideo.style.display = "none";
            resultText.textContent = "Webcam stopped.";
        }
    });

    async function processFrames() {
        const ctx = canvas.getContext("2d");

        setInterval(async () => {
            if (isProcessing) return;  // Skip if still processing the previous frame
            isProcessing = true;  // Mark as processing

            // Capture frame from the video
            ctx.drawImage(webcamVideo, 0, 0, canvas.width, canvas.height);
            const frameData = canvas.toDataURL("image/jpeg");

            try {
                const response = await fetch("/process-frame", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ frame: frameData })
                });

                const result = await response.json();
                if (result.success) {
                    resultText.textContent = `Detected Plate: ${result.plate}\n` +
                        `Owner: ${result.owner}\nPending Amount: ${result.pending_amount}\nViolations: ${result.violations}`;
                } else {
                    resultText.textContent = result.error || "No plate detected.";
                }
            } catch (error) {
                resultText.textContent = "Error processing frame: " + error.message;
            }

            isProcessing = false;  // Mark as done processing
        }, 1000); // Process a frame every second
    }
});
