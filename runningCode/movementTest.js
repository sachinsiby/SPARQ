var arDrone = require('ar-drone');
var client = arDrone.createClient();
var FLIGHT_TIME = 60000;
var startTime = Date.now();
var stable = false;

client.takeoff(function() { console.log("Drone is now stable\n"); stable = true; });

while(!stable) {
	;
}

circumbabulate(8);

client
  .after(FLIGHT_TIME, function() {
	      this.stop();
	          this.land();
		    });


function circumbabulate(radius) {
	rotationSpeed = radius;
	time = 10 * 1000;
	iterations = 40;

	// Log function
	logRiseVal = 0.8;
	multiplier = rotationSpeed / Math.log(logRiseVal*(iterations+1));

	// Linear function
	divisor = rotationSpeed / iterations;

	// Quadratic function
	scaler = rotationSpeed / (iterations*iterations);

	client.left(0.09);
	for(i=1;i<iterations+1;i++) {
		(function(i) {
			//setTimeout(function() { turn((i*i) * scaler) }, i*(time/iterations));
			//setTimeout(function() { turn((i*rotationSpeed)/divisor) }, i*(time/iterations));
			setTimeout(function() { turn(multiplier * Math.log(logRiseVal*(i+1))) }, i*(time/iterations));
		})(i);
	}
	//turn(rotationSpeed/3);
	//setTimeout(function() { turn(rotationSpeed) }, 3000);
}

function turn(rotationSpeed) {
	console.log("("+Math.floor((Date.now()-startTime)/10)/100+") Turning clockwise with speed: " + rotationSpeed);
	client.clockwise(rotationSpeed*0.09);
}

