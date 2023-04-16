<?php

$link = $_GET['link'];

if ($link == "") {
    header('Location: '.'/wl');
    exit();
}
if (substr_count($link, "/") == 0) {
    header('Location: '.'/'.$link);
    exit();
} else {
    header('Location: '.'/wl');
    exit();
}