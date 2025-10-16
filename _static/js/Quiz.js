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

    const questions3 = [
        {"q": "What is the largest desert in the world?", "choices": ["Sahara", "Antarctic", "Arabian", "Gobi"], "answer": "Antarctic"},
        {"q": "Which blood type is known as the universal donor?", "choices": ["A", "B", "AB", "O negative"], "answer": "O negative"},
        {"q": "Who developed the theory of general relativity?", "choices": ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Galileo Galilei"], "answer": "Albert Einstein"},
        {"q": "Which instrument measures atmospheric pressure?", "choices": ["Thermometer", "Barometer", "Altimeter", "Hygrometer"], "answer": "Barometer"},
        {"q": "What is the capital city of Canada?", "choices": ["Toronto", "Vancouver", "Ottawa", "Montreal"], "answer": "Ottawa"},
        {"q": "Which ocean lies between Africa and Australia?", "choices": ["Atlantic", "Pacific", "Indian", "Arctic"], "answer": "Indian"},
        {"q": "Who painted the Mona Lisa?", "choices": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Caravaggio"], "answer": "Leonardo da Vinci"},
        {"q": "What does DNA stand for?", "choices": ["Deoxyribonucleic Acid", "Deoxynitric Acid", "Dynamic Nucleic Acid", "Dioxygen Nitric Acid"], "answer": "Deoxyribonucleic Acid"},
        {"q": "What planet is known as the Red Planet?", "choices": ["Venus", "Mars", "Mercury", "Jupiter"], "answer": "Mars"},
        {"q": "How many continents are there on Earth?", "choices": [5, 6, 7, 8], "answer": 7},
        {"q": "Which gas do humans exhale in higher concentration than they inhale?", "choices": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon dioxide"},
        {"q": "Which country invented paper?", "choices": ["Greece", "India", "China", "Egypt"], "answer": "China"},
        {"q": "What is H2O commonly known as?", "choices": ["Hydrogen", "Water", "Oxygen", "Salt"], "answer": "Water"},
        {"q": "What is the currency of Japan?", "choices": ["Won", "Yen", "Yuan", "Ringgit"], "answer": "Yen"},
        {"q": "Which organ pumps blood through the body?", "choices": ["Brain", "Heart", "Lungs", "Liver"], "answer": "Heart"},
        {"q": "What is the smallest unit of life?", "choices": ["Tissue", "Organ", "Cell", "Molecule"], "answer": "Cell"},
        {"q": "Who was known as the 'Maid of Orléans'?", "choices": ["Marie Curie", "Joan of Arc", "Catherine the Great", "Queen Victoria"], "answer": "Joan of Arc"},
        {"q": "Which element has the chemical symbol O?", "choices": ["Gold", "Oxygen", "Osmium", "Oxide"], "answer": "Oxygen"},
        {"q": "What is the capital of Australia?", "choices": ["Sydney", "Canberra", "Melbourne", "Perth"], "answer": "Canberra"},
        {"q": "What is the boiling point of water at sea level?", "choices": [50, 90, 100, 120], "answer": 100},
        {"q": "Which animal is the largest mammal?", "choices": ["Elephant", "Blue Whale", "Giraffe", "Orca"], "answer": "Blue Whale"},
        {"q": "What is the longest river in the world?", "choices": ["Amazon", "Nile", "Yangtze", "Mississippi"], "answer": "Nile"},
        {"q": "Who invented the telephone?", "choices": ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Guglielmo Marconi"], "answer": "Alexander Graham Bell"},
        {"q": "What is the hardest natural material?", "choices": ["Basalt", "Obsidian", "Diamond", "Granite"], "answer": "Diamond"},
        {"q": "How many bones are in the adult human body?", "choices": [106, 206, 256, 306], "answer": 206},
        {"q": "What is the capital of Italy?", "choices": ["Rome", "Venice", "Milan", "Florence"], "answer": "Rome"},
        {"q": "Which planet has the most moons?", "choices": ["Earth", "Saturn", "Jupiter", "Neptune"], "answer": "Saturn"},
        {"q": "What color is chlorophyll?", "choices": ["Green", "Blue", "Red", "Yellow"], "answer": "Green"},
        {"q": "What is the largest internal organ in the human body?", "choices": ["Heart", "Liver", "Lung", "Kidney"], "answer": "Liver"},
        {"q": "Who discovered penicillin?", "choices": ["Louis Pasteur", "Alexander Fleming", "Marie Curie", "Isaac Newton"], "answer": "Alexander Fleming"},
        {"q": "Which famous scientist introduced the idea of natural selection?", "choices": ["Charles Darwin", "Gregor Mendel", "Francis Crick", "Carl Linnaeus"], "answer": "Charles Darwin"},
        {"q": "What is the freezing point of water in Celsius?", "choices": [0, 32, 100, -10], "answer": 0},
        {"q": "What is the national flower of Japan?", "choices": ["Lotus", "Cherry blossom", "Rose", "Orchid"], "answer": "Cherry blossom"},
        {"q": "What is the chemical symbol for Iron?", "choices": ["Ir", "In", "Fe", "I"], "answer": "Fe"},
        {"q": "Which planet is closest to the sun?", "choices": ["Venus", "Mercury", "Earth", "Mars"], "answer": "Mercury"},
        {"q": "What does the Richter scale measure?", "choices": ["Temperature", "Wind speed", "Earthquake magnitude", "Sound"], "answer": "Earthquake magnitude"},
        {"q": "Which country is known as the Land of the Rising Sun?", "choices": ["China", "Thailand", "Japan", "Korea"], "answer": "Japan"},
        {"q": "What is the main language spoken in Brazil?", "choices": ["Spanish", "Portuguese", "French", "English"], "answer": "Portuguese"},
        {"q": "Who is the Greek god of the sea?", "choices": ["Zeus", "Apollo", "Poseidon", "Hermes"], "answer": "Poseidon"},
        {"q": "What is the tallest mountain in the world?", "choices": ["K2", "Mount Everest", "Kilimanjaro", "Denali"], "answer": "Mount Everest"}
        ];

    
    const questions4 = [
        {"q": "Which metal is liquid at room temperature?", "choices": ["Iron", "Mercury", "Sodium", "Copper"], "answer": "Mercury"},
        {"q": "Which continent is the largest by land area?", "choices": ["Africa", "Asia", "Europe", "North America"], "answer": "Asia"},
        {"q": "Who painted 'The Last Supper'?", "choices": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Titian"], "answer": "Leonardo da Vinci"},
        {"q": "Which planet is known as the Morning Star?", "choices": ["Venus", "Mars", "Mercury", "Jupiter"], "answer": "Venus"},
        {"q": "Which gas do plants absorb during photosynthesis?", "choices": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon dioxide"},
        {"q": "What is the capital of France?", "choices": ["Berlin", "Madrid", "Paris", "Lisbon"], "answer": "Paris"},
        {"q": "How many players are on a soccer team on the field?", "choices": [9, 10, 11, 12], "answer": 11},
        {"q": "Who wrote '1984'?", "choices": ["Aldous Huxley", "George Orwell", "Ray Bradbury", "J.D. Salinger"], "answer": "George Orwell"},
        {"q": "Which ocean is the smallest?", "choices": ["Arctic", "Atlantic", "Indian", "Southern"], "answer": "Arctic"},
        {"q": "What is the main ingredient in bread?", "choices": ["Yeast", "Flour", "Salt", "Sugar"], "answer": "Flour"},
        {"q": "What device converts electrical energy into mechanical motion?", "choices": ["Transformer", "Motor", "Generator", "Condenser"], "answer": "Motor"},
        {"q": "Which organ filters blood in the human body?", "choices": ["Liver", "Lung", "Heart", "Kidney"], "answer": "Kidney"},
        {"q": "Which color has the shortest wavelength?", "choices": ["Red", "Blue", "Green", "Violet"], "answer": "Violet"},
        {"q": "Who was the first person to walk on the Moon?", "choices": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins"], "answer": "Neil Armstrong"},
        {"q": "Which country gifted the Statue of Liberty to the USA?", "choices": ["Germany", "France", "Italy", "Spain"], "answer": "France"},
        {"q": "What is the fastest land animal?", "choices": ["Lion", "Cheetah", "Horse", "Leopard"], "answer": "Cheetah"},
        {"q": "What is the largest organ of the human body?", "choices": ["Liver", "Skin", "Heart", "Lung"], "answer": "Skin"},
        {"q": "What is the main gas found in Earth's atmosphere?", "choices": ["Oxygen", "Nitrogen", "Carbon dioxide", "Argon"], "answer": "Nitrogen"},
        {"q": "How many teeth does a normal adult human have?", "choices": [28, 30, 32, 34], "answer": 32},
        {"q": "What is the primary language spoken in Argentina?", "choices": ["Portuguese", "Spanish", "English", "French"], "answer": "Spanish"},
        {"q": "Which famous scientist formulated the three laws of motion?", "choices": ["Isaac Newton", "Albert Einstein", "Galileo", "Kepler"], "answer": "Isaac Newton"},
        {"q": "What is the capital of Egypt?", "choices": ["Cairo", "Alexandria", "Luxor", "Giza"], "answer": "Cairo"},
        {"q": "Which chemical element has the symbol Na?", "choices": ["Nitrogen", "Nickel", "Sodium", "Neon"], "answer": "Sodium"},
        {"q": "How many colors are in a rainbow?", "choices": [5, 6, 7, 8], "answer": 7},
        {"q": "Who wrote 'Pride and Prejudice'?", "choices": ["Jane Austen", "Emily Brontë", "Louisa May Alcott", "Mary Shelley"], "answer": "Jane Austen"},
        {"q": "What is the chemical formula for table salt?", "choices": ["NaCl", "KCl", "CaCO3", "H2SO4"], "answer": "NaCl"},
        {"q": "What is the largest island in the world?", "choices": ["Australia", "Greenland", "New Guinea", "Borneo"], "answer": "Greenland"},
        {"q": "Which part of the plant conducts photosynthesis?", "choices": ["Root", "Stem", "Leaf", "Flower"], "answer": "Leaf"},
        {"q": "What is the main ingredient in guacamole?", "choices": ["Tomato", "Avocado", "Onion", "Cucumber"], "answer": "Avocado"},
        {"q": "What kind of animal is a Komodo dragon?", "choices": ["Mammal", "Bird", "Reptile", "Fish"], "answer": "Reptile"},
        {"q": "Who was the first woman to win a Nobel Prize?", "choices": ["Rosalind Franklin", "Marie Curie", "Ada Lovelace", "Dorothy Hodgkin"], "answer": "Marie Curie"},
        {"q": "What is the largest bone in the human body?", "choices": ["Femur", "Tibia", "Humerus", "Spine"], "answer": "Femur"},
        {"q": "Which instrument is used to measure temperature?", "choices": ["Barometer", "Thermometer", "Altimeter", "Manometer"], "answer": "Thermometer"},
        {"q": "Which organ in the human body produces insulin?", "choices": ["Liver", "Pancreas", "Kidney", "Spleen"], "answer": "Pancreas"},
        {"q": "What planet is known for its Great Red Spot?", "choices": ["Mars", "Jupiter", "Saturn", "Neptune"], "answer": "Jupiter"},
        {"q": "Which sport uses a shuttlecock?", "choices": ["Tennis", "Badminton", "Cricket", "Squash"], "answer": "Badminton"},
        {"q": "What is the capital of Spain?", "choices": ["Madrid", "Barcelona", "Valencia", "Seville"], "answer": "Madrid"},
        {"q": "Which element has the atomic number 1?", "choices": ["Helium", "Hydrogen", "Oxygen", "Nitrogen"], "answer": "Hydrogen"},
        {"q": "How many days are in a leap year?", "choices": [364, 365, 366, 367], "answer": 366}
        ];



    // Reset the local variables
    localStorage.removeItem("currentQuestion");
    // localStorage.removeItem("timer");

    const game_field_name = 'id_'+js_vars.field_name;
    let currentQuestion = 0;
    // let timer = 10;
    // let interval;
    var questions = questions1
    
    const trial = js_vars.trial
    console.log('Quiz type:', trial, 'field_name:', game_field_name);

    if (trial === 'trial1') {
        questions = questions1;
    } else if (trial === 'trial2') {
        questions = question2;
    } else if (trial === 'trial3') {
        questions = questions3;
    } else if (trial === 'trial4') {
        questions = questions4;
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
            // if (!interval) {
            //     timer = parseInt(localStorage.getItem("timer"), 5);
            // }
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
            // document.getElementById('timer').textContent = `Time left for this question: ${timer} seconds`;
            // Only start the interval if it's not already running
            // if (!interval) {
            //     interval = setInterval(updateTimer, 1000);
            // }
        } else {
            document.getElementById('quiz-container').innerHTML = '<div>Quiz completed!</div>';
            // Clear local storage as the quiz is completed
            localStorage.removeItem("currentQuestion");
            // localStorage.removeItem("timer");
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

    function moveToNextQuestion() {
        // clearInterval(interval);
        interval = null; // Clear interval ID
        currentQuestion++;
        // Reset the timer for the next question
        // timer = 10;
        localStorage.setItem("currentQuestion", currentQuestion);
        // localStorage.setItem("timer", timer);
        showQuestion();
    }

    showQuestion();
});
