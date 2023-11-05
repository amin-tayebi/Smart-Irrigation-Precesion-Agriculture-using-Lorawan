#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include <SDI12.h>

#define relay_pin 3           //relay PIN
#define LED_pin 8

#define sensor_pin A7                // soil sensor PIN



/** Define the SDI-12 bus */
SDI12 mySDI12(4);



//-----------------------------------------------------
int p=0;
int x[13];

 struct sensorData {
  int payload[13];   // 6 payloads like 26.45  (26.45*100)
  // int humidity[6];  // 6 payloads like 0.004526  (0.004526*1000000)
  // int battery;         // 1 payload like 3.45  (3.45*100)
};

#define PACKET_SIZE sizeof(sensorData)

 union LoRa_Packet {
  sensorData sensor;
  byte LoRaPacketBytes[PACKET_SIZE];
};

//now create a variable called levelinfo to hold the data
LoRa_Packet levelinfo;

//------------------------------------------------------------
static const PROGMEM u1_t NWKSKEY[16] = { 0x5E, 0xCA, 0x65, 0xCD, 0xDC, 0x73, 0xA1, 0x7D, 0xA4, 0x5E, 0x92, 0x97, 0x27, 0x3F, 0xE0, 0x17 };

// LoRaWAN AppSKey, application session key
// This is the default Semtech key, which is used by the early prototype TTN
// network.
static const u1_t PROGMEM APPSKEY[16] = { 0x5B, 0x17, 0xCD, 0xAC, 0x51, 0x4F, 0xF1, 0x67, 0xF3, 0xB9, 0x8E, 0xCE, 0x16, 0xCA, 0xD9, 0x5B };

// LoRaWAN end-device address (DevAddr)
static const u4_t DEVADDR = 0x260B069C ; // <-- Change this address for every node!

// These callbacks are only used in over-the-air activation, so they are
// left empty here (we cannot leave them out completely unless
// DISABLE_JOIN is set in config.h, otherwise the linker will complain).
void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }

//static uint8_t mydata[] = "Hello, world!";
static osjob_t sendjob;

// Schedule TX every this many seconds (might become longer due to duty
// cycle limitations).
const unsigned TX_INTERVAL = 600;

// Pin mapping
const lmic_pinmap lmic_pins = {
  .nss = 10,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 9,
  .dio = {2, 6, 7},
};
//------------------------------------------------------------

char decToChar(byte i) {
  if (i < 10) return i + '0';
  if ((i >= 10) && (i < 36)) return i + 'a' - 10;
  if ((i >= 36) && (i <= 62))
    return i + 'A' - 36;
  else
    return i;
}

//------------------------------------------------------------------------functions


bool getResults(char i, int resultsExpected) {
  uint8_t resultsReceived = 0;
  uint8_t cmd_number      = 0;
  while (resultsReceived < resultsExpected && cmd_number <= 9) {
    String command = "";
    // in this example we will only take the 'DO' measurement
    command = "";
    command += i;
    command += "D";
    command += cmd_number;
    command += "!";  // SDI-12 command to get data [address][D][dataOption][!]
    mySDI12.sendCommand(command);

    uint32_t start = millis();
    while (mySDI12.available() < 3 && (millis() - start) < 1500) {}
    mySDI12.read();           // ignore the repeated SDI12 address
    char c = mySDI12.peek();  // check if there's a '+' and toss if so
    if (c == '+') {
      mySDI12.read();
    }

    while (mySDI12.available()) {
      char c = mySDI12.peek();
      if (c == '-' || (c >= '0' && c <= '9') || c == '.') {
        float result = mySDI12.parseFloat(SKIP_NONE);
        Serial.print(String(result, 4));
        // AT:-----------------------------------put result on the defined LIST-------Then print each payload with 6 digits after .---------------
        x[resultsReceived] = result * 1000;
        Serial.print("---->");
        Serial.print( x[resultsReceived]);
         Serial.println();
       levelinfo.sensor.payload[p] =  x[resultsReceived] ;
      
        // ---------------------------------------------------------
        if (result != -9999) {
          resultsReceived++;
//I added
            p++;
        }
      } else if (c == '+') {
        mySDI12.read();
        // Serial.print(", ");
      } else {
        mySDI12.read();
      }
      delay(10);  // 1 character ~ 7.5ms
    }
    if (resultsReceived < resultsExpected) {
      Serial.print(", ");
    }
    cmd_number++;
  }
  mySDI12.clearBuffer();

  return resultsReceived == resultsExpected;
}

bool takeMeasurement(char i, String meas_type = "") {
  mySDI12.clearBuffer();
  String command = "";
  command += i;
  command += "M";
  command += meas_type;
  command += "!";  // SDI-12 measurement command format  [address]['M'][!]
  mySDI12.sendCommand(command);
  delay(100);

  // wait for acknowlegement with format [address][ttt (3 char, seconds)][number of
  // measurments available, 0-9]
  String sdiResponse = mySDI12.readStringUntil('\n');
  sdiResponse.trim();

  String addr = sdiResponse.substring(0, 1);
  // Serial.print(addr);
  //Serial.print(", ");

  // find out how long we have to wait (in seconds).
  uint8_t wait = sdiResponse.substring(1, 4).toInt();
  // Serial.print(wait);
  //Serial.print(", ");

  // Set up the number of results to expect
  int numResults = sdiResponse.substring(4).toInt();
  // Serial.print(numResults);
  //Serial.print(", ");

  unsigned long timerStart = millis();
  while ((millis() - timerStart) < (1000 * (wait + 1))) {
    if (mySDI12.available())  // sensor can interrupt us to let us know it is done early
    {
      // Serial.print(millis() - timerStart);
      //  Serial.print(", ");
      mySDI12.clearBuffer();
      break;
    }
  }
  // Wait for anything else and clear it out
  delay(30);
  mySDI12.clearBuffer();

  if (numResults > 0) {
    return getResults(i, numResults);
  }

  return true;
}

//------------------------------------------------------------------------------------

void onEvent (ev_t ev) {
  Serial.print(os_getTime());
  Serial.print(": ");
  switch (ev) {
    case EV_SCAN_TIMEOUT:
      Serial.println(F("EV_SCAN_TIMEOUT"));
      break;
    case EV_BEACON_FOUND:
      Serial.println(F("EV_BEACON_FOUND"));
      break;
    case EV_BEACON_MISSED:
      Serial.println(F("EV_BEACON_MISSED"));
      break;
    case EV_BEACON_TRACKED:
      Serial.println(F("EV_BEACON_TRACKED"));
      break;
    case EV_JOINING:
      Serial.println(F("EV_JOINING"));
      break;
    case EV_JOINED:
      Serial.println(F("EV_JOINED"));
      break;
    case EV_RFU1:
      Serial.println(F("EV_RFU1"));
      break;
    case EV_JOIN_FAILED:
      Serial.println(F("EV_JOIN_FAILED"));
      break;
    case EV_REJOIN_FAILED:
      Serial.println(F("EV_REJOIN_FAILED"));
      break;
    case EV_TXCOMPLETE:
      Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
      if (LMIC.txrxFlags & TXRX_ACK)
        Serial.println(F("Received ack"));
      if (LMIC.dataLen) {
        Serial.println(F("Received "));
        Serial.println(LMIC.dataLen);
        Serial.println(F(" bytes of payload"));
        //------ Added ----------------
        uint8_t dnlink = LMIC.frame[LMIC.dataBeg + 0];
        if (dnlink == 0)  {
          Serial.println("LED off");
          digitalWrite(LED_pin, LOW);


        }
        if (dnlink == 1)  {
          Serial.println("LED on");
          digitalWrite(LED_pin, HIGH);
          delay(5000);
          digitalWrite(LED_pin, LOW);
        }
         if (dnlink == 2) {
            digitalWrite(LED_pin, HIGH);
          delay(20000);
          digitalWrite(LED_pin, LOW);
        }
        if (dnlink == 3) {
                    digitalWrite(relay_pin, HIGH);
          delay(10000);
          digitalWrite(relay_pin, LOW);
        }



        Serial.println();
        //-----------------------------

      }
      // Schedule next transmission
      os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(TX_INTERVAL), do_send);
      break;
    case EV_LOST_TSYNC:
      Serial.println(F("EV_LOST_TSYNC"));
      break;
    case EV_RESET:
      Serial.println(F("EV_RESET"));
      break;
    case EV_RXCOMPLETE:
      // data received in ping slot
      Serial.println(F("EV_RXCOMPLETE"));
      break;
    case EV_LINK_DEAD:
      Serial.println(F("EV_LINK_DEAD"));
      break;
    case EV_LINK_ALIVE:
      Serial.println(F("EV_LINK_ALIVE"));
      break;
    default:
      Serial.println(F("Unknown event"));
      break;
  }
}

void do_send(osjob_t* j) {
  // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND) {
    Serial.println(F("OP_TXRXPEND, not sending"));
  } else {
/*    // int moisture_value = analogRead(sensor_pin);
    int moisture_value = map(analogRead(sensor_pin), 680, 0, 100, 0);// map(output_value,550,10,0,100);   //map(analogRead(moisture_sensor), 330, 1023, 100, 0);
    Serial.print("Mositure : ");
    Serial.print(moisture_value);
    Serial.println("%");
*/
/*
takeMeasurement(decToChar(1), "4");
 takeMeasurement(decToChar(1), "");
 takeMeasurement(decToChar(1), "9");

 if (levelinfo.sensor.payload[0] < 26500 || levelinfo.sensor.payload[7] > 2 || levelinfo.sensor.payload[12] < 4800 )  {
     // Serial.println(levelinfo.sensor.payload[0]);
              //    Serial.println("Temperature is below 26.5 c");
                  digitalWrite(LED_pin, HIGH);
               delay(2000);
               digitalWrite(LED_pin, LOW);
                }
*/
  
 /*   if (moisture_value < 75) {
      digitalWrite(relay_pin, HIGH);
      //digitalWrite(LED_pin, HIGH);
      delay(3000);
      digitalWrite(relay_pin, LOW);
      // digitalWrite(LED_pin, LOW);
    }
    levelinfo.sensor.payload[0] = moisture_value ;
*/
    //  LMIC_setTxData2(1, mydata, sizeof(mydata)-1, 0);
  LMIC_setTxData2(1, levelinfo.LoRaPacketBytes, sizeof(levelinfo.LoRaPacketBytes), 0);
Serial.println();
    Serial.println(sizeof(levelinfo.LoRaPacketBytes));
    Serial.println(F("Packet queued"));
    
/* Serial.println(x[0]);
 Serial.println(x[1]);
 Serial.println(x[2]);
 Serial.println(x[3]);
 Serial.println(x[4]);
 Serial.println(x[5]);
 Serial.println(x[6]);
 Serial.println(x[7]);
 Serial.println(x[8]);
 Serial.println(x[9]);
 Serial.println(x[10]);
 Serial.println(x[11]);
 Serial.println(x[12]);
 Serial.println(x[13]);
 */
    
  }
  // Next TX is scheduled after TX_COMPLETE event.
}


//-----------------------------------------------------------------------------------------------

void setup() {
  Serial.begin(115200);
  //mySDI12.begin();
  //delay(500);  // allow things to settle

    // Power the sensors;
  if (22 > 0) {                                 /*!< The sensor power pin (or -1 if not switching power) */
   // Serial.println("Powering up sensors...");
    pinMode(22, OUTPUT);
    digitalWrite(22, HIGH);
    delay(200);
  }
    
  //----------------------------------- Set PIN 8 to output ----------------
  pinMode(relay_pin, OUTPUT);
   pinMode(LED_pin, OUTPUT);
   
    pinMode(sensor_pin, INPUT);
  //---------------------------------------------------------------------------------------
  Serial.println(F("Starting"));

#ifdef VCC_ENABLE
  // For Pinoccio Scout boards
  pinMode(VCC_ENABLE, OUTPUT);
  digitalWrite(VCC_ENABLE, HIGH);
  delay(1000);
#endif

  // LMIC init
  os_init();
  // Reset the MAC state. Session and pending data transfers will be discarded.
  LMIC_reset();

  // Set static session parameters. Instead of dynamically establishing a session
  // by joining the network, precomputed session parameters are be provided.
#ifdef PROGMEM
  // On AVR, these values are stored in flash and only copied to RAM
  // once. Copy them to a temporary buffer here, LMIC_setSession will
  // copy them into a buffer of its own again.
  uint8_t appskey[sizeof(APPSKEY)];
  uint8_t nwkskey[sizeof(NWKSKEY)];
  memcpy_P(appskey, APPSKEY, sizeof(APPSKEY));
  memcpy_P(nwkskey, NWKSKEY, sizeof(NWKSKEY));
  LMIC_setSession (0x1, DEVADDR, nwkskey, appskey);
#else
  // If not running an AVR with PROGMEM, just use the arrays directly
  LMIC_setSession (0x1, DEVADDR, NWKSKEY, APPSKEY);
#endif

#if defined(CFG_eu868)
  // Set up the channels used by the Things Network, which corresponds
  // to the defaults of most gateways. Without this, only three base
  // channels from the LoRaWAN specification are used, which certainly
  // works, so it is good for debugging, but can overload those
  // frequencies, so be sure to configure the full frequency range of
  // your network here (unless your network autoconfigures them).
  // Setting up channels should happen after LMIC_setSession, as that
  // configures the minimal channel set.
  // NA-US channels 0-71 are configured automatically
  LMIC_setupChannel(0, 868100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(1, 868300000, DR_RANGE_MAP(DR_SF12, DR_SF7B), BAND_CENTI);      // g-band
  LMIC_setupChannel(2, 868500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(3, 867100000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(4, 867300000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(5, 867500000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(6, 867700000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(7, 867900000, DR_RANGE_MAP(DR_SF12, DR_SF7),  BAND_CENTI);      // g-band
  LMIC_setupChannel(8, 868800000, DR_RANGE_MAP(DR_FSK,  DR_FSK),  BAND_MILLI);      // g2-band
  // TTN defines an additional channel at 869.525Mhz using SF9 for class B
  // devices' ping slots. LMIC does not have an easy way to define set this
  // frequency and support for class B is spotty and untested, so this
  // frequency is not configured here.
#elif defined(CFG_us915)
  // NA-US channels 0-71 are configured automatically
  // but only one group of 8 should (a subband) should be active
  // TTN recommends the second sub band, 1 in a zero based count.
  // https://github.com/TheThingsNetwork/gateway-conf/blob/master/US-global_conf.json
  LMIC_selectSubBand(1);
#endif

  // Disable link check validation
  LMIC_setLinkCheckMode(1);

  // TTN uses SF9 for its RX2 window.
  LMIC.dn2Dr = DR_SF9;

  // Set data rate and transmit power for uplink (note: txpow seems to be ignored by the library)
  LMIC_setDrTxpow(DR_SF7, 14);


// Let LMIC compensate for +/- 0.5% clock error
LMIC_setClockError(MAX_CLOCK_ERROR * 0.5 / 100);
  // Start job

  
  do_send(&sendjob);
}

void loop() {
  os_runloop_once();
}
