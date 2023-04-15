<?php

include 'vars.php';

$name = $_POST['name'];
$email = $_POST['email'];
$link = $_POST['link'];
$file = $_POST['file'];
$text = $_POST['text'];

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $email = "-";
}

if ($link == "" and $file == "") {
    echo 'Empty report <br> <a href="/rp">Report page</a>';
} else {
    $date = new DateTimeImmutable();
    $db = new SQLite3(__DIR__.DB_PATH."report.db");
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ipv4 = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ipv4 = $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else {
        $ipv4 = $_SERVER['REMOTE_ADDR'];
    }
    $time = $date->getTimestamp();
    try
    {
        $db->query("INSERT or IGNORE INTO report
                    (name, email, link, file, text, ipv4, time) VALUES 
                    ('$name', '$email', '$link', '$file', '$text', '$ipv4', $time)");
        $result = $db->query("SELECT * FROM report ORDER BY id DESC LIMIT 1");
        $row = $result->fetchArray(SQLITE3_NUM)[0] ??= "";
        $db->close();
        echo "<b>Your report id: $row</b>" . "<br><br>" . "Name: " . $name . "<br>" . "Email: " . $email . "<br>" . "Link: " . $link . "<br>" . "File: " . $file . "<br>" . "Text: " . $text . "<br>";

    }
    catch (Exception)
    {
        $db->close();
        echo "Error";
    }
}

echo '<hr> <p><a href="/">Back to home page</a></p>';

