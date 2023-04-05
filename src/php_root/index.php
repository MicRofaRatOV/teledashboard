<?php

error_reporting(E_ERROR | E_PARSE);

require "functions.php";
require "msg.php";

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
    include '../html/photo.html';
}
