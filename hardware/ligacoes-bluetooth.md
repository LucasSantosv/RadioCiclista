# Ligações atuais: Bluetooth, tela e PCM5102A

Base de referência: montagem que o autor informou estar funcionando com boa qualidade em 23/10/2026. Confira a variante física das placas antes de repetir as ligações.

| ESP32 | Destino |
|---|---|
| GPIO18 | ST7789 SCK/CLK |
| GPIO23 | ST7789 MOSI/SDA (SPI, não I²C) |
| GPIO16 | ST7789 CS |
| GPIO17 | ST7789 DC |
| GPIO13 | ST7789 RST |
| GPIO32 | Encoder A |
| GPIO33 | Encoder B |
| GPIO27 | Encoder PUSH |
| GPIO34 | Botão K0 |
| GPIO19 | PCM5102A BCK |
| GPIO25 | PCM5102A LCK/LRCK |
| GPIO26 | PCM5102A DIN |

Alimentação e iluminação da tela dependem de sua placa: o firmware não define GPIO para backlight. GPIO34 não possui pull-up interno; use o pull-up da placa ou resistor externo de 10 kΩ para 3,3 V, se ausente.

## DAC e amplificador

| PCM5102A roxo com regulador | Ligação |
|---|---|
| VIN | 5 V regulados (somente módulo com regulador identificado) |
| GND | GND comum do ESP32 e fonte |
| SCK | GND, sem MCLK externo |
| LOUT/LROUT, marcado L | Entrada L do HW-644 |
| ROUT, marcado R | Entrada R do HW-644 |
| AGND | GND da entrada do HW-644 |
| A3V3 | Sem ligação externa |

O CI PCM5102A trabalha com alimentação de 3,3 V; os 5 V se aplicam apenas à entrada VIN do módulo com regulador. Não aplicar 5 V em A3V3 nem nos GPIOs. Não alimentar o DAC com os 12 V do amplificador. A fonte, bateria, corrente e variantes físicas do conjunto ainda precisam de um BOM final medido; não foi publicado um projeto definitivo de alimentação.

| Jumper traseiro | Ponte |
|---|---|
| H1L / FLT | Centro com L |
| H2L / DEMP | Centro com L |
| H3L / XSMT | Centro com H |
| H4L / FMT | Centro com L |

H representa 3,3 V e L representa GND. Não unir os três pontos. Faça alterações com a alimentação desligada.

As antigas saídas analógicas dos GPIO25/26, com seus filtros e capacitores, devem ser retiradas antes de usar esses pinos como sinais digitais I²S. O P2 do PCM5102A é saída de linha e pode substituir L/R/AGND; não é saída para falantes passivos.

Cada falante permanece ligado ao par de saídas do seu canal no HW-644. Não usar L− ou R− como GND, nem unir canais. Comece com volume baixo; a saída de linha do DAC pode saturar a entrada de um amplificador de ganho alto.
