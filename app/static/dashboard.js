var	background = document.querySelector("body");
var button = document.getElementById("searchbutton");
var buttonDiv = document.getElementById("searchbtn");
var resetbtnDiv = document.getElementById("resetbtn");
var searchInput = document.getElementsByClassName("searchInput");
var selectInput = document.getElementsByClassName("selectInput");

function validateAndSend() {
    if (myForm.bolNumber.value == '' && myForm.ordNumber.value == '' && myForm.invoiceNumber.value == '' && myForm.ak1.value == '' && myForm.gsID.value == '') {
        alert('You have to enter at least one BOL Number, Order Number or Invoice Number number.');
        return false;
    }else if(myForm.gsID.value != '' && (myForm.receiverID.value == '' && myForm.senderID.value == '')){
    	alert('You have to enter the Receiver ID if you are looking for a GS number.');
    }
    else {
		// background.style.color = "#555555";
		// background.style.backgroundColor = "#2053c1";
		buttonDiv.style.visibility = "hidden";
		resetbtnDiv.style.visibility = "hidden";
        myForm.submit();
    }
}

function resetValues(){
	for(var i = 0; i < searchInput.length; i++){
		searchInput[i].value = "";
        selectInput[i].value = "1";
	}
    $(document).ready(function() {
     $('.change-background').on('change', function() {
        var $this = $(this);
        var value = $.trim($this.val());

        // toggleClass can be provided a bool value,
        // If we provide true we add class, if false we remove class
        $this.toggleClass('filled-background', value.length !== 0);
      }).change();
      // We also want to call a 'change' event on 
      // all inputs with the change-background class just incase the page has
      // pre-filled in values
    });
}


$(document).ready(function() {
 $('.change-background').on('change', function() {
    var $this = $(this);
    var value = $.trim($this.val());

    // toggleClass can be provided a bool value,
    // If we provide true we add class, if false we remove class
    $this.toggleClass('filled-background', value.length !== 0);
  }).change();
  // We also want to call a 'change' event on 
  // all inputs with the change-background class just incase the page has
  // pre-filled in values
});