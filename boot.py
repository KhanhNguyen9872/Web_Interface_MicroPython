print("Booting...")
import gc,config,network
from machine import Pin,freq,reset
freq(160000000)
hotspot=network.WLAN(network.AP_IF)
try:
  print("Starting hotspot ["+config.ap_name+"]"+" ["+config.ap_password+"]")
  hotspot.config(essid=str(config.ap_name),password=str(config.ap_password),channel=int(config.ap_channel),hidden=0)
  hotspot.ifconfig((str(config.ap_web_ip),str(config.ap_subnet),str(config.ap_gateway),str(config.ap_dns)))
except:
  pass
hotspot.active(True)
gc.collect()
z={}
from lib import *
from lib2 import *
from program import *
try:
  import usocket as socket
except:
  import socket
wifi.active(True)
hotspot.active(True)
auto_connect=str(config.auto_connect)
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
  reset()
def configure(conn,request,url,wifi_name,wifi_signal):
  id=int(-1)
  match=search("ssid=([^&]*)",request)
  if match is None:
    not_found(conn,url)
    return False
  id=h(match)
  if id==int(-1):
    not_found(conn,url)
    return False
  match=search("password=([^&]*)",request)
  if match is None:
    not_found(conn,url)
    return False
  password=h(match)
  if password=="" or len(password)>7:
    pass
  else:
    response_error(conn,"Password must be equal to or greater than 8. If your wifi is open, you must not enter the password dialog")
  ssid=wifi_name[int(id)]
  del id
  print("Selected SSID: "+ssid)
  print("Input Password: "+password)
  with open("/www/selected_wifi.html",'r') as f:
    response=f.read().format(str(ssid))
  return ssid,password,response
car_remote_dict={"up":"print(\"up\")","down":"print(\"down\")","left":"print(\"left\")","right":"print(\"right\")","end_up":"print(\"end_up\")","end_down":"print(\"end_down\")","end_left":"print(\"end_left\")","end_right":"print(\"end_right\")"}
