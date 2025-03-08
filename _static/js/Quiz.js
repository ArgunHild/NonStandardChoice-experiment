document.addEventListener('DOMContentLoaded', function() {
    const questions1 = [
        {"q": "What is the definition and the danger of recoil?", "choices": ["To recoil is to respond in fear, and it is dangerous because engineers and workers need to remain in control. Losing control could result in serious injuries on the job.", "Recoil is the concept of \u201ckicking back\u201d or leaping back after being released. It may be dangerous due to the possibility of injury upon having equipment \u201cleap back\u201d rapidly.", "To recoil is to move quickly and efficiently, and it is not dangerous but desired.", "To recoil is to feel revolted or disgusted, and it is dangerous because it creates job dissatisfaction."], "answer": "Recoil is the concept of \u201ckicking back\u201d or leaping back after being released. It may be dangerous due to the possibility of injury upon having equipment \u201cleap back\u201d rapidly."},
        {"q": "The Great Gatsby was written by which author?", "choices": ["Ernest Hemingway", "F. Scott Fitzgerald", "Mark Twain", "Harper Lee"], "answer": "F. Scott Fitzgerald"},
        {"q": "What process do plants use to convert sunlight into food?", "choices": ["Photosynthesis", "Respiration", "Transpiration", "Fermentation"], "answer": "Photosynthesis"},
        {"q": "What is the name for the small image icons used to express emotions or ideas in digital communication?", "choices": ["Emoticons", "Emails", "Emoji", "Signals"], "answer": "Emoji"},
        {"q": "What is a common term for the decrease in the value of money?", "choices": ["Inflation", "Deflation", "Recession", "Depression"], "answer": "Inflation"},
        {"q": "What is the hardest natural substance on Earth?", "choices": ["Granite", "Diamond", "Quartz", "Steel"], "answer": "Diamond"},
        {"q": "Which gas is the primary contributor to global warming?", "choices": ["Oxygen", "Hydrogen", "Carbon dioxide", "Nitrogen"], "answer": "Carbon dioxide"},
        {"q": "During its circulation throughout the body, blood from the left ventricle then goes to which of these locations?", "choices": ["left atrium", "aorta", "pulmonary artery", "right atrium"], "answer": "aorta"},
        {"q": "In which book series is the fictional continent Westeros found?", "choices": ["The Wheel of Time", "The Chronicles of Narnia", "A Song of Ice and Fire", "The Lord of the Rings"], "answer": "A Song of Ice and Fire"},
        {"q": "What is the largest planet in our solar system?", "choices": ["Earth", "Jupiter", "Mars", "Venus"], "answer": "Jupiter"},
        {"q": "What country has the longest coastline?", "choices": ["Canada", "Australia", "Russia", "Brazil"], "answer": "Canada"},
        {"q": "What is the Fibonacci sequence?", "choices": ["A series of numbers where the next number is found by adding up the two numbers before it", "A series of prime numbers", "A series of numbers where each number is the sum of the two preceding ones, starting from 0 and 1", "A series of numbers where each number is the product of the two preceding ones"], "answer": "A series of numbers where the next number is found by adding up the two numbers before it"},
        {"q": "Which artist painted \"Guernica\"?", "choices": ["Picasso", "Van Gogh", "Dali", "Monet"], "answer": "Picasso"},
        {"q": "What percentage of the Earth's surface is covered by oceans?", "choices": [0.51, 0.61, 0.71, 0.81], "answer": 0.71},
        {"q": "What is the most widely spoken language in India?", "choices": ["Hindi", "Bengali", "Tamil", "Marathi"], "answer": "Hindi"},
        {"q": "Who is the author of the Harry Potter series?", "choices": ["J.K. Rowling", "J.R.R. Tolkien", "Stephen King", "Suzanne Collins"], "answer": "J.K. Rowling"},
        {"q": "Prior\u00a0most nearly means", "choices": ["personal", "more urgent", "more attractive", "earlier"], "answer": "earlier"},
        {"q": "What is the force that causes objects to fall to the ground?", "choices": ["Gravity", "Electricity", "Magnetism", "Friction"], "answer": "Gravity"},
        {"q": "Who composed the Four Seasons?", "choices": ["Vivaldi", "Bach", "Mozart", "Beethoven"], "answer": "Vivaldi"},
        {"q": "What galaxy is Earth located in?", "choices": ["Milky Way", "Andromeda", "Galaxy B", "Whirlpool Galaxy"], "answer": "Milky Way"},
        {"q": "Which is the largest ocean on Earth?", "choices": ["Atlantic", "Pacific", "Indian", "Arctic"], "answer": "Pacific"},
        {"q": "Who was the first President of the United States?", "choices": ["George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"], "answer": "George Washington"},
        {"q": "Which composer wrote the Brandenburg Concertos?", "choices": ["Johann Sebastian Bach", "Wolfgang Amadeus Mozart", "Ludwig van Beethoven", "Franz Schubert"], "answer": "Johann Sebastian Bach"},
        {"q": "Your woodwork has a slightly uneven plane. Which tool should you use to correct the problem?", "choices": ["A rasp", "A file", "A chisel", "A plane"], "answer": "A plane"},
        {"q": "What is the study of meaning in language called?", "choices": ["Syntax", "Semantics", "Phonology", "Morphology"], "answer": "Semantics"},
        {"q": "Which primary colors are used to create all other colors?", "choices": ["Red, Yellow, Blue", "Red, Green, Blue", "Yellow, Blue, Purple", "Orange, Green, Violet"], "answer": "Red, Yellow, Blue"},
        {"q": "What is the main component of the sun?", "choices": ["Helium", "Hydrogen", "Nitrogen", "Oxygen"], "answer": "Hydrogen"},
        {"q": "Which bird is often associated with delivering babies in folklore?", "choices": ["Stork", "Sparrow", "Pelican", "Swan"], "answer": "Stork"},
        {"q": "Deportment\u00a0most nearly means", "choices": ["attendance", "intelligence", "neatness", "behavior"], "answer": "behavior"},
        {"q": "In tennis, what term is used for a score of zero?", "choices": ["Love", "Fault", "Deuce", "Advantage"], "answer": "Love"},
        {"q": "Current is measured using .", "choices": ["a currentometer", "wires", "an ammeter", "a spectrometer"], "answer": "an ammeter"},
        {"q": "What is the heaviest naturally occurring element?", "choices": ["Uranium", "Lead", "Plutonium", "Osmium"], "answer": "Uranium"},
        {"q": "What is a group of lions called?", "choices": ["Pack", "Pride", "School", "Herd"], "answer": "Pride"},
        {"q": "Which particle is negatively charged?", "choices": ["Electron", "Neutron", "Proton", "Photon"], "answer": "Electron"},
        {"q": "Who painted \"The Starry Night\"?", "choices": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"], "answer": "Vincent van Gogh"},
        {"q": "In which country is the traditional Maori haka dance performed?", "choices": ["Australia", "New Zealand", "Fiji", "Samoa"], "answer": "New Zealand"},
        {"q": "Which part of the atom helps determine its atomic number?", "choices": ["neutron", "proton", "electron", "anion"], "answer": "proton"},
        {"q": "Who wrote \"Le Petit Prince (The Little Prince)\"?", "choices": ["Richard Bach", "Ken Kesey", "James Redfield", "Antoine de Saint-Exup\u00e9ry"], "answer": "Antoine de Saint-Exup\u00e9ry"},
        {"q": "Who wrote \"To Kill a Mockingbird\"?", "choices": ["Harper Lee", "Ernest Hemingway", "Mark Twain", "J.D. Salinger"], "answer": "Harper Lee"},
        {"q": "Automatic transmissions transmit engine torque to the transmission via a", "choices": ["Torque case", "Torque axle", "Torque shaft", "Torque converter"], "answer": "Torque converter"} 
    ];

    const question2 = [
        {"q": "What river runs through Cairo?", "choices": ["Nile", "Amazon", "Thames", "Ganges"], "answer": "Nile"},
        {"q": "What year was the World Wide Web introduced to the public?", "choices": [1989, 1991, 1993, 1995], "answer": 1991},
        {"q": "What is the most commonly used letter in the English language?", "choices": ["E", "T", "A", "S"], "answer": "E"},
        {"q": "Who directed \"The Godfather\"?", "choices": ["Martin Scorsese", "Steven Spielberg", "Francis Ford Coppola", "Alfred Hitchcock"], "answer": "Francis Ford Coppola"},
        {"q": "What vitamin is produced when a person is exposed to sunlight?", "choices": ["Vitamin C", "Vitamin D", "Vitamin A", "Vitamin E"], "answer": "Vitamin D"},
        {"q": "Who wrote \"And Then There Were None\"?", "choices": ["Richard Bach", "Linda Hogan", "Agatha Christie", "James Baldwin"], "answer": "Agatha Christie"},
        {"q": "What TV series is based in the fictional town of Hawkins, Indiana?", "choices": ["Stranger Things", "Riverdale", "Smallville", "Euphoria"], "answer": "Stranger Things"},
        {"q": "What is the name of the default directory that serves as the main folder for user files in Windows?", "choices": ["Documents", "My Documents", "My Files", "User Folder"], "answer": "My Documents"},
        {"q": "What is the process by which plants make their food?", "choices": ["Transpiration", "Photosynthesis", "Respiration", "Osmosis"], "answer": "Photosynthesis"},
        {"q": "Who wrote \"The Power of Now\"?", "choices": ["Douglas Adams", "Eckhart Tolle", "Elisabeth K\u00fcbler-Ross", "Maxine Hong"], "answer": "Eckhart Tolle"},
        {"q": "To measure voltage, one would use", "choices": ["a volta", "a volt gauge", "a voltmeter", "an electrical difference machine"], "answer": "a voltmeter"},
        {"q": "Who wrote \"The Godfather\"?", "choices": ["Theodore Dreiser", "Don Miguel Ruiz", "Mario Puzo", "Edward Ball"], "answer": "Mario Puzo"},
        {"q": "What is the chemical symbol for gold?", "choices": ["Au", "Ag", "Gd", "Go"], "answer": "Au"},
        {"q": "What is the term for the fear of technology?", "choices": ["Cyberphobia", "Technophobia", "Robophobia", "Mechaphobia"], "answer": "Technophobia"},
        {"q": "What does \"HTTP\" stand for?", "choices": ["HyperText Transfer Protocol", "High Transfer Text Protocol", "Hyper Tech Transfer Protocol", "HyperText Tech Protocol"], "answer": "HyperText Transfer Protocol"},
        {"q": "What renewable energy source is derived from the Earth's internal heat?", "choices": ["Solar", "Wind", "Hydrothermal", "Geothermal"], "answer": "Geothermal"},
        {"q": "What kind of musical instrument is a zither?", "choices": ["Stringed instrument", "Woodwind instrument", "A kind of xylophone", "A kind of trumpet"], "answer": "Stringed instrument"},
        {"q": "Who composed the music for the ballet \u201cSwan Lake\u201d?", "choices": ["Mozart", "Vivaldi", "Tchaikovsky", "Dvorak"], "answer": "Tchaikovsky"},
        {"q": "What is the name of the galaxy closest to the Milky Way?", "choices": ["Andromeda", "Whirlpool", "Triangulum", "Black Eye"], "answer": "Andromeda"},
        {"q": "Who wrote the epic poem \"Paradise Lost\"?", "choices": ["John Milton", "William Blake", "Geoffrey Chaucer", "William Shakespeare"], "answer": "John Milton"},
        {"q": "Welders using the electric-arc welding method wear face shields to protect themselves from", "choices": ["Gamma radiation", "Ultraviolet radiation", "X-ray radiation", "Microwave radiation"], "answer": "Ultraviolet radiation"},
        {"q": "Who created the fictional detective Sherlock Holmes?", "choices": ["Mark Twain", "Agatha Christie", "Arthur Conan Doyle", "Charles Dickens"], "answer": "Arthur Conan Doyle"},
        {"q": "At which temperature would water freeze if recorded on a Fahrenheit thermometer?", "choices": ["21 degrees", "15 degrees", "32 degrees", "0 degrees"], "answer": "32 degrees"},
        {"q": "In a classroom of 32 students, 14 are male. What percentage of the class is female?", "choices": [0.46, 0.44, 0.56, 0.52], "answer": 0.56},
        {"q": "What is the name for the classification system used to organize living things?", "choices": ["The Linnaean System", "The Dewey Decimal System", "The Darwinian System", "The Newtonian System"], "answer": "The Linnaean System"},
        {"q": "Grimy\u00a0most nearly means", "choices": ["ill-fitting", "poorly made", "dirty", "ragged"], "answer": "dirty"},
        {"q": "What is tofu made from?", "choices": ["Wheat", "Milk", "Soybeans", "Rice"], "answer": "Soybeans"},
        {"q": "Which celestial body is the center of our Solar System?", "choices": ["Earth", "The Moon", "The Sun", "Jupiter"], "answer": "The Sun"},
        {"q": "To\u00a0necessitate\u00a0most nearly means", "choices": ["required", "irrelevant", "enter", "depart"], "answer": "required"},
        {"q": "Which film features a character named Forrest Gump?", "choices": ["Forrest Gump", "The Shawshank Redemption", "Pulp Fiction", "Schindler's List"], "answer": "Forrest Gump"},
        {"q": "What musical instrument has keys, pedals, and strings?", "choices": ["Piano", "Drum", "Guitar", "Trumpet"], "answer": "Piano"},
        {"q": "Which planet is known for its rings?", "choices": ["Mars", "Saturn", "Jupiter", "Venus"], "answer": "Saturn"},
        {"q": "Revenue\u00a0most nearly means", "choices": ["taxes", "income", "expenses", "produce"], "answer": "income"},
        {"q": "Which artist is known for the painting \"The Starry Night\"?", "choices": ["Pablo Picasso", "Vincent van Gogh", "Leonardo da Vinci", "Claude Monet"], "answer": "Vincent van Gogh"},
        {"q": "Which element is named after the creator of the periodic table?", "choices": ["Curium", "Einsteinium", "Mendelevium", "Nobelium"], "answer": "Mendelevium"},
        {"q": "The energy possessed by a moving object is called\u00a0 energy", "choices": ["acceleration", "kinetic", "potential", "true"], "answer": "kinetic"},
        {"q": "What is the smallest country in the world by land area?", "choices": ["Vatican City", "Monaco", "Nauru", "Liechtenstein"], "answer": "Vatican City"},
        {"q": "The rate of electrons through a conductor is measured in units of", "choices": ["volts", "electricity", "current", "amperes"], "answer": "amperes"},
        {"q": "Who painted the Sistine Chapel ceiling?", "choices": ["Michelangelo", "Raphael", "Donatello", "Leonardo da Vinci"], "answer": "Michelangelo"},
        {"q": "What is the main purpose of the operating system?", "choices": ["Run applications", "Manage hardware", "Play video games", "Browse the internet"], "answer": "Manage Inernet"},
];
    
    // Reset the local variables
    localStorage.removeItem("currentQuestion");
    localStorage.removeItem("timer");

    const game_field_name = 'id_'+js_vars.field_name;
    let currentQuestion = 0;
    let timer = 10;
    let interval;
    var questions = questions1
    
    const trial = js_vars.type

    if (trial == 'trial'){
        // console.log('trial')
        questions = question2
    }

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
        // Load saved state, if exists and the page is initially loaded
        if(localStorage.getItem("currentQuestion") && currentQuestion === 0) {
            currentQuestion = parseInt(localStorage.getItem("currentQuestion"), 10);
            // Load timer only if it's not already counting down
            if (!interval) {
                timer = parseInt(localStorage.getItem("timer"), 5);
            }
        }
    
        if (currentQuestion < questions.length) {
            currentQuestion_idx = currentQuestion+1;
            MaxQuestions_idx = questions.length-1;
            document.getElementById('question').textContent = 'Question ' + currentQuestion_idx + '. '  + questions[currentQuestion].q;
            // console.log('Question ' + currentQuestion_idx + 'of max ' + MaxQuestions_idx + '. '  + questions[currentQuestion].q)
            const choicesContainer = document.getElementById('choices');
            choicesContainer.innerHTML = ''; // Clear previous choices
            questions[currentQuestion].choices.forEach(function(choice) {
                const button = document.createElement('button');
                button.textContent = choice;
                button.onclick = selectAnswer;
                choicesContainer.appendChild(button);
            });
            // Update the timer display without resetting it
            document.getElementById('timer').textContent = `Time left for this question: ${timer} seconds`;
            // Only start the interval if it's not already running
            if (!interval) {
                interval = setInterval(updateTimer, 1000);
            }
        } else {
            document.getElementById('quiz-container').innerHTML = '<div>Quiz completed!</div>';
            // Clear local storage as the quiz is completed
            localStorage.removeItem("currentQuestion");
            localStorage.removeItem("timer");
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


    function updateTimer() {
        timer--;
        document.getElementById('timer').textContent = `Time left for this question: ${timer} seconds`;
        if (timer <= 0) {
            moveToNextQuestion();
        }
        // Save current state
        localStorage.setItem("currentQuestion", currentQuestion);
        localStorage.setItem("timer", timer);
    }

    function moveToNextQuestion() {
        clearInterval(interval);
        interval = null; // Clear interval ID
        currentQuestion++;
        // Reset the timer for the next question
        timer = 10;
        localStorage.setItem("currentQuestion", currentQuestion);
        localStorage.setItem("timer", timer);
        showQuestion();
    }

    showQuestion();
});
