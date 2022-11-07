from lib2 import *
import network,config
hotspot=network.WLAN(network.AP_IF)
def program(conn,url):
  print("Show list program")
  with open("/www/head.html",'r') as f:
    html=str(f.read().format("List program"))
  with open("/program.txt",'r') as f:
    list_program=[str(x) for x in f.read().replace("\r","\n").split("\n")]
  with open("/www/list_program.html",'r') as f:
    a=f.read()
  for i in list_program:
    html+=a.format(i)
  send_response(conn,html)
  remove()
def hello_world(conn,url):
  print("hello_world")
  send_response(conn,"Hello world!")
def car_remote(conn,url,port):
  print("car_remote")
  with open("/www/car_remote.html",'r') as f:
    send_response(conn,str(f.read()).replace("{0}",hotspot.ifconfig()[0]).replace("{1}",str(port)).replace("{2}",str(config.admin_passmd5)))

