#Alumnos:
# Motocanchi Huanca, Elvis David
# D'Aragona Agustin Alejandro

import Adafruit_DHT
import time

class Temperatura:
    def __init__(self, pin=17, sensor= Adafruit_DHT.DHT11):
        self._sensor = sensor
        self._data_pin = pin

    def datos_sensor(self):
      humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
      return {'temperatura': temperatura, 'humedad': humedad, 'fecha': time.ctime()}

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class Matriz:
    def __init__(self, numero_matrices=2, orientacion=0, rotacion=0, ancho=8, alto=8):
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width= ancho, height= alto, cascaded= numero_matrices, rotate= rotacion)
    
    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        show_message(self.device, msg, fill= "white",font= proportional(self.font[font]),scroll_delay= delay)

import RPi.GPIO as GPIO

class Sonido:   
    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        # Desactivo las warnings por tener más de un circuito en la GPIO
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)
        
    def evento_detectado(self, funcion, datos):
        if GPIO.event_detected(self._canal):
            funcion(datos)
