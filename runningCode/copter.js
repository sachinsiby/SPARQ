var arDrone = require('ar-drone');
var client = arDrone.createClient();
var FLIGHT_TIME = 20000;

var fs = require('fs');
var filepath = "image.png";

var inFlight = false;
var dir = 0;
var counter = 0;
var max = 2;
var imageNum = 0;

client.takeoff();

inFlight = true;

var pngStream = client.getPngStream();
pngStream.on('data', function(pngBuffer) {

			if(counter == max - 1) {
				fs.writeFile("copterImages/image"+imageNum+".png", pngBuffer, function(err) {
					if(err) {
						console.error("Error writing image file\n");
					}
				});
			}


			fs.writeFile(filepath, pngBuffer, function(err) {
				if(err) {
					console.error("Could not write file\n");
				}

				if(inFlight && counter == max) {
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


function directDrone(pngFile) {

	var sys = require('sys'),
    	    	  exec = require('child_process').exec;
			  
	exec('python utils.py', function(err, stdout, stderr) {
		var dir = parseInt(stdout);
		var rot = parseInt(stderr);
		
		client.after(1000, function() { console.log("Standby\n"); this.stop(); });

		if(dir == 0) {
			console.log("Left");
			client.left(0.12);
			if(rot == 0) {
				console.log(" (cw)");
				client.clockwise(0.1);
			} else {
				console.log(" (ccw)");
				client.counterClockwise(0.1);
			}
			console.log("\n");
		} else if(dir == 1) {
			console.log("Front\n");
			client.front(0.1);
		} else if(dir == 2) {
			console.log("Right");
			client.right(0.12);
			if(rot == 0) {
				console.log(" (cw)");
				client.counterClockwise(0.1);
			} else {
				console.log(" (ccw)");
				client.clockwise(0.1);
			}
			console.log("\n");
		} else if(dir ==3) {
			console.log("Back\n");
			client.back(0.1);
		} else if(dir == 4) {
			console.log("Up\n");
			client.up(0.1);
		} else if(dir == 5) {
			console.log("Down\n");
			client.down(0.1);
		}
	});
	//dir = (dir + 1) % 6;
}
