# coding: utf-8

from time import sleep
import hdc1000
import ambient

hdc1000 = hdc1000.Hdc1000(0x40, 7)
ambi = ambient.Ambient(100, "your_writeKey") # ご自分のチャネルID、ライトキーに置き換えてください

print 'Manufacturer ID: 0x%04x' % hdc1000.readId()

while True:
    temp = hdc1000.getTemp()
    humid = hdc1000.getHumid()
    print 'temp: %.1f, humid: %.1f' % (temp, humid)

    r = ambi.send({"d1": temp, "d2": humid})
    print 'Status code: %d' % r.status_code

    sleep(300)
