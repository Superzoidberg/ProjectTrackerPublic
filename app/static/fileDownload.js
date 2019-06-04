var ediFile = document.querySelector("textarea");





var x12 = "";



function downloadX12(){
	x12 = ediFile.textContent;
	x12 = x12.replace(/\n/g, "\r\n");
    var filename = window.location.pathname;
    filename = filename.replace("/","_");
    console.log("filename");
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";

    var blob = new Blob([x12], { type: "octet/stream" });
    var url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = "EDI" + filename + ".txt";
    a.click();
    window.URL.revokeObjectURL(url);
    // };

}