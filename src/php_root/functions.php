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
        if (!is_int(to_int_or_null($id))){
            return "<font color='#dc143c'>Incorrect argument:</font> '$id'<br>";
        }

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

function to_int_or_null($v){
    if(is_int($v)) return $v;
    if(is_float($v)) return $v === (float)(int)$v ? (int)$v : null;
    if(is_numeric($v)) return to_int_or_null(+$v);
    return null;
}

function unban_by_id($arg) {
    $db = new SQLite3(__DIR__.DB_PATH."user.db");
    $return_msg = "";
    try {
        $arr = explode(" ", $arg);
        $arr_len = count($arr);

        for ($i = 0; $i < $arr_len; $i++) {
            if (is_int(to_int_or_null($arr[$i]))){
                $id = $arr[$i];
            } else {
                $return_msg .= "<font color='#dc143c'>Incorrect argument:</font> '$arr[$i]'<br>";
                continue;
            }
            $result = $db->query("SELECT ban FROM user WHERE id=$id")->fetchArray(SQLITE3_NUM)[0];
            if ($result == "") {
                $return_msg .= "<font color='#dc143c'>User not found: </font>'$id'<br>";
            } else if ($result == 0) {
                $return_msg .= "<font color='#b8860b'>User alredy unbanned: </font>'$id'<br>";
            } else {
                $db->query("UPDATE user SET ban=0 WHERE id=$id");
                $return_msg .= "<font color='green'>User unbanned: </font>'$id'. To return user status and link: <font color='#008b8b'>'undostatlink $id'</font><br>";
            }
        }
        $db->close();
        return $return_msg;
    }
    catch (Exception) {
        $db->close();
        return "<font color='#dc143c'>Incorrect argument</font>";
    }
}

function before_ban($arg) {
    $arr = explode(" ", $arg);
    if (!is_int(to_int_or_null($arr[0]))){
        return "<font color='#dc143c'>Incorrect argument</font>";
    } else {
        $id = $arr[0];
        if ($id < 1) {
            return "<font color='#dc143c'>Incorrect argument</font>";
        }
    }
    $db = new SQLite3(__DIR__.DB_PATH."user.db");
    $result = $db->query("SELECT * FROM before_ban WHERE id=$id");

    $count_id = $db->query("SELECT COUNT(id) FROM before_ban WHERE id=$id")->fetchArray(SQLITE3_NUM)[0];

    $return_msg = "";

    if ($count_id == 0) {
        $return_msg .= "<font color='#b8860b'>There are no ban history</font><br>";
    }

    for ($i = 0; $i < $count_id; $i++) {
        $row = $result->fetchArray(SQLITE3_ASSOC);
        $return_msg .= "<font color='#008b8b'>Entry </font>".($i+1).":<br>";
        foreach ($row as $key => $value) {
            if (is_string($value)) {
                $return_msg .= "<font color='#008b8b'>$key</font>='$value', ";
            } else if (is_null($value)){
                $return_msg .= "<font color='#1e90ff'>$key</font>=NULL, ";
            } else {
                $return_msg .= "<font color='green'>$key</font>=$value, ";
            }
        }
        $return_msg = substr($return_msg, 0, -2);
        $return_msg .= "<br>End<br>";
    }
    $db->close();
    return $return_msg;
}
