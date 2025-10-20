function move_to_alert(targetDiv){
    targetDiv.style.display = "flex";
    // calculate its position and scroll to this alert
    var windowHeight = window.innerHeight;
    var divHeight = targetDiv.clientHeight;
    var divTopOffset = targetDiv.getBoundingClientRect().top;
    var scrollPosition = divTopOffset - (windowHeight - divHeight) / 2;

    window.scrollTo({
        top: scrollPosition,
        behavior: "smooth"
    });
    // Apply a shake animation class
    targetDiv.classList.add("shake");

    // Wait for a moment, then remove the shake class
    setTimeout(function () {
        targetDiv.classList.remove("shake");
    }, 500); // Adjust the time (in milliseconds) for the duration of the shake effect
}

function next_button_comprehension(){
//     field1_name = 'id_Comprehension_password'
//     var field1 = document.getElementById(field1_name).value;
//     if (field1=='MARGUN'){
//     document.getElementById("submit_button").click();
// }
// else{
//     var targetDiv = document.getElementById("raiseHand");
//     move_to_alert(targetDiv)
// }
    document.getElementById("submit_button").click();
}
