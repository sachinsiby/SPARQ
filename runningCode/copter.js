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

var searchDir = 0; // 0 is cw, 1 is ccw - means which dir to search if drone gets lost

var camera = "top";

client.takeoff();

inFlight = true;

client.config('video:video_channel', 0);

var pngStream = client.getPngStream();
pngStream.on('data', function(pngBuffer) {

			
			if(counter == max - 1) {
				fs.writeFile("/Users/z/copterImages/image"+imageNum+".png", pngBuffer, function(err) {
					if(err) {
						console.error("Error writing image file\n");
					}
				});
			}


			fs.writeFile(filepath, pngBuffer, function(err) {
				if(err) {
					console.error("Could not write file\n");
				} else if(inFlight && counter >= max) {
					if(camera == "top") {
						directDrone(pngBuffer, imageNum);
					}else if(camera == "bottom") {
						align(pngBuffer, imageNum);
					}
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


function directDrone(pngFile, imageNumUsed) {

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

		if(dir == currDir && ((dir == 2 && rot >= prevRatio) || (dir != 2))) {
			return;
		}

		currDir = dir;

		console.log("("+imageNumUsed+") Changing direction: " + dir + ", " + rot);

		resetMovement();

		if(dir==0) {
			client.counterClockwise(0.04);
		} else if(dir==1) {
			client.clockwise(0.06);
		} else if(dir==2) {
			if(rot < prevRatio) {
				console.log("Switched rotations for cmb");
				currRot = (~currRot) & (1);
				circumbabulate(8,currRot);
			} else {
				circumbabulate(8,currRot);
			}
			prevRatio = rot;
		} else if(dir==3) {
			client.left(0.04);
		} else if(dir==4) {
			client.right(0.04);
		} else if(dir==5) {
			client.front(0.06);
		} else if(dir==6) {
			client.stop();
			console.log("====SWITCHING TO BOTTOM CAMERA====");
			client.config('video:video_channel', 3);
			currDir = -1;
			max = 8;
			camera = "bottom";
		}
	});
}

function align(pngFile) {
	var sys = require('sys'),
	    	  exec = require('child_process').exec;

	exec('python align.py', function(err, stdout, stderr) {
		var dir = parseInt(stdout);
		if(isNaN(dir)) {
			console.log("Error processing image");
			currDir = -1;
			resetMovement();
			return;
		}

		/*if(dir == currDir) {
			return;
		}*/


		console.log("Changing direction: " + dir);

		//resetMovement();


		if(dir == 0) {
			client.clockwise(0.02);
		}else if(dir == 1) {
			client.counterClockwise(0.02);
		}else if(dir == 2) {
			client.front(0.08);
		}else if(dir == 3) {
			client.left(0.08);
		}else if(dir == 4) {
			client.right(0.08);
		}else if(dir == 5) {
			client.back(0.08);
		}else if(dir == 6) {
			if(currDir == dir) {
				console.log("****LANDING****");
				client.stop();
				client.land();
				inFlight = false;
			}
		}else if(dir == 7) {
			client.stop();
			console.log("====SWITCHING TO FRONT CAMERA====");
			client.config('video:video_channel', 0);
			currDir = -1;
			max = 3;
			camera = "top";
		}

		resetMovement();

		currDir = dir;
	});
}



function circumbabulate(radius, dir) {
	rotationSpeed = radius;
	time = 10 * 1000;
	iterations = 40;

	// Log function
	logRiseVal = 0.5;
	multiplier = rotationSpeed / Math.log(logRiseVal*(iterations+1));

	// Linear function
	divisor = rotationSpeed / iterations;

	// Quadratic function
	scaler = rotationSpeed / (iterations*iterations);

	if(dir == 0) {
		client.left(0.06);
	} else {
		client.right(0.06);
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
		client.clockwise(rotationSpeed*0.02);
	} else {
		client.counterClockwise(rotationSpeed*0.02);
	}
}

