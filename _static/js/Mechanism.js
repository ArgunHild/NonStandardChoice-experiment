document.addEventListener('DOMContentLoaded', () => {
    
    // Function to clear cookies on page load
    window.onload = function() {
        document.cookie.split(";").forEach(function(cookie) {
            document.cookie = cookie
                .replace(/^ +/, "")
                .replace(/=.*/, "=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/");
        });
    };

    console.log('Mechanism loaded!');

    // Extracting Mechanism type from js_vars
    const Mechanism = js_vars.Mechanism;  // Ensure js_vars.Mechanism is passed from oTree

    // Function to determine which Mechanism to execute
    function MechanismHandler() {
        console.log('Mechanism selected:', Mechanism);

        if (Mechanism === 'Sequential') {
            Sequential();
        } else if (Mechanism === 'Binary') {
            Binary();
        } 
    }

    // Assign MechanismHandler to the button click event
    document.getElementById('NextButton').addEventListener('click', MechanismHandler);
    
});

// Placeholder functions for Sequential and Binary (to be implemented next)
function Sequential() {
    console.log('Sequential mechanism triggered!');
    const availableBundles = js_vars.AvailableBundles;  // Bundles like ["Math_3", "Spot_1"]
    const bundleIcons = js_vars.BundleIcons;  // Nested dictionary
    const Field_name = 'id_'+js_vars.Field_name;

    // Determine the rank (assuming rank is stored in js_vars)
    const rank = js_vars.Rank || "1";  // Default to rank "1" if not provided

    // Create a popup modal
    let popup = document.createElement("div");
    popup.id = "popupModal";
    popup.classList.add("popup");

    // Modal content
    popup.innerHTML = `
        <div class="popup-content">
            <h2>Select a Bundle</h2>
            <p>Click on a bundle to select it.</p>
            <div id="bundleContainer"></div>
        </div>
    `;

    document.body.appendChild(popup);

    let container = document.getElementById("bundleContainer");

    // Populate the modal with graphical bundle options
    availableBundles.forEach((bundle, index) => {
        let emoji = bundleIcons[bundle] || bundle;  // Get emoji from the correct rank, fallback to text if missing

        let bundleDiv = document.createElement("div");
        bundleDiv.classList.add("bundle-option");
        bundleDiv.innerHTML = `${emoji}`;  // Use the emoji

        // Click to select
        bundleDiv.addEventListener("click", () => {
            console.log("Selected bundle:", bundle);
            
            // Update the popup content with selection and next button
            container.innerHTML = `
                <p><strong>The outcome bundle is: ${emoji}.</strong></p>
                <button id="confirmSelection" class="next-button">Next</button>
            `;

            // Handle the next button click
            document.getElementById("confirmSelection").addEventListener("click", () => {
                // Save outcome bundle to the hidden field
                document.getElementById(Field_name).value = bundle;

                // Click the hidden Next button
                document.getElementById("HiddenNextButton").click();
            });
        });

        container.appendChild(bundleDiv);
    });
}


function Binary() {
    console.log('Binary mechanism triggered!');
    const availableBundles = js_vars.AvailableBundles; 
    const bundleIcons = js_vars.BundleIcons;
    const Field_name = 'id_'+js_vars.Field_name;
    const rank = js_vars.Rank || "1";  // Use the correct rank

    // Create popup
    let popup = document.createElement("div");
    popup.id = "popupModal";
    popup.classList.add("popup");
    popup.innerHTML = `
    <div class="popup-content">
        <h2>Binary Comparison</h2>
        <p>Select your preferred bundle</p>
        <div id="progressContainer">
            <div id="progressBar"></div>
        </div>
        <div id="comparisonContainer"></div>
    </div>
`;

    document.body.appendChild(popup);

    let container = document.getElementById("comparisonContainer");
    
    let index = 0;  // Tracking comparisons
    let progress = 0;  // Progress bar
    let winners = [];  // Store winners

    function startComparison(bundle1, bundle2) {
        let emoji1 = bundleIcons[bundle1] || bundle1;
        let emoji2 = bundleIcons[bundle2] || bundle2;

        container.innerHTML = `
            <div class="comparison">
                <button class="bundle-option" id="option1">${emoji1}</button>
                <span>or</span>
                <button class="bundle-option" id="option2">${emoji2}</button>
            </div>
        `;

        document.getElementById("option1").addEventListener("click", () => nextRound(bundle1));
        document.getElementById("option2").addEventListener("click", () => nextRound(bundle2));
    }

    function nextRound(winner) {
        winners.push(winner);
        index += 2;
        progress += 1;
    
        // Update Progress Bar
        let totalComparisons = availableBundles.length - 1;
        let completedComparisons = Math.min(progress, totalComparisons);
        let progressPercentage = (completedComparisons / totalComparisons) * 100;
        console.log(totalComparisons)
        document.getElementById("progressBar").style.width = progressPercentage + "%";
    
        // console.log(index)
        // TODO: there is a strange bug that leads to a double comparison at the end fix it.
        if (index < availableBundles.length) {
            startComparison(availableBundles[index], availableBundles[index + 1] || winner);
        } else if (winners.length > 1) {
            let finalWinner = winners.shift();
            startComparison(finalWinner, winners.shift());
        } else {
            // Display outcome under the comparisons
            let finalEmoji = bundleIcons[winners[0]] || winners[0];
    
            container.innerHTML = `
                <p><strong>The outcome bundle is: ${finalEmoji}.</strong></p>
                <button id="confirmSelection" class="next-button">Next</button>
            `;
    
            // Handle the next button click
            document.getElementById("confirmSelection").addEventListener("click", () => {
                // Save outcome bundle to the field
                document.getElementById(Field_name).value = winners[0];
    
                // Click the hidden Next button
                document.getElementById("HiddenNextButton").click();
            });
        }
    }
    

    // Start first comparison
    startComparison(availableBundles[index], availableBundles[index + 1]);
}

