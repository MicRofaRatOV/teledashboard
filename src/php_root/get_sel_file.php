<?php

// TODO: antispam protection

error_reporting(E_ERROR | E_PARSE);

$uri = $_SERVER['REQUEST_URI'];

$link = $_POST['link'];

if ($link[-1] == "/" && $uri != "/"){
    # removing last slash
    $link = substr($link,0, -1);
}
# removing first slash
$link = substr($link,-(strlen($link)-1), strlen($link)-1);

$db = new SQLite3(__DIR__."/telegram/db/user.db");
try {
    $result = $db->query("SELECT selected_file from user WHERE link='" . $link . "'" . " OR " . "super_link='" . $link . "'");
    $row = $result->fetchArray(SQLITE3_NUM)[0];
    $db->close();
    echo $row ?? "";
}
catch (Exception)
{
    $db->close();
    echo "";
}

