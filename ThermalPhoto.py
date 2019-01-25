import os,sys
from ESCPOS import *
from PIL import Image

t = Thermal("/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0")

'''
t.textAling(1)
for x in range (10):
    t.println("Hola SOCIS")
t.cutPaper()
'''

im = Image.open("in.jpg")
print("Imprimiendo foto")
t.printOldBitmap(im)

for x in range(3):
    t.println("")
t.println("No puedes limpiar el radio si no estas en Madrid")
t.println("")
t.println("")
t.println("")
t.println("")
t.println("")
t.cutPaper()


print "Saliendo..."
t.close()
sys.exit(0)

