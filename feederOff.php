<?php 

$jsonString = file_get_contents('aqData.json');
$data = json_decode($jsonString, true);

$data['feederOff'] == "0";

$newJsonString = json_encode($data);
file_put_contents('aqData.json', $newJsonString);

?>