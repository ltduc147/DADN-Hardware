from event_manager import *
import sys
import uselect
from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from aiot_rgbled import RGBLed
from aiot_lcd1602 import LCD1602
import time
from machine import Pin, SoftI2C
from aiot_dht20 import DHT20

event_manager.reset()

def read_terminal_input():
  spoll=uselect.poll()        # Set up an input polling object.
  spoll.register(sys.stdin, uselect.POLLIN)    # Register polling object.

  input = ''
  if spoll.poll(0):
    input = sys.stdin.read(1)

    while spoll.poll(0):
      input = input + sys.stdin.read(1)

  spoll.unregister(sys.stdin)
  return input

tiny_rgb = RGBLed(pin1.pin, 4)

def on_event_timer_callback_R_U_G_S_L():
  global Cmd, Temperature, pump, Humidity, mode, Time, Soil_Moisture, min2, max2
  Cmd = read_terminal_input()
  if Cmd != '':
    if Cmd[0] == '0':
      mode = '0'
      Time = (int((Cmd[int(((Cmd.find(':') + 1) + 1) - 1) : ]))) + 1
      pin6.write_analog(round(translate(70, 0, 100, 0, 1023)))
      tiny_rgb.show(0, hex_to_rgb('#00ff00'))
      pump = '1'
    else:
      if Cmd[0] == '1':
        mode = '1'
        min2 = int((Cmd[int(((Cmd.find(':') + 1) + 1) - 1) : int((Cmd.rfind(':') + 1) - 1)]))
        max2 = int((Cmd[int(((Cmd.rfind(':') + 1) + 1) - 1) : ]))
        Time = 0
      else:
        if Cmd[-1] == '1':
          pin6.write_analog(round(translate(70, 0, 100, 0, 1023)))
          tiny_rgb.show(0, hex_to_rgb('#00ff00'))
          pump = '1'
        else:
          pin6.write_analog(round(translate(0, 0, 100, 0, 1023)))
          tiny_rgb.show(0, hex_to_rgb('#ff0000'))
          pump = '0'
          mode = '0'

event_manager.add_timer_event(500, on_event_timer_callback_R_U_G_S_L)

aiot_lcd1602 = LCD1602()

aiot_dht20 = DHT20(SoftI2C(scl=Pin(22), sda=Pin(21)))

def on_event_timer_callback_g_k_f_p_P():
  global Cmd, Temperature, pump, Humidity, mode, Time, Soil_Moisture, min2, max2
  aiot_dht20.read_dht20()
  Temperature = aiot_dht20.dht20_temperature()
  Humidity = aiot_dht20.dht20_humidity()
  Soil_Moisture = round(translate((pin0.read_analog()), 0, 4095, 0, 100))
  aiot_lcd1602.move_to(0, 0)
  aiot_lcd1602.putstr('T:')
  aiot_lcd1602.move_to(2, 0)
  aiot_lcd1602.putstr('    ')
  aiot_lcd1602.move_to(2, 0)
  aiot_lcd1602.putstr(Temperature)
  aiot_lcd1602.move_to(6, 0)
  aiot_lcd1602.putstr('*C')
  aiot_lcd1602.move_to(9, 0)
  aiot_lcd1602.putstr('H:')
  aiot_lcd1602.move_to(11, 0)
  aiot_lcd1602.putstr('    ')
  aiot_lcd1602.move_to(11, 0)
  aiot_lcd1602.putstr(Humidity)
  aiot_lcd1602.move_to(15, 0)
  aiot_lcd1602.putstr('%')
  print((''.join([str(x) for x in ['!T:', Temperature, '#']])), end =' ')
  print((''.join([str(x2) for x2 in ['!H:', Humidity, '#']])), end =' ')
  print((''.join([str(x3) for x3 in ['!SM:', Soil_Moisture, '#']])), end =' ')

event_manager.add_timer_event(15000, on_event_timer_callback_g_k_f_p_P)

def on_event_timer_callback_O_o_Z_V_K():
  global Cmd, Temperature, pump, Humidity, mode, Time, Soil_Moisture, min2, max2
  if mode == '0':
    if Time > 0 and pump == '1':
      Time = Time - 1
      aiot_lcd1602.move_to(0, 1)
      aiot_lcd1602.putstr('Time:')
      aiot_lcd1602.move_to(15, 1)
      aiot_lcd1602.putstr('s')
      aiot_lcd1602.move_to(10, 1)
      aiot_lcd1602.putstr('     ')
      aiot_lcd1602.move_to(10, 1)
      aiot_lcd1602.putstr(Time)
      if Time == 0:
        pin6.write_analog(round(translate(0, 0, 100, 0, 1023)))
        tiny_rgb.show(0, hex_to_rgb('#ff0000'))
  else:
    aiot_lcd1602.move_to(0, 1)
    aiot_lcd1602.putstr('                ')

event_manager.add_timer_event(1000, on_event_timer_callback_O_o_Z_V_K)

def on_event_timer_callback_G_J_y_Q_n():
  global Cmd, Temperature, pump, Humidity, mode, Time, Soil_Moisture, min2, max2
  if mode == '1':
    if Soil_Moisture < min2:
      pin6.write_analog(round(translate(70, 0, 100, 0, 1023)))
      tiny_rgb.show(0, hex_to_rgb('#00ff00'))
    if Soil_Moisture > max2:
      pin6.write_analog(round(translate(0, 0, 100, 0, 1023)))
      tiny_rgb.show(0, hex_to_rgb('#ff0000'))

event_manager.add_timer_event(15000, on_event_timer_callback_G_J_y_Q_n)

def on_button_a_pressed():
  global Cmd, Temperature, pump, Humidity, mode, Time, Soil_Moisture, min2, max2
  pin6.write_analog(round(translate(70, 0, 100, 0, 1023)))
  tiny_rgb.show(0, hex_to_rgb('#00ff00'))
  pump = '1'

button_a.on_pressed = on_button_a_pressed

def on_button_b_pressed():
  global Cmd, Temperature, pump, Humidity, mode, Time, Soil_Moisture, min2, max2
  tiny_rgb.show(0, hex_to_rgb('#ff0000'))
  pin6.write_analog(round(translate(0, 0, 100, 0, 1023)))
  pump = '0'

button_b.on_pressed = on_button_b_pressed

if True:
  display.scroll('AIOT')
  aiot_lcd1602.clear()
  tiny_rgb.show(0, hex_to_rgb('#ff0000'))
  pin6.write_analog(round(translate(0, 0, 100, 0, 1023)))
  mode = '0'
  Time = 0
  pump = '1'
  display.scroll('OK!')

while True:
  event_manager.run()
  time.sleep_ms(1000)
