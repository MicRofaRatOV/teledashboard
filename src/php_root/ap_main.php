<?php

//error_reporting(E_ERROR | E_PARSE);

$key = $_POST["password"];
$cmd = $_POST["command"];
$arg = $_POST["arguments"];

require_once "functions.php";
require_once "msg.php";

$cmd = trim(preg_replace('/ {2,}/',' ', preg_replace("/\r\n|\r|\n/", ' ', $cmd)));
$arg = trim(preg_replace('/ {2,}/',' ', preg_replace("/\r\n|\r|\n/", ' ', $arg)));

include "../html/adminpanel.html";

// Start
$out = "<font color='#008b8b'>========== Output ==========</font><br>";

if (check_key($key)){
    $out .= "<font color='green'>Access key is correct</font><br>";
    $out .= "Adding operation to log<br><br>";
    $ip = get_ip();
    operation_to_log($key, $cmd, $arg, $ip);

    switch ($cmd) {
        case "help":
            $out .= AP_HELP;
            break;
        case "getidbylink":
            $out .= get_id_by_link($arg);
            break;
        case "banid":
            $out .= ban_by_id($arg);
            break;
        case "unbanid":
            $out .= unban_by_id($arg);
            break;
        case "banhistory":
            $out .= before_ban($arg);
            break;
        case "setlevel":
            $out .= set_level($arg);
            break;
        case "userinfo":
            $out .= user_info($arg);
            break;
        case "telegrambot":
            $out .= telegram($arg);
            break;
        default:
            $out .= "<font color='#b8860b'>Unknown command</font><br>Use '<font color='#008b8b'>help</font>' for more information<br>";
            break;

    }
} else {
    $out .= "<font color='#dc143c'>Incorrect key</font><br>";
}

include "../html/ap_output.html";
