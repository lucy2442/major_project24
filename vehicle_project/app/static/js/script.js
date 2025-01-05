// home section js

// JavaScript for Dropdown Menu and Navbar Functionality
document.addEventListener("DOMContentLoaded", function () {
    // Activate dropdowns using Bootstrap
    const dropdownElements = document.querySelectorAll('.dropdown-toggle');
    dropdownElements.forEach((dropdown) => {
        new bootstrap.Dropdown(dropdown);
    });

    // Smooth scrolling for navigation
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const targetId = link.getAttribute("href").split("#")[1];
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                event.preventDefault();
                targetElement.scrollIntoView({ behavior: "smooth" });
            }
        });
    });
});

// JavaScript for Form Validation
function validateContactForm() {
    const nameField = document.getElementById("name");
    const emailField = document.getElementById("email");
    const messageField = document.getElementById("message");

    if (nameField.value.trim() === "") {
        alert("Please enter your name.");
        nameField.focus();
        return false;
    }
    if (!validateEmail(emailField.value)) {
        alert("Please enter a valid email address.");
        emailField.focus();
        return false;
    }
    if (messageField.value.trim() === "") {
        alert("Please enter a message.");
        messageField.focus();
        return false;
    }
    alert("Form submitted successfully!");
    return true;
}

// Helper function to validate email
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Attach validation to the contact form
document.querySelector("form").addEventListener("submit", function (event) {
    if (!validateContactForm()) {
        event.preventDefault();
    }
});


// ********************scan the number plate section**************************
// Select DOM elements
const uploadImageButton = document.getElementById("uploadImage");
const startWebcamButton = document.getElementById("startWebcam");
const webcamFeed = document.getElementById("webcamFeed");
const uploadedImage = document.getElementById("uploadedImage");
const placeholderText = document.getElementById("placeholderText");

// Handle "Upload Image" functionality
uploadImageButton.addEventListener("click", () => {
    // Create an invisible file input
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";

    // Listen for file selection
    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = "block";
                webcamFeed.style.display = "none";
                placeholderText.style.display = "none";
            };
            reader.readAsDataURL(file);
        }
    });

    // Trigger the file input
    fileInput.click();
});

// Handle "Live Webcam" functionality
startWebcamButton.addEventListener("click", async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        webcamFeed.srcObject = stream;
        webcamFeed.style.display = "block";
        uploadedImage.style.display = "none";
        placeholderText.style.display = "none";
    } catch (error) {
        alert("Unable to access the webcam. Please check your device settings.");
    }
});




