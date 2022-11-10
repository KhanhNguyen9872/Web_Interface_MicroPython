print("Booting...")
import gc,config,network
from machine import Pin,freq,reset
freq(160000000)
hotspot=network.WLAN(network.AP_IF)
wifi=network.WLAN(network.STA_IF)
try:
  print("Starting hotspot ["+config.ap_name+"]"+" ["+config.ap_password+"]")
  hotspot.config(essid=str(config.ap_name),password=str(config.ap_password),channel=int(config.ap_channel),hidden=0)
  hotspot.ifconfig((str(config.ap_web_ip),str(config.ap_subnet),str(config.ap_gateway),str(config.ap_dns)))
except:
  pass
hotspot.active(True)
z={}
from lib import *
from lib2 import *
from program import *
from car import *
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
def process(conn,ssid,password):
  if str(wifi.isconnected())=="True":
    with open("/www/already_connect.html",'r') as f:
      response=f.read().format(ssid,wifi.config('essid'))
  else:
    timeout=int(config.timeout)*4
    print("Connecting to {}...".format(ssid))
    wifi.active(False)
    wifi.active(True)
    wifi.connect(ssid,password)
    count=0
    while str(wifi.isconnected())=="False":
      sleep(0.24)
      Pin(2,Pin.IN)
      count+=1
      sleep(0.24)
      Pin(2,Pin.OUT)
      if count==timeout:
        break
    if int(count)==int(timeout):
      timeout=int(timeout/4)
      Pin(2,Pin.IN)
      print("TIMEOUT {}s: {}".format(str(timeout),ssid))
      with open("/www/cannot_connect.html",'r') as f:
        response=f.read().format(ssid,str(timeout))
    else:
      Pin(2,Pin.OUT)
      print("SUCCESS!")
      write_file(ssid,password)
      with open("/www/connected.html",'r') as f:
        response=f.read().format(ssid,wifi.ifconfig()[0],wifi.ifconfig()[1],wifi.ifconfig()[2],wifi.ifconfig()[3],"/","Home")
  return response
def wifi_scanning(conn,wifi):
  print("Searching wifi...")
  list_wifi_tuple=[x for x in wifi.scan()]
  wifi_name=[x[0].decode('utf-8') for x in list_wifi_tuple]
  wifi_signal=[x[3] for x in list_wifi_tuple]
  wifi_hidden=[x[5] for x in list_wifi_tuple]
  del list_wifi_tuple
  print("Completed wifi search!")
  with open("/www/head_find_wifi.html",'r') as f:
    response=f.read()
  for i in range (0,len(wifi_name),1):
    if (wifi_hidden[i]==0):
      with open("/www/wifi_select.html",'r') as f:
        response+=f.read().format(wifi_name[i],wifi_signal[i],i)
  with open("/www/button_find_wifi.html",'r') as f:
    response+=f.read()
  del wifi_hidden
  return wifi_name,wifi_signal,response