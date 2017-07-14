# LIS3DHをI2Cでアクセスするライブラリー
#
from machine import Pin, I2C
import ustruct

class  Lis3dh:
    def __init__(self):
        self.i2c = I2C(scl=Pin(14), sda=Pin(13), freq=100000)
        self.addr = 0x18
        if self.devid() != b'\x33':
            print('Envalid device')
        self._writeReg(0x20, 0x57) # CTRL_REG1, 100Hz, Nomal mode, XYZ enable
        self._writeReg(0x23, 0x88) # CTRL_REG4, BDU, High Resolution, ±2G

    def devid(self):
        r = self._readReg(1, 0x0f)
        return r

    def readAccel(self):
        while True:
            stat = ustruct.unpack('B', self._readReg(1, 0x27))[0] # STATUS_REG
            if stat & 0x08 == 0x08:
                break
        r = self._readReg(6, 0x28 | 0x80)
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

    RtoG = lambda R: round((R / 16000), 3)

    lis = Lis3dh()

    while True:
        xyz = lis.readAccel()
        xyz = list(map(RtoG, xyz))
        print(xyz)
        time.sleep(1)
