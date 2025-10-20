
document.addEventListener("DOMContentLoaded", function () {
var likertDropdowns = document.querySelectorAll(".likert-scale");
var submitBtn = document.getElementById("submit-btn");

// Disable all rows except the first one
likertDropdowns.forEach((dropdown, index) => {
if (index > 0) {
    dropdown.disabled = true;
}
});

function updateLikertOptions() {
let maxAllowed = 10; // Maximum possible score

likertDropdowns.forEach((dropdown, index) => {
    let prevValue = index > 0 ? parseInt(likertDropdowns[index - 1].value) || maxAllowed : maxAllowed;

    // Restrict available choices based on the previous row’s selection
    dropdown.querySelectorAll("option").forEach(option => {
        if (option.value !== "" && parseInt(option.value) > prevValue) {
            option.disabled = true;
        } else {
            option.disabled = false;
        }
    });

    // Enable the next row only if the current one is selected
    if (dropdown.value) {
        if (index + 1 < likertDropdowns.length) {
            likertDropdowns[index + 1].disabled = false;
        }
    } else {
        // If a row is unselected, disable all rows below it
        for (let i = index + 1; i < likertDropdowns.length; i++) {
            likertDropdowns[i].disabled = true;
            likertDropdowns[i].value = ""; // Reset lower selections
        }
    }
});

checkIfAllSelected();
}

function checkIfAllSelected() {
let allFilled = [...likertDropdowns].every(dropdown => dropdown.value !== "");
submitBtn.disabled = !allFilled;

}


// Attach event listener to each dropdown
likertDropdowns.forEach(dropdown => {
dropdown.addEventListener("change", updateLikertOptions);
});

updateLikertOptions(); // Initialize correct state
});

