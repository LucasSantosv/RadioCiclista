/*
  RADIO ESP32 V1.2 - teste Bluetooth + PCM5102A
  Adaptado da V1.1 recuperada do chat "Comparar antenas para radio".
  ESP32 classico, ST7789 240x320, EC11, HW-644.
  BCK=19, LRCK=25, DIN=26. Remover o audio analogico antigo de 25/26!
  Nao gravar esta versao em ESP32-C3/S3 (nao possuem Bluetooth Classic).
*/
#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <AudioTools.h>
#include <BluetoothA2DPSink.h>

#if !defined(CONFIG_IDF_TARGET_ESP32)
#error "Selecione ESP32 Dev Module (ESP32 classico)."
#endif

#define TFT_CS 16
#define TFT_DC 17
#define TFT_RST 13
#define TFT_SCK 18
#define TFT_MOSI 23
#define ENC_A 32
#define ENC_B 33
#define ENC_PUSH 27
#define BTN_K0 34
#define I2S_BCK 19
#define I2S_LRCK 25
#define I2S_DIN 26

// 0 permite comparar o audio sem desenhar a tela, mantendo a mesma montagem.
#define USAR_TELA 1
const bool INVERTER_ENCODER = false;
const int PASSOS_ENCODER = 4;
const char* NOME_BT = "RADIO_PCM5102";

#define COR_FUNDO 0x0841
#define COR_CARTAO 0x18C3
#define COR_SELECAO 0x0456
#define COR_AZUL 0x05FF
#define COR_BRANCO 0xFFFF
#define COR_CINZA 0xAD55
#define COR_VERDE 0x07E0
#define COR_AMARELO 0xFFE0

Adafruit_ST7789 tft(TFT_CS, TFT_DC, TFT_RST);
I2SStream saidaAudio;
BluetoothA2DPSink bluetooth(saidaAudio);

enum TelaAtual { MENU_PRINCIPAL, TELA_BLUETOOTH, TELA_VOLUME, TELA_EM_BREVE };
TelaAtual telaAtual = MENU_PRINCIPAL;
int itemSelecionado = 0;
int volumeAtual = 10; // Inicio baixo; o celular pode sincronizar outro volume.
volatile bool btConectado = false;
volatile bool btTocando = false;
bool ultimoConectado = false, ultimoTocando = false;
bool atualizarTela = true;
const char* menuItens[] = {"Bluetooth", "Radio AM/FM/SW", "Radio Internet", "Volume"};
const int TOTAL_ITENS = 4;
uint8_t estadoAnteriorEncoder = 0;
int acumuladorEncoder = 0;
const int8_t tabelaEncoder[16] = {
  0,-1,1,0, 1,0,0,-1, -1,0,0,1, 0,1,-1,0
};
bool leituraAnteriorPush = HIGH, estadoEstavelPush = HIGH;
bool leituraAnteriorK0 = HIGH, estadoEstavelK0 = HIGH;
unsigned long tempoMudancaPush = 0, tempoMudancaK0 = 0;

void aoConectarBluetooth(esp_a2d_connection_state_t estado, void*) {
  btConectado = (estado == ESP_A2D_CONNECTION_STATE_CONNECTED);
  if (!btConectado) btTocando = false;
}
void aoMudarAudio(esp_a2d_audio_state_t estado, void*) {
  btTocando = (estado == ESP_A2D_AUDIO_STATE_STARTED);
}
int volumePorcentagem() { return volumeAtual * 100 / 127; }
void ajustarVolume(int mudanca) {
  volumeAtual = constrain(volumeAtual + mudanca * 4, 0, 127);
  bluetooth.set_volume((uint8_t)volumeAtual);
  atualizarTela = true;
}
void escrever(int x, int y, const char* mensagem, uint16_t cor, int tamanho = 2) {
  tft.setTextSize(tamanho); tft.setTextColor(cor);
  tft.setCursor(x,y); tft.print(mensagem);
}
void desenharCabecalho() {
  tft.fillRect(0,0,320,40,COR_CARTAO);
  escrever(12,12,"RADIO ESP32",COR_BRANCO);
  escrever(255,15,btConectado ? "BT OK" : "BT --",btConectado ? COR_VERDE : COR_CINZA,1);
  tft.drawFastHLine(0,40,320,COR_AZUL);
}
void desenharRodape(const char* mensagem) {
  tft.drawFastHLine(0,215,320,COR_CINZA);
  escrever(10,225,mensagem,COR_CINZA,1);
}
void desenharBarraVolume(int y) {
  tft.drawRoundRect(25,y,270,20,4,COR_BRANCO);
  int preenchimento = volumeAtual * 266 / 127;
  if (preenchimento > 0) tft.fillRect(27,y+2,preenchimento,16,COR_AZUL);
}
void desenharMenu() {
  for (int i=0;i<TOTAL_ITENS;i++) {
    int y = 49+i*39;
    tft.fillRoundRect(8,y,304,34,5,i==itemSelecionado ? COR_SELECAO : COR_CARTAO);
    if (i==itemSelecionado) escrever(13,y+9,">",COR_AZUL);
    escrever(32,y+9,menuItens[i],COR_BRANCO);
    if (i==1 || i==2) escrever(275,y+12,"...",COR_CINZA,1);
  }
  desenharRodape("GIRAR: MENU   PUSH: OK   K0: VOLTAR");
}
void desenharBluetooth() {
  escrever(15,52,"BLUETOOTH / PCM5102",COR_AZUL);
  escrever(15,85,"Nome: RADIO_PCM5102",COR_BRANCO,1);
  escrever(15,109,btConectado ? "Celular conectado" : "Aguardando celular",
           btConectado ? COR_VERDE : COR_AMARELO);
  if (btConectado) escrever(15,139,btTocando ? "Reproduzindo" : "Pausado",
                           btTocando ? COR_VERDE : COR_AMARELO);
  escrever(15,173,"Volume:",COR_BRANCO);
  tft.setCursor(215,173); tft.setTextSize(2); tft.setTextColor(COR_AZUL);
  tft.print(volumePorcentagem()); tft.print("%");
  desenharBarraVolume(193);
  desenharRodape("GIRAR: VOL  PUSH: PLAY/PAUSE  K0: MENU");
}
void desenharVolume() {
  escrever(28,60,"CONTROLE DE VOLUME",COR_BRANCO);
  tft.setCursor(90,107); tft.setTextSize(4); tft.setTextColor(COR_AZUL);
  tft.print(volumePorcentagem()); tft.print("%");
  desenharBarraVolume(170);
  desenharRodape("GIRAR: VOL  PUSH: VOLTAR");
}
void desenharEmBreve() {
  escrever(22,65,itemSelecionado==1 ? "RADIO AM/FM/SW" : "RADIO INTERNET",COR_AZUL);
  escrever(22,107,itemSelecionado==1 ? "Modulo SI4732" : "Conexao Wi-Fi",COR_BRANCO);
  escrever(22,155,"Em desenvolvimento",COR_AMARELO);
  desenharRodape("PUSH OU K0: VOLTAR");
}
void redesenhar() {
#if USAR_TELA
  tft.fillScreen(COR_FUNDO); desenharCabecalho();
  switch(telaAtual) {
    case MENU_PRINCIPAL: desenharMenu(); break;
    case TELA_BLUETOOTH: desenharBluetooth(); break;
    case TELA_VOLUME: desenharVolume(); break;
    case TELA_EM_BREVE: desenharEmBreve(); break;
  }
#endif
}
int lerEncoder() {
  uint8_t estado = (digitalRead(ENC_A)<<1) | digitalRead(ENC_B);
  if (estado != estadoAnteriorEncoder) {
    acumuladorEncoder += tabelaEncoder[(estadoAnteriorEncoder<<2) | estado];
    estadoAnteriorEncoder = estado;
  }
  int direcao = 0;
  if (acumuladorEncoder >= PASSOS_ENCODER) { direcao=1; acumuladorEncoder=0; }
  else if (acumuladorEncoder <= -PASSOS_ENCODER) { direcao=-1; acumuladorEncoder=0; }
  return INVERTER_ENCODER ? -direcao : direcao;
}
bool botaoPressionado(uint8_t pino, bool &anterior, bool &estavel, unsigned long &mudanca) {
  bool leitura = digitalRead(pino);
  unsigned long agora = millis();
  if (leitura != anterior) { mudanca=agora; anterior=leitura; }
  if (agora-mudanca >= 35 && leitura != estavel) {
    estavel=leitura;
    return estavel == LOW;
  }
  return false;
}
void processarGiro(int direcao) {
  if (!direcao) return;
  if (telaAtual == MENU_PRINCIPAL) {
    itemSelecionado = (itemSelecionado+direcao+TOTAL_ITENS)%TOTAL_ITENS;
    atualizarTela=true;
  } else if (telaAtual==TELA_BLUETOOTH || telaAtual==TELA_VOLUME) ajustarVolume(direcao);
}
void processarPush() {
  switch(telaAtual) {
    case MENU_PRINCIPAL:
      telaAtual = itemSelecionado==0 ? TELA_BLUETOOTH :
                  itemSelecionado==3 ? TELA_VOLUME : TELA_EM_BREVE;
      break;
    case TELA_BLUETOOTH:
      if (btConectado) { if (btTocando) bluetooth.pause(); else bluetooth.play(); }
      break;
    default: telaAtual=MENU_PRINCIPAL; break;
  }
  atualizarTela=true;
}
void setup() {
  Serial.begin(115200); delay(300);
  pinMode(ENC_A,INPUT_PULLUP); pinMode(ENC_B,INPUT_PULLUP);
  pinMode(ENC_PUSH,INPUT_PULLUP);
  pinMode(BTN_K0,INPUT); // GPIO34 exige pull-up EXTERNO se ausente na placa.
  estadoAnteriorEncoder=(digitalRead(ENC_A)<<1)|digitalRead(ENC_B);
  leituraAnteriorPush=estadoEstavelPush=digitalRead(ENC_PUSH);
  leituraAnteriorK0=estadoEstavelK0=digitalRead(BTN_K0);
#if USAR_TELA
  SPI.begin(TFT_SCK,-1,TFT_MOSI,TFT_CS);
  tft.init(240,320); tft.setRotation(3); tft.setTextWrap(false);
  tft.fillScreen(COR_FUNDO);
  escrever(20,90,"INICIANDO PCM5102",COR_AZUL);
#endif
  auto cfg=saidaAudio.defaultConfig(TX_MODE);
  cfg.sample_rate=44100; cfg.channels=2; cfg.bits_per_sample=16;
  cfg.pin_bck=I2S_BCK; cfg.pin_ws=I2S_LRCK; cfg.pin_data=I2S_DIN;
  cfg.pin_mck=-1; cfg.use_apll=false;
  if (!saidaAudio.begin(cfg)) {
    Serial.println("ERRO: I2S nao iniciou. Bluetooth nao sera iniciado.");
#if USAR_TELA
    tft.fillScreen(COR_FUNDO); escrever(20,90,"ERRO I2S",COR_AMARELO);
#endif
    while(true) delay(1000);
  }
  bluetooth.set_on_connection_state_changed(aoConectarBluetooth);
  bluetooth.set_on_audio_state_changed(aoMudarAudio);
  bluetooth.set_volume((uint8_t)volumeAtual);
  bluetooth.start(NOME_BT);
  Serial.println("RADIO ESP32 V1.2: BCK=19 LRCK=25 DIN=26, APLL=false");
  Serial.println("I2S iniciado; isto NAO confirma som na saida do DAC.");
}
void loop() {
  processarGiro(lerEncoder());
  if (botaoPressionado(ENC_PUSH,leituraAnteriorPush,estadoEstavelPush,tempoMudancaPush)) processarPush();
  if (botaoPressionado(BTN_K0,leituraAnteriorK0,estadoEstavelK0,tempoMudancaK0)) {
    telaAtual=MENU_PRINCIPAL; atualizarTela=true;
  }
  if (btConectado!=ultimoConectado || btTocando!=ultimoTocando) {
    ultimoConectado=btConectado; ultimoTocando=btTocando; atualizarTela=true;
    Serial.printf("Bluetooth conectado=%d reproduzindo=%d\n",ultimoConectado,ultimoTocando);
  }
  static unsigned long ultimaConsulta=0, ultimoDesenho=0;
  if (millis()-ultimaConsulta >= 250) {
    ultimaConsulta=millis();
    int novoVolume=bluetooth.get_volume();
    if (novoVolume!=volumeAtual) { volumeAtual=novoVolume; atualizarTela=true; }
  }
  // Sem desenho nos callbacks de audio; no maximo 10 atualizacoes/s, somente se mudou.
  if (atualizarTela && millis()-ultimoDesenho >= 100) {
    atualizarTela=false; redesenhar(); ultimoDesenho=millis();
  }
  delay(1);
}
