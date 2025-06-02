function next_button_comprehension(){
    field1_name = 'id_Comprehension_password'
    var field1 = document.getElementById(field1_name).value;
    if (field1!='MARGUN'){
    var targetDiv = document.getElementById("alert-move-sliders");
    move_to_alert(targetDiv)
    }
    else{
    document.getElementById("submit_button").click();
    }
}
