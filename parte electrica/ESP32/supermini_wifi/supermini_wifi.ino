#include <WiFi.h>

// Escribe aqui el nombre y la contraseña de tu red Wi-Fi de casa
const char* ssid = "MIWIFI_B07C";
const char* password = "h35fZxP77CDEc4";

void setup() {
  Serial.begin(115200);
  delay(2000); // Espera a que el puerto USB este listo

  Serial.println();
  Serial.println("=========================================");
  Serial.print("Iniciando conexion a: ");
  Serial.println(ssid);

  // Modo cliente Wi-Fi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  // Intentando conectar... saldran puntitos mientras conecta
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("=========================================");
  Serial.println("�CONECTADO CON EXITO A TU RED WI-FI!");
  Serial.print("Direccion IP asignada: ");
  Serial.println(WiFi.localIP()); // La IP que le ha dado tu router
  Serial.print("Potencia de senal (RSSI): ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
  Serial.println("=========================================");
}

void loop() {
  // Mientras este conectado, nos avisa cada 5 segundos
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Conexion Wi-Fi activa y estable.");
  } else {
    Serial.println("Conexion perdida. Reconectando...");
    WiFi.reconnect();
  }
  delay(5000);
}
