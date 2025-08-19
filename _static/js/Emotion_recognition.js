document.addEventListener('DOMContentLoaded', function() {
    const questions1 = [
        {"q": "Emotion_recognition/Amusement.png", "choices": ["Amusement", "Desire", "Surprise", "Excitement"], "answer": "Amusement"},
        {"q": "Emotion_recognition/Anger.png", "choices": ["Sadness", "Pain", "Anger", "Disgust"], "answer": "Anger"},
        {"q": "Emotion_recognition/Compassion.png", "choices": ["Compassion", "Sadness", "Anger", "Interest"], "answer": "Compassion"},
        {"q": "Emotion_recognition/Contempt.png", "choices": ["Sadness", "Shame", "Disgust", "Contempt"], "answer": "Contempt"},
        {"q": "Emotion_recognition/Desire.png", "choices": ["Disgust", "Love", "Contempt", "Desire"], "answer": "Desire"},
        {"q": "Emotion_recognition/Disgust.png", "choices": ["Anger", "Pain", "Disgust", "Sadness"], "answer": "Disgust"},
        {"q": "Emotion_recognition/Embarrassment.png", "choices": ['Embarrassment','Sadness','Amusement','Shame'], "answer": "Embarrassment"},
        {"q": "Emotion_recognition/Embarrassment_2.png", "choices": ['Sadness','Shame','Embarrassment','Love'], "answer": "Embarrassment"},
        {"q": "Emotion_recognition/Fear.png", "choices": ['Embarrassment','Fear','Sadness', 'Desire'], "answer": "Fear"},
        {"q": "Emotion_recognition/Flirtatiousness.png", "choices": ['Flirtatiousness','Desire','Embarrassment','Love'], "answer": "Flirtatiousness"},  
    ];
    
    const question2 = [
        {"q": "Emotion_recognition/Happiness.png", "choices": ['Flirtatiousness','Interest','Happiness','Politeness'], "answer": "Happiness"},
        {"q": "Emotion_recognition/Interest.png", "choices": ['Surprise','Interest','Desire','Happiness'], "answer": "Interest"},
        {"q": "Emotion_recognition/Love.png", "choices": ['Satisfaction','Flirtatiousness','Love','Compassion'], "answer": "Love"},
        {"q": "Emotion_recognition/Pain.png", "choices": ['Shame','Anger','Sadness','Pain'], "answer": "Pain"},
        {"q": "Emotion_recognition/Pain_2.png", "choices": ['Guilt','Sadness','Pain','Disgust'], "answer": "Pain"},
        {"q": "Emotion_recognition/Politeness.png", "choices": ['Happiness','Desire','Politeness','Disgust'], "answer": "Politeness"},
        {"q": "Emotion_recognition/Pride.png", "choices": ['Pride','Contempt',' Excitement','Anger'], "answer": "Pride"},
        {"q": "Emotion_recognition/Sadness.png", "choices": ['Sadness','Shame','Disgust','Compassion'], "answer": "Sadness"},
        {"q": "Emotion_recognition/Shame.png", "choices": ['Sadness','Pride','Embarrassment','Shame'], "answer": "Shame"},
        {"q": "Emotion_recognition/Surprise.png", "choices": ['Fear','Surprise','Interest','Compassion'], "answer": "Surprise"},
        
];
    // disable the continue button
    const nextBtn = document.getElementById('NextButton');
    nextBtn.disabled = true;
    // Reset the local variables
    localStorage.removeItem("currentQuestion");
    // localStorage.removeItem("timer"); // uncomment to have a timer

    const game_field_name = 'id_'+js_vars.field_name;
    const round = js_vars.round;
    let currentQuestion = 0;
    const trial = js_vars.trial;
    var questions = questions1
    
    if (trial == 'trial'){
        console.log('trial')
        questions = question2
    }

    // uncomment to have a timer
    // let timer = 10;
    // let interval;

        

    // this is the image element that holds the picture. will change it dynamically
    const imageElement = document.getElementById('image1');
    const staticPrefix = '/static/';  // If your static files are served at this path

    function setChoiceButtonsDisabled(state) {
        const buttons = document.querySelectorAll('#choices button');
        buttons.forEach(button => {
            button.disabled = state;
        });

        setTimeout(() => {
            buttons.forEach(button => {
                button.disabled = false;
            });
        }, 3000); 
     
    }


    function showQuestion() {

        console.log("Trial:", trial);
        console.log("Using questions:", questions);
        console.log("questions.length:", questions.length);
        console.log("currentQuestion:", currentQuestion);

        // Load saved state, if exists and the page is initially loaded
        if(localStorage.getItem("currentQuestion") && currentQuestion === 0) {
            const savedIndex = parseInt(localStorage.getItem("currentQuestion"), 10);
            // Load timer only if it's not already counting down
            // if (!interval) { // uncomment to have a timer
            //     timer = parseInt(localStorage.getItem("timer"), 5);
            // }
            if (savedIndex < questions.length) {
                currentQuestion = savedIndex;
            } else {
                currentQuestion = 0;
                localStorage.setItem("currentQuestion", currentQuestion); // Reset if saved index is out of bounds
            }
        }

    
        if (currentQuestion < questions.length) {
            console.log('Loading question:', currentQuestion);
            currentQuestion_idx = currentQuestion+1;
            MaxQuestions_idx = questions.length-1;
            // document.getElementById('question').textContent = 'Question ' + currentQuestion_idx + '. '  + questions[currentQuestion].q;
            
            // change picture
            imageElement.src = staticPrefix + questions[currentQuestion].q;

            const choicesContainer = document.getElementById('choices');
            choicesContainer.innerHTML = ''; // Clear previous choices
            questions[currentQuestion].choices.forEach(function(choice) {
                const button = document.createElement('button');
                button.textContent = choice;
                button.onclick = selectAnswer;
                choicesContainer.appendChild(button);
            });
            // Update the timer display without resetting it
            // document.getElementById('timer').textContent = `Time left for this question: ${timer} seconds`; // uncomment to have a timer
            // Only start the interval if it's not already running
            // if (!interval) { // uncomment to have a timer
            //     interval = setInterval(updateTimer, 1000);
            // }
        } else {
            document.getElementById('quiz-container').innerHTML = '<div>Quiz completed!</div>';
            // Clear local storage as the quiz is completed
            localStorage.removeItem("currentQuestion");
            // localStorage.removeItem("timer");
            // HERE: enable Continue
            console.log('enable next button')
            nextBtn.disabled = false;
        }
    }

    function selectAnswer(event) {
        const selectedAnswer = event.target.textContent;
        const correctAnswer = questions[currentQuestion].answer;
        if (selectedAnswer === correctAnswer) {
            // console.log(currentQuestion,  'is Correct!');
            document.getElementById(game_field_name).value ++;
        } else {
            // console.log(currentQuestion, 'is Wrong!');
        }
        moveToNextQuestion();
        setChoiceButtonsDisabled(true);
    }

    // uncomment to have a timer
    // function updateTimer() {
    //     timer--;
    //     document.getElementById('timer').textContent = `Time left for this question: ${timer} seconds`;
    //     if (timer <= 0) {
    //         moveToNextQuestion();
    //     }
    //     // Save current state
    //     localStorage.setItem("currentQuestion", currentQuestion);
    //     localStorage.setItem("timer", timer);
    // }

    // to have a timer replace the function below with this one
    // function moveToNextQuestion() {
    //     clearInterval(interval);
    //     interval = null; // Clear interval ID
    //     currentQuestion++;
    //     // Reset the timer for the next question
    //     localStorage.setItem("currentQuestion", currentQuestion);
    //     timer = 10; 
    //     localStorage.setItem("timer", timer);
    //     showQuestion();
    // }

    function moveToNextQuestion() {
        currentQuestion++;
        if (currentQuestion < questions.length) {
            showQuestion();
        } else {
            document.getElementById('quiz-container').innerHTML = '<div>Quiz completed!</div>';
            localStorage.removeItem("currentQuestion"); // Ensure quiz progress resets
            // localStorage.removeItem("timer");
            // HERE: enable Continue
            console.log('enable next button')
            nextBtn.disabled = false;
        }
    }

    showQuestion();
});
