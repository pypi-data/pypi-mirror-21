FGPIO Lib  - A package for managing E/S of Raspberry pi or PCduino
           - Une librairie pour gerer les e/s d'un RPi ou d'un pcduino
========================================================================

This package allows to manage the following components with a Raspberry PI or pcduino
(Ce module permet de gerer les composants suivants avec un Raspberry PI ou un pcduino)

     -     Rpi or pcduino     with     rpiduino_io
     -     Bouton             with     bt_io
     -     Led                with     led_io
     -     lcd                with     lcd_io
     -     luminosity         with     lum_capteur_io
     -     max7219            with     max7219_io
     -     radio controlled plugs
                              with     rcSwitch_io et prises
     -     Ultrasonic distance sensor
                              with     UltraSonic_io
     -     DHT11 temperature sensor
                              with     dht11_io
     -     GPIO extension
                   MCP23017   with     mcp23017_io
                   PCA9555 (DF ROBOT DFR0013)
                              with     pca9555_io
     -     rotary encoder     with     rotary_encoder_io
     -     a menu on lcd and rotary encoder
                              with     f_menu
     -     CAN mcp3004/3008   with     mcp300x_io
	 -     temperature RF sensors
	                          with     rf_recept_io
	 -     servo motors       with     servo_motor_io
	 -     Gyroscope accelerometer MPU-6050
	                          with     mpu_6050_io
	 - 	   Detector qrd1114   with     qrd1114_io
	 -     CT sensor YHDC     with     SCT013_v_io
     -     HRLV max sonar sensor with  hrlv_max_sonar_io
	 -     Relays             with     relay_io
	 -     buzzer             with     buzz_io
	 -     rain_sensor        with     rain_sensor_io
	 -     Digital IR motion sensor 
	                          with     ir_detect_io
	 

All input component can be use with thread (see examples)

Installation :
     pip install FGPIO

Example :

from FGPIO.rpiduino_io import *
from FGPIO.led_io import *
pc = rpiduino_io()
led = led_io(pc.logical_pin(2))
led.on()

def action_bt_change():
	if bt.th_readed():
		print "bt Pushed."

bt = bt_io(pc.logical_pin(10), True, action_bt_change)