#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
//------ Added ----------------

#define valve1_pin 4                  //relay PIN
//-----------------------------


//-----------------------------------------------------
struct sensorData {
  int payload[1];
};

#define PACKET_SIZE sizeof(sensorData)

union LoRa_Packet {
  sensorData sensor;
  byte LoRaPacketBytes[PACKET_SIZE];
};

//now create a variable called levelinfo to hold the data
LoRa_Packet levelinfo;
//---------------------------------------------------------------------------------------------------
static const u1_t PROGMEM APPEUI[8] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
void os_getArtEui (u1_t* buf) {
  memcpy_P(buf, APPEUI, 8);
}

// This should also be in little endian format, see above.
static const u1_t PROGMEM DEVEUI[8] = { 0x20, 0x42, 0x05, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };
void os_getDevEui (u1_t* buf) {
  memcpy_P(buf, DEVEUI, 8);
}

// This key should be in big endian format (or, since it is not really a
// number but a block of memory, endianness does not really apply). In
// practice, a key taken from ttnctl can be copied as-is.
// The key shown here is the semtech default key.
static const u1_t PROGMEM APPKEY[16] = { 0xDD, 0x2C, 0x83, 0x8E, 0xAE, 0x6A, 0x9A, 0x71, 0xD1, 0xE8, 0x5A, 0x7F, 0xD7, 0x63, 0x5D, 0x48 };
void os_getDevKey (u1_t* buf) {
  memcpy_P(buf, APPKEY, 16);
}

static uint8_t mydata[] = "Hello, world!";
static osjob_t sendjob;

// Schedule TX every this many seconds (might become longer due to duty
// cycle limitations).
const unsigned TX_INTERVAL = 600;

const lmic_pinmap lmic_pins = {
  .nss = 10,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 9,
  .dio = {2, 6, 7},
};
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

      // Disable link check validation (automatically enabled
      // during join, but not supported by TTN at this time).
      LMIC_setLinkCheckMode(0);
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
        if (LMIC.dataLen == 1) {
          uint8_t result = LMIC.frame[LMIC.dataBeg + 0];
          if (result == 0)  {
            Serial.println("VALVE__1 is OFF ");
            digitalWrite(valve1_pin, LOW);
          }

          if (result == 1)  {
            Serial.println("VALVE__1 is ON ");
            digitalWrite(valve1_pin, HIGH);
            delay(2000);
            digitalWrite(valve1_pin, LOW);
          }

          if (result == 2)  {
            Serial.println("VALVE__1 is ON for 2 seconds");
            digitalWrite(valve1_pin, HIGH);
            delay(2000);
            digitalWrite(valve1_pin, LOW);
          }

          if (result == 3)  {
            Serial.println("VALVE__1 is ON for 10 seconds");
            digitalWrite(valve1_pin, HIGH);
            delay(10000);
            digitalWrite(valve1_pin, LOW);
          }

          levelinfo.sensor.payload[0] = valve1_pin ;


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
    // Prepare upstream data transmission at the next possible time.
    // LMIC_setTxData2(1, mydata, sizeof(mydata)-1, 0);

    
    //------------------------Added
LMIC_setTxData2(1, levelinfo.LoRaPacketBytes, sizeof(levelinfo.LoRaPacketBytes), 0);
//----------------------


    Serial.println(F("Packet queued 0"));
  }
  // Next TX is scheduled after TX_COMPLETE event.
}

void setup() {
  Serial.begin(115200);

  //------ Added ----------------
  pinMode(valve1_pin, OUTPUT);
  //-----------------------------


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

  // Let LMIC compensate for +/- 0.5% clock error
  LMIC_setClockError(MAX_CLOCK_ERROR * 0.5 / 100);


  // Start job (sending automatically starts OTAA too)
  do_send(&sendjob);
}

void loop() {
  os_runloop_once();
}
