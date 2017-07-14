# 3軸加速度センサーADXL345で振動を測定、HDC1000で温度、湿度を測定し、
# Ambientで記録する

from micropython import mem_info
import utime
import adxl345
import hdc1000
import mcp3425
from machine import Pin, ADC
import math
import ambient

calibp = 100 # キャリブレーション間隔(m秒)
calibn = 10 # キャリブレーション回数

samplingp = 1000 # サンプリング間隔(m秒)
samplingn = 300 # サンプリング回数
sampling10 = 30 # サンプリング回数/10

mGperLSB = 3.9 # ADXL345 分解能 mG/LSB

# 100m秒間隔で10回、加速度を読み、キャリブレーション値にする
calib = [0, 0, 0]

def calibration():
    global calib
    c = [0, 0, 0]
    for var in range(calibn):
        a = ac.readAccel()
        c = [e1 + e2 for (e1, e2) in zip(c, a)]
        utime.sleep_ms(calibp)
    calib = list(map(lambda x:x/calibn, c))
    print(calib)

# 1秒間隔で300回(5分間)、加速度を読み、x、y、z、それぞれの
# 最大値と上から10%(30個目)の値を求める

def max10(a, v):
    a.append(v)
    a.sort(reverse=True)
    a.pop()

def do_connect(ssid, password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    # print('network config:', sta_if.ifconfig())

ac = adxl345.Adxl345()
calibration()
hdc = hdc1000.Hdc1000(2)
ad = mcp3425.Mcp3425()
p5 = Pin(5, Pin.OUT)
p5.value(0)
adc = ADC(0)

do_connect('...ssid...', '...password...')
am = ambient.Ambient(100, '...writeKey...')

while True:
    x = [0 for i in range(sampling10)]
    y = [0 for i in range(sampling10)]
    z = [0 for i in range(sampling10)]

    for var in range(samplingn):
        xyz = ac.readAccel()
        xyzc = [e1 - e2 for (e1, e2) in zip(xyz, calib)]
        max10(x, abs(xyzc[0]))
        max10(y, abs(xyzc[1]))
        max10(z, abs(xyzc[2]))
        utime.sleep_ms(samplingp)

    # print(x)
    # print(y)
    # print(z)

    RtodB = lambda R: math.log((R) * mGperLSB / 1000 * 9.80665 / 0.00001) / math.log(10) * 20

    X10 = RtodB(x[len(x) - 1])
    Y10 = RtodB(y[len(y) - 1])
    Z10 = RtodB(z[len(z) - 1])

    temp = hdc.readTemp()
    humid = hdc.readHumid()
    p5.value(1)
    utime.sleep_ms(10)
    lx = ad.readAdc() / 1000 * 2 # 負荷抵抗: 1kΩ、Lux = 2 * photocurrent(μA)
    p5.value(0)
    vb = adc.read() / 1024 / 20 * 120

    str = 'd1: %.1f, d2: %.1f, d3: %.1f, d4: %.1f, d5: %.1f, d6: %.1f, d7: %.1f' % (temp, humid, lx, X10, Y10, Z10, vb)
    print(str)

    r = am.send({'d1': temp, 'd2': humid, 'd3': lx, 'd4': X10, 'd5': Y10, 'd6': Z10, 'd7': vb})
    print(r.status_code)
    r.close()

    mem_info()
