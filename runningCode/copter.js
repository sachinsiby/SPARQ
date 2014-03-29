var arDrone = require('ar-drone');
var client = arDrone.createClient();
//client.config('general:navdata_demo', 'FALSE');
var FLIGHT_TIME = 100000;

var fs = require('fs');
var filepath = "image.png";

var inFlight = false;
var dir = 0;
var counter = 0;
var max = 3;
var imageNum = 0;

var currDir = -1;
var prevRatio = 0;
var currRot = 0;

client.takeoff();

inFlight = true;

var pngStream = client.getPngStream();
pngStream.on('data', function(pngBuffer) {

			/*
			if(counter == max - 1) {
				fs.writeFile("/Users/z/copterImages/image"+imageNum+".png", pngBuffer, function(err) {
					if(err) {
						console.error("Error writing image file\n");
					}
				});
			}*/


			fs.writeFile(filepath, pngBuffer, function(err) {
				if(err) {
					console.error("Could not write file\n");
				} else if(inFlight && counter >= max) {
					directDrone(pngBuffer);
					counter = 0;
				}
			});
			imageNum++;
			counter++;
		});



client
  .after(FLIGHT_TIME, function() {
	      this.stop();
	          this.land();
		inFlight = false;
		    });


function resetMovement() {
	/*client.front(0);
	client.back(0);
	client.left(0);
	client.right(0);*/
	client.counterClockwise(0);
	client.clockwise(0);
	client.stop();
}


function directDrone(pngFile) {

	var sys = require('sys'),
    	    	  exec = require('child_process').exec;
			  
	exec('python utils.py', function(err, stdout, stderr) {
		var dir = parseInt(stdout);
		if(isNaN(dir)) {
			console.log("Error processing image");
			currDir = -1;
			resetMovement();
			return;
		}
		var rot = parseInt(stderr);

		if(dir == currDir) {
			return;
		}

		currDir = dir;

		console.log("Changing direction: " + dir + ", " + rot);

		resetMovement();

		if(dir==0) {
			client.counterClockwise(0.02);
		} else if(dir==1) {
			client.clockwise(0.02);
		} else if(dir==2) {
			if(rot < prevRatio) {
				console.log("Switched rotations for cmb");
				currRot = (~currRot) & (1);
				circumbabulate(4,currRot);
			} else {
				circumbabulate(4,currRot);
			}
			prevRatio = rot;
		} else if(dir==3) {
			client.left(0.02);
		} else if(dir==4) {
			client.right(0.02);
		} else if(dir==5) {
			client.front(0.04);
		} else if(dir==6) {
			client.stop();
			client.land();
			inFlight = false;
		}
	});
}



function circumbabulate(radius, dir) {
	rotationSpeed = radius;
	time = 10 * 1000;
	iterations = 40;

	// Log function
	logRiseVal = 0.2;
	multiplier = rotationSpeed / Math.log(logRiseVal*(iterations+1));

	// Linear function
	divisor = rotationSpeed / iterations;

	// Quadratic function
	scaler = rotationSpeed / (iterations*iterations);

	if(dir == 0) {
		client.left(0.03);
	} else {
		client.right(0.03);
	}
	for(i=1;i<iterations+1;i++) {
		(function(i) {
			//setTimeout(function() { turn((i*i) * scaler) }, i*(time/iterations));
			//setTimeout(function() { turn((i*rotationSpeed)/divisor) }, i*(time/iterations));
			setTimeout(function() { turn(multiplier * Math.log(logRiseVal*(i+1)), dir) }, i*(time/iterations));
		})(i);
	}
	//turn(rotationSpeed/3);
	//setTimeout(function() { turn(rotationSpeed) }, 3000);
}

function turn(rotationSpeed, dir) {
	if(dir==0) {
		client.clockwise(rotationSpeed*0.03);
	} else {
		client.counterClockwise(rotationSpeed*0.03);
	}
}

