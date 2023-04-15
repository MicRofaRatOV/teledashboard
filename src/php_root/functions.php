<?php

require_once 'vars.php';

function main_page(): void
{
    $db = new SQLite3(__DIR__.DB_PATH."web.db");
    $result = $db->query("SELECT * from stat LIMIT 1");
    $row = $result->fetchArray(SQLITE3_ASSOC);
    $db->close();

    $user_count = $row["user_count"];
    $file_count = $row["file_count"];
    $version = $row["version"];

    include '../html/main_page.html';
}

function get_page_type($link): string
{
    $db = new SQLite3(__DIR__.DB_PATH."user.db");
    try
    {
        $key = get_selected_file($link);
        $result = $db->query("SELECT file_type from file WHERE status=0 AND key='" . $key . "'");
        $row = $result->fetchArray(SQLITE3_NUM)[0] ??= "";
        $db->close();
        return $row ?? "";
    }
    catch (Exception)
    {
        $db->close();
        return "";
    }
}

function get_selected_file($link): string
{
    $db = new SQLite3(__DIR__.DB_PATH."user.db");
    try {
        $result = $db->query("SELECT selected_file from user WHERE (link='" . $link . "'" . " OR " . "super_link='" . $link . "') AND activate_link=1");
        $row = $result->fetchArray(SQLITE3_NUM)[0];
        $db->close();
        return $row ?? "";
    }
    catch (Exception)
    {
        $db->close();
        return "";
    }
}

function normalize_link($link): string
{
    if ($link[-1] == "/"){
        # removing last slash
        $link = substr($link,0, -1);
    }
    # removing first slash
    return substr($link, -(strlen($link)-1), strlen($link)-1);
}
