<?php

$servername = "localhost";
$dBusername = "root";
$dBPassword = "";
$dBName = "phpproject01";

$conn = mysqli_connect($servername, $dBusername, $dBPassword, $dBName);

if(!$conn) {
    die("Connection failed: ". mysqli_connect_error());
}