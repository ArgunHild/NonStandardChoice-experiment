document.addEventListener('DOMContentLoaded', () => {

    window.onload = function() {
        document.cookie.split(";").forEach(function(cookie) {
            document.cookie = cookie
                .replace(/^ +/, "")
                .replace(/=.*/, "=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/");
        });
    };


    console.log('Game started!');

    // the game_field variable
    const game_field_name = 'id_'+js_vars.field_name;

    let userMarks = []; // will store the user's marks
    let score = 0;
    const maxScore = 10; // Assuming there are 10 differences
    
    const circlesCountElement = document.getElementById('circlesCount'); // The new element for displaying count
    const canvas = document.getElementById('overlayCanvas'); // where the differences are drawn
    const ctx = canvas.getContext('2d');
    const img = document.getElementById('image2');

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

    const trial = js_vars.trial;
    if (trial == 'trial') {
        console.log('trial')
        var actual_differences = actual_differences_farm;
    }
    else {
        var actual_differences = actual_differences_elephant;
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
            if (Math.hypot(diff.x - mark.x, diff.y - mark.y) < 20) { // Threshold for being considered correct
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
    console.log(game_field_name, game_field_name.value)
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
    };

    if (img.complete && img.naturalWidth) {
        redrawCanvas();
    }
});
