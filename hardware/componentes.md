# Componentes por etapa

## Base Bluetooth com funcionamento relatado

| Quantidade | Componente | Observação |
|---:|---|---|
| 1 | ESP32 clássico DevKit | Compatível com Bluetooth Classic A2DP |
| 1 | Display ST7789 240×320 | Modo paisagem, rotação 3 |
| 1 | Encoder EC11 com PUSH | GPIO32/33/27 |
| 1 | Botão K0 | GPIO34; pull-up externo se necessário |
| 1 | PCM5102A estéreo | Módulo roxo com regulador e jumpers |
| 1 | Amplificador HW-644 | Modelo comercial informado pelo autor; CI/ganho ainda não confirmados por inspeção neste repositório |
| 2 | Alto-falantes reaproveitados da JBL Flip 4 | Impedância e potência não medidas/documentadas aqui |
| — | Fonte regulada e fiação | Projeto de alimentação definitivo pendente |

## Receptor FM em montagem, sem recepção validada

| Quantidade | Componente |
|---:|---|
| 1 | SI4732-A10 SOIC-16 |
| 1 | Cristal 32,768 kHz, carga a confirmar |
| 2 | Capacitores de carga de referência 22 pF, a ajustar ao cristal |
| 1 | Resistor 2,2 kΩ |
| 2 | Resistores 4,7 kΩ |
| 1 | Resistor 10 kΩ |
| 1 | Capacitor 100 nF (104) |
| 1 | Capacitor 10 µF |
| 1 | Capacitor 1 nF (102) para antena FM |
| 1 | Antena FM para o teste |

A lista de AM/SW, comutação de áudio, gabinete e desligamento controlado ainda será definida.
