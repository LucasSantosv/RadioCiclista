# Firmware Bluetooth

Programa principal: `firmware/bluetooth/RadioCiclista/RadioCiclista.ino`.

## Ambiente da primeira compilação

| Item | Versão/configuração registrada |
|---|---|
| Arduino ESP32 core | 3.3.11 |
| Placa | ESP32 Dev Module, ESP32 clássico |
| Partição | Huge APP, 3 MB de programa |
| ESP32-A2DP, Phil Schatzmann | 1.8.11 |
| audio-tools, Phil Schatzmann | 1.2.6 |
| Adafruit GFX + ST7735/ST7789 + BusIO | Instaladas; versões exatas não registradas no primeiro log |

Use Upload Speed 115200 se houver falha de comunicação. A seleção da porta deve corresponder à placa conectada. Não é necessário alterar o firmware para resolver erro de conexão do gravador.

O programa recebe Bluetooth A2DP, envia áudio por I²S (BCK=19, LRCK=25, DIN=26), configura APLL=false e deixa MCLK desabilitado. A biblioteca ajusta a taxa de saída à negociada com o celular. Bluetooth permanece uma transmissão comprimida; o DAC externo não cria áudio sem perdas.

Tela 240×320 em paisagem com `setRotation(3)`. Encoder: girar seleciona menu; PUSH abre. Na página Bluetooth, girar altera volume e PUSH envia play/pause. K0 retorna ao menu. O display só redesenha após mudanças, limitado a 10 atualizações/s.

O volume inicial é baixo, mas o celular pode sincronizar outro nível. A página BT OK confirma a conexão, não mede a saída física do DAC.

## Diagnóstico antigo

`firmware/diagnosticos/TESTE2_DAC_INTERNO/` é o teste histórico RADIO_TESTE2 com AnalogAudioStream e saídas analógicas GPIO25/26. Não usar esse diagnóstico como firmware do PCM5102A; ele exige a montagem analógica antiga.

## Preservação

O arquivo principal foi copiado sem alterações funcionais da versão validada pelo autor. Seu hash está em `docs/validacao.md`. Nenhuma nova compilação ou gravação foi realizada para organizar/publicar este repositório, conforme preferência do autor.
