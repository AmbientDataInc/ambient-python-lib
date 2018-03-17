import machine
import utime
from m5stack import lcd
import bme280
import ambient

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
bme = bme280.BME280(i2c=i2c)
am = ambient.Ambient(100, '...writeKey...')

while True:
    lcd.clear()
    lcd.print(str(bme.values), 0, 0)
    print(bme.values)
    data = bme.read_compensated_data()
    r = am.send({'d1': data[0] / 100.0, 'd2': data[2] / 1024.0, 'd3': data[1] / 25600.0})
    print(r.status_code)
    r.close()

    utime.sleep(60)
