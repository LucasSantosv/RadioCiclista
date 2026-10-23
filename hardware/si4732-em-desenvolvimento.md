# SI4732-A10 — montagem em desenvolvimento

**Não testado fisicamente no RadioCiclista.** O autor possui o CI solto e um cristal; a montagem e a escolha dos capacitores de carga ainda estão em andamento. Este esquema é para um primeiro teste em FM, com áudio do receptor ainda sem ligação.

| Pino | Nome | Destino proposto |
|---|---|---|
| 1 | LOUT/DFS | Áudio L reservado, deixar sem ligação nesta etapa |
| 2 | GPO3/DCLK | Resistor 2,2 kΩ → ponto A do cristal |
| 3 | GPO2/INTB | Sem ligação |
| 4 | GPO1 | Sem ligação |
| 5 | NC | Sem ligação |
| 6 | FMI | Capacitor 1 nF (102) em série → antena FM |
| 7 | RFGND | GND comum |
| 8 | AMI | Reservado à antena AM, sem ligação no teste FM |
| 9 | RST | GPIO14; resistor 10 kΩ entre o sinal e 3V3 |
| 10 | SENB | 3V3; endereço esperado 0x11 |
| 11 | SCLK | GPIO22; resistor 4,7 kΩ entre o sinal e 3V3 |
| 12 | SDIO | GPIO21; resistor 4,7 kΩ entre o sinal e 3V3 |
| 13 | RCLK | Ponto B do cristal |
| 14 | VDD | 3V3 do ESP32, nunca 5 V |
| 15 | GND | GND comum |
| 16 | ROUT/DOUT | Áudio R reservado, deixar sem ligação nesta etapa |

Numeração vista por cima: ponto do pino 1 à esquerda; 1 a 8 descendo à esquerda, 9 a 16 subindo à direita.

## Relógio e filtragem

Cristal passivo de 32,768 kHz entre A e B. O resistor de 2,2 kΩ fica entre o pino 2 e A. Um capacitor de carga liga A ao GND e outro liga B ao GND. Os 22 pF mostrados seguem o circuito de referência; a escolha final depende da carga especificada para o cristal e da capacitância parasita. Equivalências discutidas: dois de 10 pF em paralelo = 20 pF; dois de 47 pF em série = 23,5 pF, em cada lado. São candidatos para teste, não substituições medidas e validadas.

Entre pinos 14 e 15, próximos ao CI: 100 nF cerâmico e 10 µF em paralelo. Se o de 10 µF for polarizado, positivo no 14 e negativo no 15. Não ligar VDD diretamente ao GND.

[Esquema SVG](esquemas/SI4732A10_ESQUEMA_EXPANDIDO.svg) · [PNG](esquemas/SI4732A10_ESQUEMA_EXPANDIDO.png)

O desenho usa cruzamentos com arco para fios sem conexão e pontos pretos para conexões. Todos os GND são comuns. A entrada FM mostrada é de protótipo: proteção ESD, filtros e layout RF definitivos ainda não foram projetados.

## Áudio e limitações

Não unir LOUT/ROUT do SI4732 às saídas do PCM5102A. Falta escolher e montar a comutação de fontes. O SI4732 pode fornecer áudio analógico, com acoplamento adequado à entrada do amplificador. Usar sua saída digital exige outro planejamento: o modo digital não pode compartilhar o modo de oscilador com cristal passivo usado neste esquema. Ver referências da biblioteca e AN332.

O firmware atual apenas mostra um item de menu reservado para AM/FM/SW; não inicializa nem sintoniza o SI4732. Antena AM, sua indutância e o caminho de SW serão tratados depois.

## Referências e correção

- [PU2CLR: esquemas e pinagem SI4732](https://github.com/pu2clr/SI4735/tree/master/extras/schematic)
- [Proposta acadêmica de Amitav Mitra, Boston University](https://physics.bu.edu/adlab_and_elab/wp-content/uploads/2020/12/ELab_Project_Proposal.pdf): referência do circuito do cristal, antena e I²C. O texto atribui 0x11 a SENB no GND; para SI4732-A10, seguimos PU2CLR: SENB em 3V3 → 0x11; no GND → 0x63.
- [Skyworks AN383](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/application-notes/AN383.pdf)

Esquema redesenhado para esta montagem a partir das referências, sem republicar o PDF de terceiros.
