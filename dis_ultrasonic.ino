#include <NewPing.h>

#define TRIGGER_PIN  12
#define ECHO_PIN     13
#define MAX_DISTANCE 400 // Maximum distance we want to measure (in centimeters).


NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(50);                    // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.

  unsigned int time = sonar.ping();
  // float distance = sonar.ping_cm(); // Send ping, get distance in cm and print result (0 = outside set distance range)

  float distance = time / US_ROUNDTRIP_CM;
  delay(1000);
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println("cm");

  Serial.print("Time: ");
  Serial.print(time);
  Serial.println("ms");

  Serial.println();
}