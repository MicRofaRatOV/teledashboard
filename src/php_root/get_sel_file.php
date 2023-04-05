<?php

// TODO: antispam protection
require_once 'vars.php';
require_once 'functions.php';

error_reporting(E_ERROR | E_PARSE);

$link = $_POST['link']; # "/qwerty"

echo get_selected_file(normalize_link($link)); # /qwerty -> qwerty -> (md5)

