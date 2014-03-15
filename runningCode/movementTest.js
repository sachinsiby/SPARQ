var arDrone = require('ar-drone');
var client = arDrone.createClient();
var FLIGHT_TIME = 40000;
var startTime = Date.now();

client.takeoff();

client.stop();

client.after(5000, function() {
	circumbabulate(5);
});

client
  .after(FLIGHT_TIME, function() {
	      this.stop();
	          this.land();
		    });


function circumbabulate(radius) {
	multiplier = radius;
	client.left(0.09);
	for(i=1;i<7;i++) {
		(function(i) {
			//setTimeout(function() { turn(((i*i)*multiplier)/36) }, i*1000);
			setTimeout(function() { turn((i*multiplier)/6) }, i*1000);
		})(i);
	}
	//turn(multiplier/3);
	//setTimeout(function() { turn(multiplier) }, 3000);
}

function turn(multiplier) {
	console.log("("+Math.floor((Date.now()-startTime)/1000)+") Turning clockwise with speed: " + multiplier);
	client.clockwise(multiplier*0.09);
}

