# ADXL345をI2Cでアクセスするライブラリー
#
from machine import Pin, I2C
import utime
import ustruct

class  Mcp3425:
    def __init__(self):
        self.i2c = I2C(scl=Pin(14), sda=Pin(13), freq=100000)
        self.addr = 0x68
        self.i2c.writeto(self.addr, bytes([0x00]))

    def readAdc(self):
        self.i2c.writeto(self.addr, bytes([0x88]))
        while True:
            r = ustruct.unpack('>hB', self.i2c.readfrom(self.addr, 3)) # High byte, Low byte, Config Byte
            if r[1] & 0x80 == 0x00:
                break
        return r[0] * 62.5 # μV

ad = Mcp3425()
p5 = Pin(5, Pin.OUT)
p5.value(0)

while True:
    p5.value(1)
    utime.sleep_ms(10)
    print(ad.readAdc())
    p5.value(0)
    utime.sleep_ms(990)

if __name__ == '__main__':
    ad = Mcp3425()
    while True:
        print(ad.readAdc())
        utime.sleep(1)
