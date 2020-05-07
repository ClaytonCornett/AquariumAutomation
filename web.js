var temp = "";
var lightsOn = "";
var heaterOn = "";
var feederOn = "";

	var request = new XMLHttpRequest();

	request.open('GET', "data.json");
	request.onload = function(){
		var data = JSON.parse(request.responseText);
		temp = data["aquarium"][0];
		console.log(temp)
		lightsOn = data["aquarium"][1];
		console.log(lightsOn)
		heaterOn = data["aquarium"][2];
		console.log(heaterOn)
		feederOn = data["aquarium"][3];
		console.log(feederOn)
		document.getElementById('test').innerHTML = 
		"Temp: " +  lightsOn;
		console.log("at the end")
	}

