var temp = "";
var lightsOn = "";
var heaterOn = "";
var feederOn = "";

function fetchdata() {
	var request = new HMLHttpRequest();

	request.open('GET', "localhost/data.txt");
	request.onload = function(){
		var data = JSON.parse(request.responseText);
		temp = data["aquarium"][0];
		lightsOn = data["aquarium"][1];
		heaterOn = data["aquarium"][2];
		feederOn = data["aquarium"][3];
		document.getElementById('test').innerHTML = 
		"Temp: " +  temp + "<br>" +
		"Lights: " + lightsOn + "<br>" +
		"Heater: " + heaterOn + "<br>" +
		"Feeder: " + feederOn + "<br>";
	}
}