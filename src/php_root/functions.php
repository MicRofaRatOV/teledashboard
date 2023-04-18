<?php

require_once 'vars.php';

function main_page(): void
{
    global $tdb_version;
    $db = new SQLite3(__DIR__.DB_PATH."web.db");
    $result = $db->query("SELECT * FROM stat ORDER BY time DESC LIMIT 1");
    $row = $result->fetchArray(SQLITE3_ASSOC);
    $db->close();

    $user_count = $row["user_count"];
    $file_count = $row["file_count"];
    $version = $tdb_version;

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
        $result = $db->query("SELECT selected_file from user WHERE (link='" . $link . "'" . "  AND activate_link=1) OR " . "super_link='" . $link . "'");
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

function check_key($key): bool
{
    $db = new SQLite3(__DIR__.DB_PATH."web.db");
    try {
        $result = $db->query("SELECT key from key WHERE key='$key'");
        $row = $result->fetchArray(SQLITE3_NUM)[0];
        $db->close();
        if ($row == "") {
            return false;
        }
        return true;
    }
    catch (Exception)
    {
        $db->close();
        return false;
    }
}

function operation_to_log($key, $cmd, $arg, $ip): void
{
    $db = new SQLite3(__DIR__.DB_PATH."web.db");
    $db->query("INSERT INTO ap
    (key, time, command, arguments, ip)
    VALUES ('$key', ". time() .", '$cmd', '$arg', '$ip')");
    $db->close();
}

function get_ip() {
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        return $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        return $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else {
        return $_SERVER['REMOTE_ADDR'];
    }
}

function get_id_by_link($arg) {
    $db = new SQLite3(__DIR__.DB_PATH."user.db");
    try {
        $link = explode(" ", $arg)[0];
        $result = $db->query("SELECT id from user WHERE link='" . $link . "'" . " OR " . "super_link='" . $link . "'");
        $row = $result->fetchArray(SQLITE3_NUM)[0];
        $db->close();
        if ($row == "") {
            return "<font color='#b8860b'>ID not found</font>";
        }
        return "<font color='green'>ID is:</font> " . $row . "<br>" ?? "<font color='#b8860b'>ID not found</font>";
    }
    catch (Exception)
    {
        $db->close();
        return "<font color='#dc143c'>Incorrect argument</font>";
    }
}

function ban_by_id($arg) {
    $db = new SQLite3(__DIR__.DB_PATH."user.db");
    try {
        $arr = explode(" ", $arg);

        $id = $arr[0];

        // TODO: check incorrect enter (like: 'banid one hihihi')

        if (count($arr) > 1) {
            $reason = "";
            for ($i = 1; $i < count($arr); $i++) {
                $reason .= "$arr[$i] ";
            }
            $reason = substr($reason, 0, -1);
        } else {
            $reason = "no reason";
        }

        // Checking if already banned
        $result = $db->query("SELECT ban FROM user WHERE id=$id");
        $row = $result->fetchArray(SQLITE3_NUM)[0];
        if ($row == "") {
            return "<font color='#dc143c'>User doesnt exist!</font>";
        } else if ($row == 1) {
            return "<font color='#b8860b'>User alredy banned!</font>";
        }

        // Backuping
        $backup = $db->query("SELECT * FROM user WHERE id=$id")->fetchArray(SQLITE3_NUM);

        $backup_str = "";

        foreach ($backup as $row) {
            if (is_string($row)) {
                $backup_str .= "'".$row."', ";
            } else if (is_null($row)){
                $backup_str .= "NULL, ";
            } else {
                $backup_str .= $row.", ";
            }
        }

        $backup_str = substr($backup_str, 0, -2);

        try {
            $ban_id = $db->query("SELECT ban_id FROM before_ban ORDER BY ban_id DESC LIMIT 1")->fetchArray(SQLITE3_NUM)[0]+1;
        }
        catch (Exception)
        {
            $ban_id = 1;
        }

        if ($ban_id == ""){
            $ban_id = 1;
        }

        // Adding ban to log
        $db->query(" INSERT INTO before_ban VALUES ($ban_id, ".time().", '$reason', $backup_str) ");

        // Banning
        # "ban, activate_link, super_link, link, level", "1, 0, NULL, 'defalut', 0", f"id={db_id}"
        $db->query(" UPDATE user SET (ban, activate_link, super_link, link, level) =
        (1, 0, NULL, 'defalut', 0) WHERE id=$id");

        $db->close();
        return "User with ID: " . $id . " <font color='green'>successfully banned</font><br>";
    }
    catch (Exception)
    {
        $db->close();
        return "<font color='#dc143c'>Not found</font>";
    }
}