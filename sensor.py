import time
import board
import digitalio
import busio

from adafruit_seesaw.seesaw import Seesaw

i2c = board.I2C()
ss = Seesaw(i2c, addr=0x36)

while True:
    touch = ss.moisture_read()
    temp = ss.get_temp()
    print("temp: " + str(temp) + " moisture: " + str(touch))
    time.sleep(1)
