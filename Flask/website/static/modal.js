// Get the modal
var modal = document.getElementById("myModal");
modal.style.display = "none";
// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementById("closebutton");

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}



// Get the modal
var modal2 = document.getElementById("formModal");
// Get the button that opens the modal
modal2.style.display = "none";
var btn2 = document.getElementById("mybutton");

// Get the <span> element that closes the modal
var span2 = document.getElementById("closebutton2");
var club = document.getElementById("club");
var point = document.getElementById("point");
var event = document.getElementById("event");
var purchase = document.getElementById("Purchase");
var subform = document.getElementById("subform");

// When the user clicks on the button, open the modal
btn2.onclick = function() {
  modal2.style.display = "block";
}

subform.onclick = function(){
  // setTimeout(timevalue(), 5000)
}

// function timevalue(){
//   club.value = "0";
//   point.value = "0";
// }

// When the user clicks on <span> (x), close the modal
span2.onclick = function() {
  modal2.style.display = "none";
  club.value = "0";
  point.value = "0";
}


if(document.refreshForm.visited.value != ""){
  club.value = "0";
  point.value = "0";
}
//check for Navigation Timing API support
if (window.performance) {
  console.info("window.performance works fine on this browser");
}
console.info(performance.navigation.type);
if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
  console.info( "This page is reloaded" );
  club.value = "0";
  point.value = "0";
} else {
  console.info( "This page is not reloaded");
}