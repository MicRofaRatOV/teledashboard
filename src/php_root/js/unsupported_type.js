
function dot_extension(type) {
    switch (type) {
        case "audio":
            return ".mp3";
            break;
        case "voice":
            return ".ogg";
            break;
        case "video":
        case "video_note":
            return ".mp4";
            break;
        case "photo":
            return ".jpg";
            break;
        case "sticker_webm":
            return ".webm";
            break;
        case "sticker_tgs":
            return ".tgs";
            break;
        default:
            return "";
    }
}
console.log(previous_type, dot_extension(previous_type))
const downEl = document.getElementById("downloadElement");

downEl.download = previous_file+dot_extension(previous_type);

// type_changer
setInterval(function() {
    let xhr_type = new XMLHttpRequest();
    xhr_type.open("POST", "/get_file_type.php", true);
    xhr_type.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr_type.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            previous_type = this.responseText;
            //location.reload();
            window.location.replace("//"+location.hostname+window.location.pathname);
        }
    };
    xhr_type.send("link="+window.location.pathname);
}, 5000);