// Handle Pending Challans Form Submission
document.getElementById("pending-challans-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const vehicleNumber = document.getElementById("challanVehicleNumber").value.trim();

    if (!vehicleNumber) {
        alert("Please enter a vehicle number.");
        return;
    }

document.getElementById('pending-challans-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const vehicleNumber = document.getElementById('challanVehicleNumber').value.trim();
    const resultContainer = document.getElementById('challanResult');
    resultContainer.innerHTML = '<p>Loading...</p>';

    // Send POST request to Flask backend
    fetch('/check-challans', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ vehicle_number: vehicleNumber })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let resultHtml = '<h5>Challans:</h5><ul>';
            data.data.challans.forEach(challan => {
                resultHtml += `
                    <li>
                        Date: ${challan.date}<br>
                        Violation: ${challan.violation}<br>
                        Amount: ₹${challan.amount}
                    </li>`;
            });
            resultHtml += '</ul>';
            resultContainer.innerHTML = resultHtml;
        } else {
            resultContainer.innerHTML = `<p>${data.message}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultContainer.innerHTML = '<p>Error checking challans. Please try again later.</p>';
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
