from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W,H=1800,1640
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>']
font_path='C:/Windows/Fonts/arial.ttf'
def text(x,y,s,size=23,color='#182630',anchor='start'):
    font=ImageFont.truetype(font_path,size)
    a={'start':'lt','middle':'mt','end':'rt'}[anchor]
    d.text((x,y),s,font=font,fill=color,anchor=a)
    svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" dominant-baseline="text-before-edge">{escape(s)}</text>')
def line(x1,y1,x2,y2,color='#182630',width=3):
    d.line((x1,y1,x2,y2),fill=color,width=width)
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
def rect(x,y,w,h,color='#182630',width=2):
    d.rectangle((x,y,x+w,y+h),outline=color,width=width)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{color}" stroke-width="{width}"/>')
def dot(x,y):
    d.ellipse((x-5,y-5,x+5,y+5),fill='#182630')
    svg.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#182630"/>')
def gnd(x,y):
    line(x,y,x,y+15)
    for yy,ww in [(y+15,30),(y+23,20),(y+31,8)]:line(x-ww/2,yy,x+ww/2,yy)
def nc(x,y):
    line(x-6,y-6,x+6,y+6);line(x-6,y+6,x+6,y-6)
def resistor_h(x1,x2,y,label):
    m=(x1+x2)/2;line(x1,y,m-32,y);rect(m-32,y-12,64,24);line(m+32,y,x2,y)
    text(m,y-48,label,21,anchor='middle')
def cap_v(x,y1,y2,label):
    m=(y1+y2)/2;line(x,y1,x,m-7);line(x-20,m-7,x+20,m-7)
    line(x-20,m+7,x+20,m+7);line(x,m+7,x,y2)
    text(x+30,m-20,label,21)
def resistor_v(x,y1,y2,label):
    m=(y1+y2)/2;line(x,y1,x,m-28);rect(x-11,m-28,22,56);line(x,m+28,x,y2)
    text(x+25,m-16,label,21)

text(900,24,'SI4732-A10 + ESP32 — esquema do primeiro teste FM',35,anchor='middle')
text(900,76,'U1: vista superior, 16 pinos • Alimentação 3,3 V • Áudio do receptor reservado para a próxima etapa',23,anchor='middle')
rect(30,120,1740,650)
rect(650,155,500,580)
text(900,170,'U1 — SI4732-A10',26,anchor='middle')
dot(676,190)
left=['LOUT/DFS','GPO3/DCLK','GPO2/INTB','GPO1','NC','FMI','RFGND','AMI']
right=['ROUT/DOUT','GND','VDD','RCLK','SDIO','SCLK','SENB','RST']
ys=[230+i*65 for i in range(8)]
leftlabels=['Áudio L: sem ligação agora','CLK_OUT: ver cristal abaixo','Sem ligação','Sem ligação','Sem ligação (NC)','','','AM: sem ligação neste teste']
rightlabels=['Áudio R: sem ligação agora','GND comum','3V3 do ESP32','RCLK: ver cristal abaixo','SDA → GPIO21 do ESP32','SCL → GPIO22 do ESP32','3V3 (endereço I²C 0x11)','RESET → GPIO14 do ESP32']
for i,y in enumerate(ys):
    line(610,y,650,y);text(670,y-13,str(i+1),21);text(715,y-13,left[i],23)
    line(1150,y,1190,y);text(1130,y-13,str(16-i),21,anchor='end');text(1080,y-13,right[i],23,anchor='end')
    text(1210,y-13,rightlabels[i],23)
    if i not in (1,5,6):nc(610,y)
    if leftlabels[i]:text(590,y-13,leftlabels[i],23,anchor='end')
# Pin 6: RF coupling capacitor in series, NOT to ground.
y=ys[5];line(610,y,460,y);line(460,y-20,460,y+20);line(447,y-20,447,y+20);line(447,y,240,y)
line(240,y,240,y-50);line(215,y-75,240,y-50);line(265,y-75,240,y-50);line(215,y-75,265,y-75)
text(450,y+28,'C3: 1 nF (102), em série',21,anchor='middle');text(240,y-108,'ANT_FM',21,anchor='middle')
y=ys[6];line(610,y,540,y);gnd(540,y);text(505,y-10,'GND',22,anchor='end')
text(900,738,'Nomes iguais (3V3, GND, SDA, SCL, RESET, CLK_OUT e RCLK) representam a mesma ligação.',20,anchor='middle')

# Oscillator: resistor before node A; each load capacitor to ground.
rect(30,800,1000,360)
text(530,820,'Relógio: cristal passivo de 32,768 kHz',27,anchor='middle')
text(100,898,'CLK_OUT',22);text(100,926,'U1 pino 2',20)
resistor_h(100,360,990,'R1: 2,2 kΩ');dot(360,990);text(360,940,'A',22,anchor='middle')
line(360,990,500,990);line(500,965,500,1015);rect(515,970,30,40);line(560,965,560,1015)
line(500,990,515,990);line(545,990,560,990);line(560,990,730,990);dot(730,990)
line(730,990,930,990);text(915,898,'RCLK',22,anchor='end');text(915,926,'U1 pino 13',20,anchor='end')
text(530,914,'X1: 32,768 kHz',21,anchor='middle');text(730,940,'B',22,anchor='middle')
cap_v(360,990,1080,'C1: 22 pF');gnd(360,1080)
cap_v(730,990,1080,'C2: 22 pF');gnd(730,1080)
text(530,1125,'C1/C2: 22 pF ou associação equivalente; fios bem curtos.',21,anchor='middle')

# Supply rails: no direct VDD/GND connection.
rect(1050,800,720,360)
text(1410,820,'Desacoplamento junto ao CI',27,anchor='middle')
text(1090,892,'3V3 / U1 pino 14',22)
line(1090,945,1680,945);dot(1210,945);dot(1500,945)
cap_v(1210,945,1075,'C4: 100 nF');cap_v(1500,945,1075,'C5: 10 µF')
text(1530,958,'+',23)
line(1090,1075,1680,1075);dot(1210,1075);dot(1500,1075);gnd(1090,1075)
text(1390,1108,'GND / U1 pinos 15 e 7',22,anchor='middle')

# Pull-up network: each resistor connects 3V3 to its signal, never series in data path.
rect(30,1190,1740,285)
text(900,1210,'Resistores de pull-up — cada resistor entre o sinal e 3V3',27,anchor='middle')
for x,name,label in [(300,'SDA / GPIO21 / U1 pino 12','R2: 4,7 kΩ'),(850,'SCL / GPIO22 / U1 pino 11','R3: 4,7 kΩ'),(1400,'RESET / GPIO14 / U1 pino 9','R4: 10 kΩ')]:
    text(x,1255,'3V3',22,anchor='middle');resistor_v(x,1290,1390,label);dot(x,1390)
    text(x,1420,name,21,anchor='middle')
text(40,1500,'• Pino 10 (SENB) ligado a 3V3. Pinos 3, 4 e 5 ficam sem ligação.',23)
text(40,1538,'• Pino 8 (AMI) reservado para a antena AM. Pinos 1/16: áudio analógico L/R, sem ligação agora.',23)
text(40,1576,'• Não unir saídas de áudio do SI4732 às saídas do PCM5102A. Nunca alimentar U1 com 5 V.',23,color='#b00020')
svg.append('</svg>')
(OUT/'SI4732A10_ESQUEMA_FM.svg').write_text('\n'.join(svg),encoding='utf-8')
im.save(OUT/'SI4732A10_ESQUEMA_FM.png')
print('Esquema SVG e PNG gerados.')

