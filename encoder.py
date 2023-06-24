# import the required libraries
from machine import Pin, I2C
import utime, time
from ssd1306 import SSD1306_I2C
import framebuf

# counter for loop
counter = 0
rpm = 0

# declare the pin objects
EncoderPin = Pin(13, Pin.IN, Pin.PULL_DOWN)

WIDTH = 128
HEIGHT = 64

# i2c = I2C(1, scl = Pin(27), sda = Pin(26), freq=400000)
# 
# display = SSD1306_I2C(128, 64, i2c)

# interrupt handler function
def CountPulse(pin):
    global counter
    counter += 1
#     print("counter = ",counter)
#     print("Inside the interrupt handler function")

# attach the interrupt to the buttonPin
EncoderPin.irq(trigger = Pin.IRQ_RISING, handler = CountPulse)
prvMillsEn = 0
def GetSpeed():
    global prvMillsEn, counter
    nowMills = utime.ticks_ms()
    if nowMills - prvMillsEn >= 1000:
        prvMillsEn = nowMills
        rpm = (counter/20)*60
#         print('Số xung/s: ', counter)
        speed = (counter/20)*(0.025*3.14)
#         print('m/s: ', speed)
        counter = 0
#         print('RPM: ', rpm)
        return rpm
def ReadSpeed():
    speed = GetSpeed()
    formatted_speed = "{:.1f}".format(speed)
    string_speed = str("RPM: " + formatted_speed)
    print(string_speed)
    time.sleep(2)
    return string_speed

# 
# while True:
# #     display.text('Lat:',0,0)
# #     speed = ReadSpeed()
# #     display.text(speed,0,55)
# #     display.show()
# #     display.fill(0)
#     print(GetSpeed())
#     print(type(GetSpeed()))
#     utime.sleep(1)
#     

        
    