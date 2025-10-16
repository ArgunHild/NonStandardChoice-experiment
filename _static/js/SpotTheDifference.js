document.addEventListener('DOMContentLoaded', () => {
    // ensure canvas is properly sized
    const canvas = document.getElementById('overlayCanvas');
    const img    = document.getElementById('image2');

    function resizeCanvas() {
        canvas.width  = img.clientWidth;
        canvas.height = img.clientHeight;
    }

    // If image is already loaded (cache hit), size immediately:
    if (img.complete && img.naturalWidth) {
        resizeCanvas();
    } else {
        // Otherwise wait for it:
        img.addEventListener('load', resizeCanvas);
    }



    // Clear all cookies on page load
    window.onload = function() {
        document.cookie.split(";").forEach(function(cookie) {
            document.cookie = cookie
                .replace(/^ +/, "")
                .replace(/=.*/, "=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/");
        });
    };

    // Disable the continue button initially
    const nextBtn = document.getElementById('NextButton');
    nextBtn.disabled = true;


    // console.log('Game started!');

    // the game_field variable
    const game_field_name = 'id_'+js_vars.field_name;

    let userMarks = []; // will store the user's marks
    let score = 0;
    const maxScore = 10; // Assuming there are 10 differences
    
    const circlesCountElement = document.getElementById('circlesCount'); // The new element for displaying count
    const ctx = canvas.getContext('2d');

    let matchedDifferences = new Set(); // Store indexes of matched differences
    // list of coordinates of correct places
    const actual_differences_elephant = [
        // x max: 400 (from game.css #image width), y max: 250 
        { x: 173, y: 188 }, // Example coordinates, replace with your actual values
        { x: 72, y: 37 }  ,
        { x: 47, y: 204 }  ,
        { x: 180, y: 82 }  ,
        { x: 103, y: 84 }  ,
        { x: 164, y: 30 }  ,
        { x: 298, y: 85 }  ,
        { x: 380, y: 133 }  ,
        { x: 272, y: 148 }  ,
        { x: 327, y: 255 }  ,
        { x: 327, y: 220 }  ,
    ];

const actual_differences_farm = [
    { x: 106, y: 38 },
    { x: 79,  y: 101 },
    { x: 295, y: 191 },
    { x: 50,  y: 222 },
    { x: 203, y: 179 },
    { x: 364, y: 94 },
    { x: 274, y: 75 },
    { x: 216, y: 93 },
    { x: 129, y: 145 },
    { x: 377, y: 208 },
];

    
    const actual_differences_grannies = [
        { x: 30, y: 60 }, // Example coordinates, replace with your actual values
        { x: 82, y: 96 }  ,
        { x: 41, y: 179 }  ,
        { x: 144, y: 150 }  ,
        { x: 207, y: 180 }  ,
        { x: 288, y: 113 }  ,
        { x: 332, y: 127 }  ,
        { x: 228, y: 82 }  ,
        { x: 151, y: 40 }  ,
        { x: 340, y: 58 }  ,
    ];
    
    const actual_differences_girls = [
        { x: 69,  y: 168 },
        { x: 145, y: 168 },
        { x: 339, y: 194 },
        { x: 358, y: 147 },
        { x: 281, y: 96 },
        { x: 378, y: 75 },
        { x: 299, y: 46 },
        { x: 201, y: 55 },
        { x: 62,  y: 104 },
        { x: 208, y: 162 },
    ];

    const trial = js_vars.trial;
    var actual_differences = actual_differences_grannies;
    if (trial == 'trial2') {
        var actual_differences = actual_differences_elephant;
    }
    else if (trial === 'trial3') {
        var actual_differences = actual_differences_farm;
    }
    else if (trial === 'trial4') {
        var actual_differences = actual_differences_girls;
    }

// Optional: to draw the differences on both sides
function drawDifferencesOnBothSides() {
    // Draw differences on right image (already positioned under the canvas)
    ctx.fillStyle = 'red';
    actual_differences.forEach(d => {
        ctx.beginPath();
        ctx.arc(d.x, d.y, 5, 0, 2 * Math.PI);
        ctx.fill();
    });

    // Draw same markers mirrored on left image
    const leftCanvas = document.getElementById('leftOverlayCanvas');
    if (leftCanvas) {
        const leftCtx = leftCanvas.getContext('2d');
        leftCtx.fillStyle = 'red';
        actual_differences.forEach(d => {
            leftCtx.beginPath();
            leftCtx.arc(d.x, d.y, 5, 0, 2 * Math.PI);
            leftCtx.fill();
        });
    }
}


    // Displayng maximum size to console to make it easy to select the correct coordinates
    img.addEventListener('load', () => {
        console.log(`Image Loaded: ${img.src}`);
        console.log(`Width: ${img.width}px, Height: ${img.height}px`);
    });
    // Drawing the actual differences to make it easy to debug
    function drawDifferences() {
        actual_differences.forEach(actual_differences => {
            ctx.fillStyle = 'red';
            ctx.beginPath();
            // Draw a circle at each actual_differences location
            ctx.arc(actual_differences.x, actual_differences.y, 5, 0, 2 * Math.PI); // Adjust the radius as needed
            ctx.fill();
        });
    }

    // to display the maximum number of clicks allowed
    function updateCirclesCount() {
        circlesCountElement.innerText = `Circles placed: ${userMarks.length}/10`;
        if (userMarks.length >= maxScore) {
            circlesCountElement.innerText = `Circles placed: ${userMarks.length}/10. \n Maximum number of circles reached. You can unclick some if you want to make changes.`;

            // Enable the continue button when the maximum number of marks is reached
            nextBtn.disabled = false;
        }
}

    function redrawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // drawDifferences();

        // Reset the score before recalculating
        score = 0;

        // Draw the user's marks and check each against actual_differences
    userMarks.forEach(mark => {
        let isCorrect = false;
        for (let diff of actual_differences) {
            if (Math.hypot(diff.x - mark.x, diff.y - mark.y) < 30) { // Threshold for being considered correct
                isCorrect = true;
                break; // Stop checking further if this mark is already correct
            }
        }

        if (isCorrect) {
            score++; // Increment score for correct marks
            // Optionally change mark color to indicate correctness
            ctx.strokeStyle = '#00FF00'; // Correct mark color
        } else {
            // Mark color for incorrect guesses
            ctx.strokeStyle = '#00FF00'; // Incorrect mark color
        }

        // Draw mark
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(mark.x, mark.y, 15, 0, Math.PI * 2);
        ctx.stroke();
    });

    // Update score and circles count display
    // console.log(game_field_name, game_field_name.value)
    document.getElementById(game_field_name).value = score;


    updateCirclesCount(); // Reflects the total number of marks put by the user
}



    
    // check if the user clicked near a difference
    function isClickNearMark(x, y) {
        const threshold = 15; // Adjust as needed
        const index = userMarks.findIndex(mark => {
            return Math.sqrt((mark.x - x) ** 2 + (mark.y - y) ** 2) < threshold;
        });
        return index;
    }

    // Check if the user clicked near an actual difference
    function isClickNearActualDifference(x, y) {
        const threshold = 20; // Define how close the click needs to be to an actual difference
        return actual_differences.some(difference => {
            return Math.hypot(difference.x - x, difference.y - y) < threshold;
        });
    }


    

    canvas.addEventListener('click', function(e) {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        console.log(`Click at (${x}, ${y})`);
    
        // First, check if the click is near an actual difference
        if (isClickNearActualDifference(x, y)) {
            // Increment score only if the mark is a new one and within the limits
            if (userMarks.length < maxScore && isClickNearMark(x, y) < 0) {
                score++;
            }
        }
    
        const nearMarkIndex = isClickNearMark(x, y);
        if (nearMarkIndex >= 0) {
            // User clicked near an existing mark, so remove it
            userMarks.splice(nearMarkIndex, 1);
        } else {
            // Only add a new mark if the maximum number of marks has not been reached
            if (userMarks.length < maxScore) {
                userMarks.push({x, y});
            } else {
                return; // Exit the function without adding a new mark
            }
        }
        redrawCanvas(); // Redraw the canvas to reflect the addition/removal of a mark
    });
    

    // Function to check proximity of click to existing marks
    function isClickNearMark(x, y) {
        const threshold = 20;
        return userMarks.findIndex(mark => Math.hypot(mark.x - x, mark.y - y) < threshold);
    }

    img.onload = () => {
        canvas.width = img.clientWidth;
        canvas.height = img.clientHeight;
        redrawCanvas();

        // DEBUG: show actual differences on both images
        //  delete this or comment (shows the true answers)
        // drawDifferencesOnBothSides();
    };

    if (img.complete && img.naturalWidth) {
        redrawCanvas();
    }
});
