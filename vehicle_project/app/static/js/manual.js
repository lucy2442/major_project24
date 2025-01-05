// Select the form and output container
const manualForm = document.querySelector(".manual-form");

// Form submission handler
manualForm.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent form from refreshing the page

    // Retrieve form values
    const vehicleNumber = document.getElementById("vehicleNumber").value.trim();
    const ownerName = document.getElementById("ownerName").value.trim();
    const vehicleType = document.getElementById("vehicleType").value;
    const comments = document.getElementById("comments").value.trim();

    // Validate form inputs
    if (!vehicleNumber || !ownerName || !vehicleType) {
        alert("Please fill in all required fields!");
        return;
    }

    // Show a success message in a pop-up
    alert(`Form Submitted Successfully!\n\nVehicle Number: ${vehicleNumber}\nOwner Name: ${ownerName}\nVehicle Type: ${vehicleType}\nComments: ${comments || "None"}`);

    // Optionally, show the data below the form (this can be added to a specific container if needed)
    // If needed, create a container in HTML to show the output

    // Reset the form after submission
    manualForm.reset();
});
