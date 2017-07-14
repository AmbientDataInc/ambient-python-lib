# ADXL345をI2Cでアクセスするライブラリー
#
from machine import Pin, I2C
import ustruct

class  Adxl345:
    def __init__(self):
        self.i2c = I2C(scl=Pin(14), sda=Pin(13), freq=100000)
        self.addr = 0x53
        # self._writeReg(0x31, 0x0b)  # ±16g 最大分解能モード
        self._writeReg(0x31, 0x08)  # ±2g 最大分解能モード
        self._writeReg(0x2d, 0x00)
        self._writeReg(0x2d, 0x10)
        self._writeReg(0x2d, 0x08)  # 測定モード

    def devid(self):
        r = self._readReg(1, 0x00)
        return r

    def readAccel(self):
        r = self._readReg(6, 0x32)
        xyz = ustruct.unpack('hhh', r)
        return xyz

    def _writeReg(self, reg, data):
        self.i2c.writeto(self.addr, bytes([reg, data]))

    def _readReg(self, n, reg):
        self.i2c.writeto(self.addr, bytes([reg]))
        r = self.i2c.readfrom(self.addr, n)
        return r

if __name__ == '__main__':
    import time

    adxl = Adxl345()

    print(adxl.devid())

    while True:
        print(adxl.readAccel())
        time.sleep(1)
