<?php

error_reporting(E_ERROR | E_PARSE);

require "functions.php";
require "msg.php";
require "reserved_names.php";

$uri = $_SERVER['REQUEST_URI'];


if ($uri[-1] == "/" && $uri != "/"){
    # removing last slash
    $uri = substr($uri,0, -1);
}


if ($uri == "/" || $uri == "/index.php" || $uri == "/index.php/"){
    main_page();
} else {
    $link = substr($uri,-(strlen($uri)-1), strlen($uri)-1);
    $type = get_page_type($link);
    $file = get_selected_file($link);

    if (in_array($link, R_NAMES)) {
        switch ($link) {
            case "rp":
                include '../html/report.html';
                break;
        }
    } else {
        switch ($type) {
            case "audio":
            case "voice":
                include '../html/audio.html';
                break;
            case "photo":
            case "sticker_webp":
                include '../html/photo.html';
                break;
            case "video":
            case "video_note":
            case "sticker_webm":
                include '../html/video.html';
                break;
            default:
                include '../html/unsupported_type.html';
                break;
    }
    }
}
