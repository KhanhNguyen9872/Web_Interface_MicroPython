print("Booting...")
import uos,machine,network,gc,config
from machine import Pin
machine.freq(160000000)
hotspot=network.WLAN(network.AP_IF)
try:
  print("Starting hotspot ["+config.ap_name+"]"+" ["+config.ap_password+"]")
  hotspot.config(essid=str(config.ap_name),password=str(config.ap_password),channel=int(config.ap_channel),hidden=0)
  hotspot.ifconfig((str(config.ap_web_ip),str(config.ap_subnet),str(config.ap_gateway),str(config.ap_dns)))
except:
  pass
hotspot.active(True)
gc.collect()
from lib import *
wifi.active(True)
hotspot.active(True)
auto_connect=str(config.auto_connect)
from program import *
from lib2 import *
try:
  import usocket as socket
except:
  import socket
first_boot=1
pass_key=0
print("Starting web [{}:{}]".format(hotspot.ifconfig()[0],str(port)))
try:
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,50)
  s.bind((hotspot.ifconfig()[0],int(port)))
  s.listen(5)
except OSError as e:
  print("Restart...")
  machine.reset()
car_remote_dict={"up":"print(\"up\")","down":"print(\"down\")","left":"print(\"left\")","right":"print(\"right\")","end_up":"print(\"end_up\")","end_down":"print(\"end_down\")","end_left":"print(\"end_left\")","end_right":"print(\"end_right\")"}



