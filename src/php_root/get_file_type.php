<?php

require_once 'vars.php';
require_once 'functions.php';

error_reporting(E_ERROR | E_PARSE);

$link = "/qwerty"; #$_POST['link']; # "/qwerty"

echo get_page_type(normalize_link($link));
