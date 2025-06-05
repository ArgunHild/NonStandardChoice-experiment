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

function Sequential() {
    console.log('Sequential mechanism triggered!');
    const availableBundles = js_vars.AvailableBundles;
    
    const bundleIcons = js_vars.BundleIcons;
    const Field_name = 'id_' + js_vars.Field_name;
    console.log("→ [Mechanism] Loaded bundleIcons:", bundleIcons);
    const rank = js_vars.Rank || "1";

    let popup = document.createElement("div");
    popup.id = "popupModal";
    popup.classList.add("popup");

    popup.innerHTML = `
        <div class="popup-content section-box" style="text-align: center; background-color: #fff; padding: 20px;">
            <h2>Make Your Choice</h2>
            <p>Which of these bundles do you prefer?</p>
            <div id="bundleContainer"></div>
        </div>
    `;

    document.body.appendChild(popup);
    let container = document.getElementById("bundleContainer");

    availableBundles.forEach((bundle) => {
        let bundleKey = Array.isArray(bundle) ? bundle.join("_") : bundle;
        console.log("→ [Sequential] Rendering bundle:", bundle);
        console.log("→ [Sequential] Lookup key:", bundleKey);
        console.log("→ [Sequential] Icon for key:", bundleIcons[bundleKey]);

        //let emoji = bundleIcons[bundle] || bundle;
        let key   = Array.isArray(bundle) ? bundle.join("_") : bundle;
        let emoji = bundleIcons[key]      || (Array.isArray(bundle) ? bundle.join(" + ") : bundle);


        let bundleDiv = document.createElement("div");
        bundleDiv.classList.add("bundle-option");
        bundleDiv.innerHTML = `${emoji}`;

        bundleDiv.addEventListener("click", () => {
            console.log("Selected bundle:", bundle);

            container.innerHTML = `
                <div style="margin-top: 20px; padding: 15px 25px; border: 2px solid #a4d4ae; border-radius: 10px; background-color: #e8f5e9; display: inline-block;">
                    <p style="font-size: 1.2em; margin-bottom: 10px;"><strong>The outcome bundle is:</strong></p>
                    <span style="font-size: 2.2em; display: inline-block;">${emoji}</span>
                </div>
                <br>
                <button id="confirmSelection" class="next-button btn btn-primary" style="margin-top: 20px; font-size: 1.1em; padding: 10px 20px;">Next</button>
            `;

            document.getElementById("confirmSelection").addEventListener("click", () => {
                document.getElementById(Field_name).value = JSON.stringify(bundle);
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

    const Field_name = 'id_' + js_vars.Field_name;
    const rank = js_vars.Rank || "1";
    console.log("→ [Mechanism] Loaded bundleIcons:", bundleIcons);

    let popup = document.createElement("div");
    popup.id = "popupModal";
    popup.classList.add("popup");
    popup.innerHTML = `
    <div class="popup-content section-box" style="text-align: center; background-color: #fff; padding: 20px;max-width: 960px; width: 90%; margin: 0 auto;">
        <h2>Make Your Choice</h2>
        <p>Which of these bundles do you prefer?</p>
        <div id="progressContainer" style="margin: 10px 0; width: 100%; background-color: #eee; height: 20px; border-radius: 10px;">
            <div id="progressBar" style="height: 100%; background-color: #4caf50; width: 0%; border-radius: 10px; transition: width 0.3s ease;"></div>
        </div>
        <div id="comparisonContainer"></div>
    </div>
    `;

    document.body.appendChild(popup);
    let container = document.getElementById("comparisonContainer");

    let comparisons = [];
    for (let i = 0; i < availableBundles.length - 1; i += 2) {
        const b1 = availableBundles[i];
        const b2 = availableBundles[i + 1];
        if (b1 && b2 && b1 !== b2) {
            comparisons.push([b1, b2]);
        }
    }


    // const total = comparisons.length + Math.ceil(Math.log2(comparisons.length + 1));
    const total = availableBundles.length-1;
    let progress = 0;
    let winners = [];
    let index = 0;

    // If there is an unpaired bundle, add it directly to the winners list
    if (availableBundles.length % 2 !== 0) {
        winners.push(availableBundles[availableBundles.length - 1]);
    }
    
    function updateProgressBar() {
        console.log('comparisons length', comparisons.length)
        const percent = (progress / total) * 100;
        document.getElementById("progressBar").style.width = `${percent}%`;
        // console.log("→ [Binary] Total comparisons:", total);
        console.log("Progress:", progress, "/", total);
    }

    function startComparison(bundle1, bundle2) {
        let key1 = Array.isArray(bundle1) ? bundle1.join("_") : bundle1;
        let emoji1 = bundleIcons[key1]      || bundle1.join(" + ");
        //let emoji1 = bundleIcons[bundle1] || bundle1;

        let key2 = Array.isArray(bundle2) ? bundle2.join("_") : bundle2;
        let emoji2 = bundleIcons[key2]      || bundle2.join(" + ");

        //let emoji2 = bundleIcons[bundle2] || bundle2;

        // console.log("→ [Binary] bundle1:", bundle1);
        // console.log("→ [Binary] key1:", key1);
        // console.log("→ [Binary] icon1:", bundleIcons[key1]);
        // console.log("→ [Binary] bundle2:", bundle2);
        // console.log("→ [Binary] key2:", key2);
        // console.log("→ [Binary] icon2:", bundleIcons[key2]);

        container.innerHTML = `
            <div class="comparison" style="display: flex; align-items: center; justify-content: center; gap: 30px; margin-top: 20px;">
                <button class="bundle-option highlight-bundle" id="option1" style="font-size: 2em; padding: 20px 30px; border: 2px solid #ccc; border-radius: 12px; background-color: #f5f5f5;">${emoji1}</button>
                <span style="font-weight: bold;">or</span>
                <button class="bundle-option highlight-bundle" id="option2" style="font-size: 2em; padding: 20px 30px; border: 2px solid #ccc; border-radius: 12px; background-color: #f5f5f5;">${emoji2}</button>
            </div>
        `;

        document.getElementById("option1").addEventListener("click", () => nextRound(bundle1));
        document.getElementById("option2").addEventListener("click", () => nextRound(bundle2));
    }

    function nextRound(winner) {
        progress++;
        updateProgressBar();
        winners.push(winner);

        if (index < comparisons.length-1) {
            index++;
            let [b1, b2] = comparisons[index];
            startComparison(b1, b2);
        } else if (winners.length > 1) {
            let final1 = winners.shift();
            let final2 = winners.shift();
            startComparison(final1, final2);
        } else {
            let finalKey = Array.isArray(winners[0]) ? winners[0].join("_") : winners[0];
            let finalEmoji = Array.isArray(winners[0]) ? bundleIcons[finalKey] || winners[0].join(" + ") : bundleIcons[winners[0]] || winners[0];

            console.log("→ [Binary] Final winner bundle:", winners[0]);
            console.log("→ [Binary] Final key:", finalKey);
            console.log("→ [Binary] Final emoji from icons:", bundleIcons[finalKey]);

            container.innerHTML = `
                <div style="margin-top: 20px; padding: 15px 25px; border: 2px solid #a4d4ae; border-radius: 10px; background-color: #e8f5e9; display: inline-block;">
                    <p style="font-size: 1.2em; margin-bottom: 10px;"><strong>The outcome bundle is:</strong></p>
                    <span style="font-size: 2.2em; display: inline-block;">${finalEmoji}</span>
                </div>
                <br>
                <button id="confirmSelection" class="next-button btn btn-primary" style="margin-top: 20px; font-size: 1.1em; padding: 10px 20px;">Next</button>
            `;

            document.getElementById("confirmSelection").addEventListener("click", () => {
                document.getElementById(Field_name).value = JSON.stringify(winners[0]);
                document.getElementById("HiddenNextButton").click();
            });
        }
    }

    if (comparisons.length > 0) {
        let [b1, b2] = comparisons[0];
        startComparison(b1, b2);
    }
}
