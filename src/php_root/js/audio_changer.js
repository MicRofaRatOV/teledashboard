const supported_types = ["audio", "voice"];

// audio changer
setInterval(function() {
    let xhr_link = new XMLHttpRequest();
    xhr_link.open("POST", "/get_sel_file.php", true);
    xhr_link.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const audioEl = document.getElementById("interactiveAudio");
            if (previous_file == this.responseText) {
                //console.log("No changes")
            } else {
                audioEl.src = '/user_files/'+this.responseText;
                console.log("File changed", "from", previous_file, "to", this.responseText);
                previous_file = this.responseText;
            }
        }
    };
    xhr_link.send("link="+window.location.pathname);
}, 5000);

// type_changer
setInterval(function() {
    let xhr_type = new XMLHttpRequest();
    xhr_type.open("POST", "/get_file_type.php", true);
    xhr_type.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr_type.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const audioEl = document.getElementById("interactiveAudio");
            previous_type = this.responseText;
            if (supported_types.includes(previous_type)) {
                //console.log("No changes")
            } else {
                console.log("Type changed to", previous_type);
                audioEl.alt = "🌍 Browser can't open file: " + previous_type;
                //location.reload();
                window.location.replace("//"+location.hostname+window.location.pathname);
            }
        }
    };
    xhr_type.send("link="+window.location.pathname);
}, 5000);