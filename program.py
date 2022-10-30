import network
from time import sleep
from machine import Pin
from lib import send_response,not_found
hotspot=network.WLAN(network.AP_IF)
wifi=network.WLAN(network.STA_IF)
def program(conn,url):
  print("Show list program")
  with open("/www/head.html",'r') as f:
    html=str(f.read().format("List program"))
  with open("/program.txt",'r') as f:
    list_program=[str(x) for x in f.read().split("\n")]
  with open("/www/list_program.html",'r') as f:
    for i in list_program:
      html+=str(f.read().format(str(i)))
  send_response(conn,html)
  try:
    del html,list_program
  except:
    pass
def hello_world(conn,url):
  send_response(conn,"Hello world!")
