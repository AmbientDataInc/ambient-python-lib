# coding: utf-8

import wiringpi
import os
import struct

class Hdc1000:
    def __init__(self, addr, rdyPin):
        wiringpi.wiringPiSetup() #setup wiringpi

        self.i2c = wiringpi.I2C() #get I2C
        self.dev = self.i2c.setup(addr) #setup I2C device
        self.rdy = rdyPin

        wiringpi.pinMode(self.rdy, 0) # set ready pin to INPUT

        self.i2c.writeReg16(self.dev, 0x02, 0x0000) # Config reg を設定 MODE=0 温度、湿度をそれぞれ取り込む

    def readId(self):
        r = self.i2c.readReg16(self.dev, 0xfe) # read Manufacturer ID
        r = (r & 0xff) << 8 | (r >> 8) & 0xff
        return r

    def getTemp(self):
        self.i2c.writeReg8(self.dev, 0x00, 0x00)

        while wiringpi.digitalRead(self.rdy) == 1:
            pass

        data = struct.unpack('BB', os.read(self.dev, 2))
        temp = (data[0] << 8) | data[1]
        temp = temp * 165.0 / 65536.0 - 40.0
        return temp

    def getHumid(self):
        self.i2c.writeReg8(self.dev, 0x01, 0x00)

        while wiringpi.digitalRead(self.rdy) == 1:
            pass

        data = struct.unpack('BB', os.read(self.dev, 2))
        humid = (data[0] << 8) | data[1]
        humid = humid * 100.0 / 65536.0
        return humid
