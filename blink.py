from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)
print('Blinking LED Example')

def blink():
  while True:
    led.value(not led.value())
    sleep(0.5)