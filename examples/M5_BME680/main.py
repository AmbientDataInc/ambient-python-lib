import machine
import utime
from m5stack import lcd
from bme680.i2c import I2CAdapter
import bme680
import ambient

i2c_dev = bme680.i2c.I2CAdapter(scl=machine.Pin(22), sda=machine.Pin(21))

sensor = bme680.BME680(i2c_device=i2c_dev, i2c_addr=0x77)
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

am = ambient.Ambient(100, '...writeKey...')

while True:
    lcd.clear()
    if sensor.get_sensor_data():
        output = "{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)
        lcd.print(output)
        print(output)
        r = am.send({'d1': sensor.data.temperature, 'd2': sensor.data.humidity, 'd3': sensor.data.pressure})
        print(r.status_code)
        r.close()
    utime.sleep(60)
