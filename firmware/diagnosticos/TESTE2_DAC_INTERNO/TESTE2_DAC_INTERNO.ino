// Teste minimo recuperado do chat. SOMENTE para a antiga montagem analogica.
// Nao usar como teste do PCM5102A: esta versao nao gera I2S externo.
#include <Arduino.h>
#include <AudioTools.h>
#include <BluetoothA2DPSink.h>
AnalogAudioStream audio;
BluetoothA2DPSink bluetooth(audio);
void setup() {
  Serial.begin(115200);
  delay(500);
  auto cfg = audio.defaultConfig(TX_MODE);
  cfg.sample_rate = 44100;
  cfg.channels = 2;
  cfg.bits_per_sample = 16;
  cfg.use_apll = false;
  audio.begin(cfg);
  bluetooth.start("RADIO_TESTE2");
  bluetooth.set_volume(18);
}
void loop() { delay(100); }
