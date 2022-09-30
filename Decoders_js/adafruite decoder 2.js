//shows "Moisture_percentage" and ""Last_Valve_mode
function Decoder(bytes) {
      var data = {};
	data.Moisture_percentage =  bytes[0] ;
	data.Last_Valve_mode =  bytes[4]  ;
    return  data;
  }
