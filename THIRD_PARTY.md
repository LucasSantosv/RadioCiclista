# Referências e componentes de terceiros

- [ESP32-A2DP](https://github.com/pschatzmann/ESP32-A2DP), Phil Schatzmann: recepção A2DP; licença do projeto upstream. Consulte também [Audio Output](https://github.com/pschatzmann/ESP32-A2DP/wiki/Audio-Output).
- [Arduino Audio Tools](https://github.com/pschatzmann/arduino-audio-tools), Phil Schatzmann: fluxo de áudio e I²S; licença upstream.
- [Adafruit GFX](https://github.com/adafruit/Adafruit-GFX-Library), [ST7735/ST7789](https://github.com/adafruit/Adafruit-ST7735-Library) e [BusIO](https://github.com/adafruit/Adafruit_BusIO): tela e barramentos; licenças upstream.
- [PU2CLR SI4735](https://github.com/pu2clr/SI4735), Ricardo Lima Caratti: referência de pinagem, circuitos e futura biblioteca para SI4732-A10. Não incorporada ao firmware Bluetooth.
- [Amitav Mitra / Boston University: proposta de receptor SI4732-A10](https://physics.bu.edu/adlab_and_elab/wp-content/uploads/2020/12/ELab_Project_Proposal.pdf): circuito de referência, incluindo cristal e antena. O esquema deste repositório é um redesenho para ESP32, com correção documentada de SENB.
- [Texas Instruments PCM5102A](https://www.ti.com/lit/ds/symlink/pcm5102a.pdf): DAC e requisitos elétricos.
- [Skyworks AN383](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/application-notes/AN383.pdf): antenas, layout e circuito SI47xx.

As bibliotecas não estão vendorizadas neste repositório. Instale-as de seus autores. Suas marcas, créditos e licenças permanecem com os respectivos titulares. A escolha GPLv3 para o código próprio não substitui licenças de terceiros.
