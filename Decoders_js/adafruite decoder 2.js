function Decoder(bytes) {
      var data = {};
	data.Moisture_percentage =  bytes[0] ;
	data.Valve_mode =  bytes[4]  ;
    return  data;
  }
