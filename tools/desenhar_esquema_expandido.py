from pathlib import Path

# Mesmo conjunto de primitivas para o SVG vetorial e sua visualização PNG.
helper = (Path(__file__).parent/'desenhar_esquema_si4732.py').read_text(encoding='utf-8-sig').split("text(900,24,")[0]
exec(helper.replace('W,H=1800,1640','W,H=2500,1650'))

def bridge_h(x1,x2,y,cross):
    line(x1,y,cross-14,y);line(cross+14,y,x2,y)
    d.arc((cross-14,y-14,cross+14,y+14),180,360,fill='#182630',width=3)
    svg.append(f'<path d="M {cross-14} {y} A 14 14 0 0 1 {cross+14} {y}" fill="none" stroke="#182630" stroke-width="3"/>')

text(1250,30,'SI4732-A10 — esquema expandido para ESP32',42,anchor='middle')
text(1250,95,'Todos os componentes desenhados junto às ligações do CI • Primeiro teste em FM',27,anchor='middle')
text(1250,150,'3V3 = pino 3V3 do ESP32. Todos os símbolos GND vão ao GND do ESP32.',26,anchor='middle')
rect(40,220,2420,1220)

# CI em vista superior: a geometria preserva os dois grupos de oito pinos.
rect(900,480,460,900)
text(1130,505,'U1 — SI4732-A10',27,anchor='middle');dot(925,552)
left=['LOUT/DFS','GPO3/DCLK','GPO2/INTB','GPO1','NC','FMI','RFGND','AMI']
right=['ROUT/DOUT','GND','VDD','RCLK','SDIO','SCLK','SENB','RST']
for i in range(8):
    y=600+100*i
    line(850,y,900,y);text(917,y-15,str(i+1),23);text(960,y-15,left[i],24)
    line(1360,y,1410,y);text(1343,y-15,str(16-i),23,anchor='end');text(1300,y-15,right[i],24,anchor='end')
for i in [0,2,3,4,7]:nc(850,600+100*i)
text(830,572,'Áudio L',22,anchor='end');text(830,604,'reservado',22,anchor='end')
for i,label in [(2,'Sem ligação'),(3,'Sem ligação'),(4,'Sem ligação (NC)'),(7,'AM: sem ligação agora')]:
    text(825,600+100*i-15,label,23,anchor='end')
nc(1410,600);text(1440,585,'Áudio R: reservado',24)

# Oscilador entre pinos 2 e 13. Cruzamentos com ponte NÃO se conectam.
line(850,700,820,700);resistor_h(650,820,700,'R1: 2,2 kΩ');line(600,700,650,700);dot(600,700)
line(600,700,600,590);line(577,590,623,590)
rect(584,545,32,30);line(577,530,623,530);line(600,575,600,590);line(600,530,600,545)
line(600,530,600,400);dot(600,400)
text(380,565,'X1',24,anchor='middle');text(380,600,'32,768 kHz',24,anchor='middle')
text(630,405,'B',22);text(630,710,'A',22)
line(400,400,600,400);cap_v(400,400,490,'C2: 22 pF');gnd(400,490)
line(400,700,600,700);cap_v(400,700,790,'C1: 22 pF');gnd(400,790)
line(600,400,1500,400);line(1500,400,1500,900);line(1410,900,1500,900)
text(1020,345,'Ligação direta do ponto B ao pino 13 (RCLK)',24,anchor='middle')

# GND pino 15 cruza o retorno do cristal SEM conexão, com ponte explícita.
bridge_h(1410,1650,700,1500);gnd(1650,700);text(1680,700,'GND',23)

# Alimentação pino 14 e dois capacitores em paralelo, sem curto entre trilhos.
bridge_h(1410,1800,800,1500);line(1800,800,1800,500)
line(1800,500,2330,500);text(2050,445,'3V3 do ESP32',26,anchor='middle')
dot(1900,500);dot(2200,500);cap_v(1900,500,650,'C4: 100 nF');cap_v(2200,500,650,'C5: 10 µF')
text(1930,605,'(104)',21);text(2230,515,'+',25)
line(1900,650,2330,650);dot(1900,650);dot(2200,650);gnd(2330,650)
text(2110,700,'C5: negativo (−) no GND',23,anchor='middle')

# SDA, SCL e RESET: ligação direta ao GPIO e resistor do sinal para 3V3.
for y,gpio,label,value,ref in [(1000,21,'SDA','4,7 kΩ','R2'),(1100,22,'SCL','4,7 kΩ','R3'),(1300,14,'RESET','10 kΩ','R4')]:
    line(1410,y,2240,y);dot(1850,y)
    # Símbolo de resistor vertical compacto, sem cruzar a linha anterior.
    line(1850,y-70,1850,y-59);rect(1839,y-59,22,42);line(1850,y-17,1850,y)
    text(1818,y-84,'3V3',21,anchor='end');text(1880,y-60,f'{ref}: {value}',23)
    text(2260,y-15,f'GPIO{gpio}',25)
    text(1590,y+18,label,21)
line(1410,1200,1670,1200);text(1700,1185,'3V3 — endereço I²C 0x11',24)

# Acoplamento da antena FM e terra de RF.
line(850,1100,520,1100);line(520,1075,520,1125);line(505,1075,505,1125)
line(505,1100,200,1100);line(200,1100,200,1020)
line(170,990,200,1020);line(230,990,200,1020);line(170,990,230,990)
text(200,940,'Antena FM',26,anchor='middle');text(510,1140,'C3: 1 nF (102)',23,anchor='middle')
line(850,1200,740,1200);gnd(740,1200);text(700,1200,'GND',23,anchor='end')

text(60,1475,'● Ponto preto em um fio = conexão. Cruzamento com uma ponte/arco = fios SEM conexão.',26)
text(60,1520,'C1 e C2: 22 pF ou associação equivalente. Mantenha cristal, R1, C1 e C2 com ligações curtas.',26)
text(60,1565,'Pinos 1 e 16: não ligar ao PCM5102A. U1 recebe SOMENTE 3,3 V; nunca 5 V.',26,color='#b00020')
svg.append('</svg>')
(OUT/'SI4732A10_ESQUEMA_EXPANDIDO.svg').write_text('\n'.join(svg),encoding='utf-8')
im.save(OUT/'SI4732A10_ESQUEMA_EXPANDIDO.png')
print('SVG e PNG do esquema expandido gerados.')

