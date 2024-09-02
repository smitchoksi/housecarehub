function togglePopupClose()
{
    var v1 = document.getElementById("error-popup");
//    console.log(v1.style.display);
    v1.style.display="none";
    var container = document.getElementById("container");
    container.style.opacity=1;
}

function valuenull(id){
    togglePopupClose();
    var form = document.getElementById(id);
    var elements = form.elements;

    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        if (element.type !== "button") { // Exclude button elements
            element.value = ""; // Clear the value
        }
    }
}
