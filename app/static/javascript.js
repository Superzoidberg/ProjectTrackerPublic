var submitBtn = document.getElementById("submit");
var home = document.getElementById("home");
var completed = document.getElementById("completed");
var devcompleted = document.getElementById("devcompleted");
var myList = document.getElementById("myList");
var newProject = document.getElementById("newProject");
var login = document.getElementById("login");
var utctime = document.getElementsByClassName("utctime");
var table = document.querySelector("table");

var csv = "";



if(window.location.pathname.includes("login")){
    //login.classList.add("active");
    //pass
}else if(window.location.pathname.includes("devcompleted")){
    devcompleted.classList.add("active");
}else if(window.location.pathname.includes("completed")){
    completed.classList.add("active");
}else if(window.location.pathname.includes("new")){
    newProject.classList.add("active");
} else if (window.location.pathname.includes("allprojects")){
    home.classList.add("active");
}else{
    myList.classList.add("active");
}

try{
    submitBtn.classList.add("btn");
}catch{
  //pass
}
try{
    submitBtn.classList.add("btn-success");
}catch{
  //pass
}
try{
    submitBtn.classList.add("btn-block");
}catch{
  //pass
}



setTimeout(function() {
    $("#messageAlert").hide();
}, 5000);


function selectChanged(ctrl) {
    var val = ctrl.value;
    var frm = document.getElementById('navSelectForm');
    frm.action = val;
  }

for (i = 0; i < utctime.length; i++ ){
    var val = utctime[i].textContent
    var date = new Date(val);
    var options = { day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit' };
    date = date.toLocaleString("en-US", options);
    utctime[i].textContent = date;
}

function downloadCSV(){
    var le = table.rows.length;
    var cnt = 0;
    for (let row of table.rows) {
        for (let cell of row.cells) {
            let value = cell.innerText;
            value = value.replace(/,/g," ");
            value = value.replace(/(?:\r\n|\r|\n)/g, " ");
            if (value == "Last Comment Download"){
                csv = csv + "Last Comment" + ",";
            }else{
                csv = csv + value + ",";
            }
        }
        cnt = cnt +1;
        csv = csv + "\r\n";
    }

    var filename = "data.csv";
    if (cnt == le){
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.style = "display: none";
        // return function (csv, fileName) {
            // var json = JSON.stringify(data),
        var blob = new Blob([csv], { type: "octet/stream" })
        var url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = "data.csv";
        a.click();
        window.URL.revokeObjectURL(url);
        // };
    }
}


 
