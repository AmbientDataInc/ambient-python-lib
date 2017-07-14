# coding: utf-8

from machine import Pin, I2C
import ustruct

class Hdc1000:
    def __init__(self, rdyPin):
        self.i2c = I2C(scl=Pin(14), sda=Pin(13), freq=100000)
        self.addr = 0x40
        self.rdy = Pin(rdyPin, Pin.IN)

        self._writeReg16(0x02, 0x00, 0x00) # Config reg を設定 MODE=0 温度、湿度をそれぞれ取り込む

    def devid(self):
        r = self._readReg(2, 0xfe)
        return r

    def readTemp(self):
        self._writeReg(0x00, 0x00)
        while self.rdy.value() == 1:
            pass

        r = ustruct.unpack('BB', self.i2c.readfrom(self.addr, 2))
        t = (r[0] << 8) | r[1]
        t = t * 165.0 / 65536.0 - 40.0
        return t

    def readHumid(self):
        self._writeReg(0x01, 0x00)
        while self.rdy.value() == 1:
            pass

        r = ustruct.unpack('BB', self.i2c.readfrom(self.addr, 2))
        h = (r[0] << 8) | r[1]
        h = h * 100.0 / 65536.0
        return h

    def _writeReg(self, reg, data):
        self.i2c.writeto(self.addr, bytes([reg, data]))

    def _writeReg16(self, reg, data0, data1):
        self.i2c.writeto(self.addr, bytes([reg, data0, data1]))

    def _readReg(self, n, reg):
        self.i2c.writeto(self.addr, bytes([reg]))
        r = self.i2c.readfrom(self.addr, n)
        return r

if __name__ == '__main__':
    hdc = Hdc1000(2)

    print(hdc.devid())

    print(hdc.readTemp())
    print(hdc.readHumid())
