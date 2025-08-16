from machine import Pin, I2C, ADC
import utime
import dht
from pico_i2c_lcd import I2cLcd   # needs lcd_api.py + pico_i2c_lcd.py

# =====================
# I2C LCD Setup
# =====================
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
I2C_ADDR = i2c.scan()[0]   # auto-detect LCD address
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)  # 2 rows, 16 cols

# =====================
# DHT11 Setup
# =====================
dht_pin = Pin(15, Pin.IN, Pin.PULL_UP)
dht_sensor = dht.DHT11(dht_pin)

# =====================
# LDR Setup (ADC0 -> GP26)
# =====================
ldr = ADC(Pin(26))

# =====================
# Helper Function
# =====================
def display_line(row, text):
    """Clear a row and print text safely"""
    lcd.move_to(0, row)
    lcd.putstr(" " * 16)        # clear row
    lcd.move_to(0, row)
    lcd.putstr(text)

# =====================
# Main Loop
# =====================
lcd.move_to(0, 0)
lcd.putstr("Weather--Station")
lcd.move_to(0, 1)
lcd.putstr("------LMES------")
utime.sleep(10)
lcd.clear()
        
while True:
    try:
        # Read DHT11
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        # Read LDR (inverted to % light)
        ldr_val = ldr.read_u16()
        light_percent = 100 - ((ldr_val / 65535) * 100)

        # Debug print
        print("Temp:{}C  Hum:{}%  Light:{:.1f}%".format(temp, hum, light_percent))

        # Update LCD
        display_line(0, "Temp:{}C Hum:{}%".format(temp, hum))
        display_line(1, "  Light:{:.1f}%".format(light_percent))

    except Exception as e:
        print("Error:", e)

    utime.sleep(2)


