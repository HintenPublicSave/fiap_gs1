#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino.h>
#include <ArduinoJson.h>

// Essa aplicação tem o objetivo enviar alertas de enchentes através da utilização de 2 sensores
// Sensores: LDR (Nivel simulado), 
// Quando 2 ou mais sensores apontarem resultados negativos o relé do sistema de irrigação será acionado e o led irá acender
// Cado API Meteorológica. representada pelo Botão Vermelho, informe que que haverá chuva o sistema de irrigação será interrompido

// CONDIÇÃO NEGATIVA DE CADA SENSOR:
// LDR (Nivel simulador): Valor > 3000 (Aplicado um fator de divisão por 10, altura de agua em cm, vai de 0 a 400 e o LDR vai de 0 a 4000), 


// === DEFINIÇÃO DE PINOS ===
#define LDR_PIN 32        // Pino analógico para simular nivel de agua em bueiros via LDR
#define RELAY_PIN 4      // Relé que aciona a bomba
#define LED_PIN 2         // LED indicativo da bomba
#define BUTTON_API 18     // Botão de API Meteorológica (vermelho)
#define ECHO_PIN 25       // ECHO (Medição do comprimento de um pulso alto para obter a distância) HC-SR04 nível de água
#define TRIG_PIN 26       // TRIG (Pulso para iniciar a medição) HC-SR04 Nível de água
#define buzzer 23         // Buzzer de alerta

// conexão com a internet do simulador do wokwi
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const int canal_wifi = 6; // Canal do WIFI, na produção não mandar este parametro para ele fazer a varredura de canais automaticamente
const char* endpoint_api = "http://192.168.0.175:8180"; // URL da API para enviar os dados. Se estiver rodando localmente, precisa ser o IP do seu computador na rede local

void conectaWiFi() {
  WiFi.begin(ssid, password, canal_wifi);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
}

// o & significa que o objeto será passado por referência, ou seja, não será copiado, bom para economizar memória
void post_data(JsonDocument& doc) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(endpoint_api);

    String jsonStr;
    serializeJson(doc, jsonStr);
    int httpCode = http.POST(jsonStr);

    if (httpCode > 0) {
      Serial.println("Status code: " + String(httpCode));
      String payload = http.getString();
      Serial.println(payload);
    } else {
      Serial.println("Erro na requisição");
    }
    http.end();
  } else {
    Serial.println("Wifi desconectado, impossível fazer requesição!");
  }
}

// === OBJETO DO SENSOR HC-SR04 ===

// === VARIÁVEIS DE ESTADO DOS BOTÕES ===
bool estadoAPI = false;
bool ultimoEstadoAPI = HIGH;

void setup() {
  // Inicializa comunicação serial
  Serial.begin(115200);

  // Configuração da entrada e saída do sensor de nível
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Configuração dos pinos de entrada
  pinMode(BUTTON_API, INPUT_PULLUP);  // Botão da API

  // Configuração dos pinos de saída
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(buzzer, OUTPUT);
  ledcSetup(0, 2000, 8); // Configura o canal 0 do PWM para o buzzer (2kHz, 8 bits de resolução)
  ledcAttachPin(buzzer, 0); 

  conectaWiFi();

}

// Parâmetros do sensor de nível de água
float readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  int duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2;
}

void loop() {
  // === LEITURA E CONTROLE DE ESTADO DOS BOTÕES ===
  
  // Cria um objeto JSON dinâmico (RAM) com capacidade para 200 bytes
  
  JsonDocument doc;

  bool leituraAPI = digitalRead(BUTTON_API);
  bool LedValue = digitalRead(LED_PIN);
  bool BuzValue = digitalRead(buzzer);

  // Verifica mudança de estado do botão da API
  if (leituraAPI == LOW && ultimoEstadoAPI == HIGH) {
    estadoAPI = !estadoAPI; // Alterna o estado
    delay(200); // Debounce
  }
  ultimoEstadoAPI = leituraAPI;

  // Leitura do LDR (simulando Nível de Agua no Bueiro)
  int ldrValue = analogRead(LDR_PIN);  // Faixa de 0 a 4095 no ESP32


  // === CONDIÇÕES DE IRRIGAÇÃO ===


 // Verifica o sinal da API foi recebido
  bool resultadoAPI = !estadoAPI;

  // Nivel de água no bueiro ideal (simulado pelo LDR)
  bool nivelIdeal = (ldrValue > 3000);

  // Verifica se a aguá está no nível aceitável (> 3m)
  float distance = readDistanceCM();

  bool isNearby = distance > 300;
  //digitalWrite(LED_BUILTIN, isNearby);

  // Mostrar valores no Serial Monitor
  Serial.print("LDR (Nível Bueiro): "); Serial.print(ldrValue / 10.0); Serial.print("cm");
  Serial.print(" | Nível Leito: "); Serial.print(distance); Serial.print("cm");
  Serial.print(" | Relé (Envio de Dados): "); Serial.print(LedValue);
  Serial.print(" | API: "); Serial.println(estadoAPI);

  doc["bueiro"] = ldrValue / 10.0;
  doc["leito"] = distance;
  doc["rele"] = LedValue;

  serializeJsonPretty(doc, Serial);

  // === AÇÃO: ATIVAR BOMBA ===

  // Conta quantas variáveis estão com valor falso (condição crítica)
  int condicoesCriticas = 0;
  if (nivelIdeal) condicoesCriticas++;
  if (isNearby) condicoesCriticas++;

  // Caso pelo menos 1 dos sensores aponte nível elevado de água e a API acuse previsão de chuva o alerta será emitido
  if (condicoesCriticas >= 1) {
    Serial.println("ALERTA: Nível elevado de água detectado!");
    digitalWrite(RELAY_PIN, HIGH);  // Liga a bomba
    digitalWrite(LED_PIN, HIGH);    // Liga o LED indicativo

    // Toca a sequência de tons
    tone(buzzer, 261);
    delay(100);
    tone(buzzer, 293);
    delay(100);
    tone(buzzer, 329);
    delay(100);
    tone(buzzer, 349);
    delay(100);
    tone(buzzer, 392);
    delay(100);
    noTone(buzzer);
  } else {
    digitalWrite(RELAY_PIN, LOW);   // Desliga a bomba
    digitalWrite(LED_PIN, LOW);     // Desliga o LED
    noTone(buzzer);
  }

  post_data(doc);  // Envia os dados para a API

  delay(2000);  // Espera 1 segundo antes da próxima leitura
}
