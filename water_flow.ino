// ESP32 + YF-S201: يقرا التدفق وينشر JSON على MQTT. مفيش ذكاء هنا (الذكاء في الـ backend).
// المكتبات: PubSubClient. عدّلي config.h
#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"

WiFiClient wifi; PubSubClient mqtt(wifi);
volatile uint32_t pulses = 0;
void IRAM_ATTR onPulse() { pulses++; }

void connectAll() {
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  while (!mqtt.connected()) { if (!mqtt.connect(SENSOR_ID, MQTT_USER, MQTT_PASS)) delay(2000); }
}

void setup() {
  pinMode(FLOW_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), onPulse, FALLING);
  connectAll();
}

void loop() {
  if (!mqtt.connected()) connectAll();
  mqtt.loop();
  static uint32_t last = 0;
  if (millis() - last >= 1000) {
    noInterrupts(); uint32_t p = pulses; pulses = 0; interrupts();
    float lpm = (p / 7.5f);                 // YF-S201: ~7.5 pulses/s لكل L/min (راجعي الـ calibration)
    char buf[200];
    snprintf(buf, sizeof(buf),
      "{\"device_id\":\"%s\",\"sensor_type\":\"water_flow\",\"value\":%.2f,\"unit\":\"L/min\",\"timestamp\":\"%s\"}",
      SENSOR_ID, lpm, "1970-01-01T00:00:00Z");  // TODO: NTP للوقت الحقيقي (أو الـ bridge يختم الوقت)
    mqtt.publish("city/sensors/" SENSOR_ID, buf);
    last = millis();
  }
}
