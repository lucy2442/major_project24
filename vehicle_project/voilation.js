// Handle Pending Challans Form Submission
document.getElementById("pending-challans-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const vehicleNumber = document.getElementById("challanVehicleNumber").value.trim();

    if (!vehicleNumber) {
        alert("Please enter a vehicle number.");
        return;
    }

    // Simulate an API call to check pending challans
    // In a real-world scenario, you can use an API call here to fetch challan data
    const result = checkPendingChallans(vehicleNumber);

    document.getElementById("challanResult").innerHTML = result;
});

// Simulate checking for pending challans (Mock function for now)
function checkPendingChallans(vehicleNumber) {
    // Simulate a successful result (this should be replaced with an actual API request)
    const randomResult = Math.random() > 0.5 ? "Pending challans found!" : "No pending challans.";
    return `<div class="alert alert-info">${randomResult}</div>`;
}

// Handle Triple Seat Violation Detection Form Submission
document.getElementById("triple-seat-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const vehicleImage = document.getElementById("vehicleImage").files[0];

    if (!vehicleImage) {
        alert("Please upload a vehicle image.");
        return;
    }

    // Simulate detecting triple seat violation
    // In a real-world scenario, you should send the image to a server for analysis
    const result = detectTripleSeatViolation(vehicleImage);

    document.getElementById("tripleSeatResult").innerHTML = result;
});

// Simulate triple seat violation detection (Mock function for now)
function detectTripleSeatViolation(vehicleImage) {
    const randomResult = Math.random() > 0.5 ? "Triple seat violation detected!" : "No triple seat violation detected.";
    return `<div class="alert alert-warning">${randomResult}</div>`;
}

// Handle Red Line Violation Detection Form Submission
document.getElementById("red-line-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const redLineImage = document.getElementById("redLineImage").files[0];

    if (!redLineImage) {
        alert("Please upload an image for red line violation.");
        return;
    }

    // Simulate red line violation detection
    // In a real-world scenario, you should send the image to a server for analysis
    const result = detectRedLineViolation(redLineImage);

    document.getElementById("redLineResult").innerHTML = result;
});

// Simulate red line violation detection (Mock function for now)
function detectRedLineViolation(redLineImage) {
    const randomResult = Math.random() > 0.5 ? "Red line violation detected!" : "No red line violation detected.";
    return `<div class="alert alert-danger">${randomResult}</div>`;
}
