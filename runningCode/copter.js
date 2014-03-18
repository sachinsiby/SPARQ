var arDrone = require('ar-drone');
var client = arDrone.createClient();
var FLIGHT_TIME = 30000;

var fs = require('fs');
var filepath = "image.png";

var inFlight = false;
var dir = 0;
var counter = 0;
var max = 3;
var imageNum = 0;

client.takeoff();

inFlight = true;

var pngStream = client.getPngStream();
pngStream.on('data', function(pngBuffer) {

			/*if(counter == max - 1) {
				fs.writeFile("/Users/z/copterImages/image"+imageNum+".png", pngBuffer, function(err) {
					if(err) {
						console.error("Error writing image file\n");
					}
				});
			}*/


			fs.writeFile(filepath, pngBuffer, function(err) {
				if(err) {
					console.error("Could not write file\n");
				}

				if(inFlight && counter >= max) {
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
	client.right(0);
	client.clockwise(0);
	client.counterClockwise(0);*/
	client.stop();
}


function directDrone(pngFile) {

	var sys = require('sys'),
    	    	  exec = require('child_process').exec;
			  
	exec('python utils.py', function(err, stdout, stderr) {
		var dir = parseInt(stdout);
		var rot = parseInt(stderr);

		console.log("Changing direction: " + dir + ", " + rot);

		resetMovement();
		
		if(dir == 0) {
			console.log("Left");
			client.left(0.04);
			if(rot == 0) {
				console.log(" (cw)");
				client.clockwise(0.03);
			} else {
				console.log(" (ccw)");
				client.counterClockwise(0.03);
			}
		} else if(dir == 1) {
			console.log("Front");
			client.front(0.03);
		} else if(dir == 2) {
			console.log("Right");
			client.right(0.04);
			if(rot == 0) {
				console.log(" (cw)");
				client.counterClockwise(0.03);
			} else {
				console.log(" (ccw)");
				client.clockwise(0.03);
			}
		} else if(dir ==3) {
			console.log("Back");
			client.back(0.03);
		} else if(dir == 4) {
			console.log("Up");
			client.up(0.03);
		} else if(dir == 5) {
			console.log("Down");
			client.down(0.03);
		}
	});
}
