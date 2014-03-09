var arDrone = require('ar-drone');
var client = arDrone.createClient();

client
  .after(10000, function() {
	      this.stop();
	          this.land();
		inFlight = false;
		    });


