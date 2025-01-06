// Handle Pending Challans Form Submission
document.getElementById("pending-challans-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const vehicleNumber = document.getElementById("challanVehicleNumber").value.trim();

    if (!vehicleNumber) {
        alert("Please enter a vehicle number.");
        return;
    }

    // Make an API call to check pending challans
    fetch(`/check_challan/${vehicleNumber}`)
        .then(response => response.json())
        .then(data => {
            if (data.pending_amount > 0) {
                document.getElementById("challanResult").innerHTML = `
                    <div class="alert alert-info">
                        Pending Challans: ₹${data.pending_amount}. Violations: ${data.violations.join(", ")}
                    </div>`;
            } else {
                document.getElementById("challanResult").innerHTML = `
                    <div class="alert alert-success">No pending challans.</div>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("challanResult").innerHTML = `
                <div class="alert alert-danger">Error checking challans. Please try again later.</div>`;
        });
});

// Handle Triple Seat Violation Detection Form Submission
document.getElementById("triple-seat-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const vehicleImage = document.getElementById("vehicleImage").files[0];

    if (!vehicleImage) {
        alert("Please upload a vehicle image.");
        return;
    }

    const formData = new FormData();
    formData.append('vehicleImage', vehicleImage);

    fetch('/detect_triple_seat', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("tripleSeatResult").innerHTML = `
                <div class="alert alert-warning">${data.result}</div>`;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("tripleSeatResult").innerHTML = `
                <div class="alert alert-danger">Error detecting violation. Please try again later.</div>`;
        });
});

// Handle Red Line Violation Detection Form Submission
document.getElementById("red-line-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const redLineImage = document.getElementById("redLineImage").files[0];

    if (!redLineImage) {
        alert("Please upload an image for red line violation.");
        return;
    }

    const formData = new FormData();
    formData.append('redLineImage', redLineImage);

    fetch('/detect_red_line', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("redLineResult").innerHTML = `
                <div class="alert alert-danger">${data.result}</div>`;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("redLineResult").innerHTML = `
                <div class="alert alert-danger">Error detecting violation. Please try again later.</div>`;
        });
});
