import network,config
from time import sleep
from ure import search
from machine import Pin,reset
from os import uname
from lib2 import *
from program import *
import md5
hotspot=network.WLAN(network.AP_IF)
wifi=network.WLAN(network.STA_IF)
port=int(config.ap_web_port)
def settings(conn):
  print("Settings")
  with open("/www/settings.html",'r') as f:
    send_response(conn,str(f.read().format(config.ap_name,config.ap_password,config.ap_gateway,config.ap_subnet,config.ap_dns,config.ap_channel,config.ap_web_ip,config.ap_web_port,config.admin_pass,config.timeout,config.auto_connect)))
def save_settings(conn,request,url):
  memory_var=["ap_name","ap_password","ap_gateway","ap_subnet","ap_dns","ap_channel","ap_web_ip","ap_web_port","admin_passmd5","timeout","auto_connect"]
  number=["0","1","2","3","4","5","6","7","8","9"]
  url=[]
  for i in memory_var:
    try:
      match=search("{}=([^&]*)".format(i),request)
    except:
      response_error(conn,"Label {} is empty".format(i))
      return False
    try:
      id=str(match.group(1).decode("utf-8").replace("%3F","?").replace("%21","!"))
    except Exception:
      id=str(match.group(1).replace("%3F","?").replace("%21","!"))
    if id=="":
      response_error(conn,"Label {} is empty".format(i))
      return False
    else:
      if i=="ap_password" and ((len(id)<8) or (len(id)>63)):
        response_error(conn,"Password must be [8-63] characters")
        return False
      else:
        if i=="ap_gateway" or i=="ap_subnet" or i=="ap_web_ip":
          temp1=""
          temp=id
          for i in temp:
            if i in number:
              continue
            else:
              temp1+=i
          temp=temp.replace(".","")
          try:
            temp=int(temp)
            if str(temp1=="...")=="False":
              temp=int("k")
            del temp,temp1
          except:
            response_error(conn,"Your IP input is Error")
            return False
          url.append(id)
        elif i=="auto_connect":
          if id=="0" or id=="1":
            url.append(id)
          elif id.upper()=="FALSE" or id.upper()=="TRUE":
            url.append(id.upper())
          else:
            url.append("0")
        elif i=="admin_passmd5":
          if ((len(str(id))<3) or (len(str(id))>20)):
            response_error(conn,"Password must be [3-20] characters")
            return False
          else:
            real=id
            id=md5.digest(id)
            url.append(id)
            continue
        else:
          url.append(id)
  file=open("/config.py","w",encoding='utf-8')
  for i in range(0,len(memory_var),1):
    file.write("{}=\"{}\"\n".format(memory_var[i],url[i]))
    if memory_var[i]=="admin_passmd5":
      file.write("admin_pass=\"{}\"\n".format(real))
  file.close()
  print("Saved settings!")
  with open("/www/save_settings.html",'r') as f:
    send_response(conn,str(f.read()))
def process(conn,ssid,password):
  if str(wifi.isconnected())=="True":
    with open("/www/already_connect.html",'r') as f:
      response=str(f.read().format(ssid,wifi.config('essid')))
  else:
    timeout=int(int(config.timeout)*4)
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
      if int(count)==int(timeout):
        break
    if int(count)==int(timeout):
      timeout=int(timeout/4)
      Pin(2,Pin.IN)
      print("TIMEOUT {}s: {}".format(str(timeout),ssid))
      with open("/www/cannot_connect.html",'r') as f:
        response=str(f.read().format(ssid,str(timeout)))
    else:
      Pin(2,Pin.OUT)
      print("SUCCESS: {}\nIP: {}\nSubnet: {}\nGateway: {}\nDNS: {}".format(ssid,wifi.ifconfig()[0],wifi.ifconfig()[1],wifi.ifconfig()[2],wifi.ifconfig()[3]))
      write_file(ssid,password)
      with open("/www/connected.html",'r') as f:
        response=str(f.read().format(ssid,wifi.ifconfig()[0],wifi.ifconfig()[1],wifi.ifconfig()[2],wifi.ifconfig()[3],"/","Home"))
  return response
def verify_auth(conn,request,url,num,port):
  match=search("password=([^&]*)",request)
  if match is None:
    response_error(conn,"Admin password is empty!")
    return False
  try:
    password=str(match.group(1).decode("utf-8").replace("%3F","?").replace("%21","!"))
  except Exception:
    password=str(match.group(1).replace("%3F","?").replace("%21","!"))
  if len(password)==0:
    response_error(conn,"Admin password is empty!")
    return False
  print("Input Admin password: "+password)
  password=md5.digest(password)
  if password==config.admin_passmd5:
    try:
      if num==0:
        wifi.active(False)
        wifi.active(True)
        send_response(conn,"""<meta http-equiv='refresh'content='0;URL=/'>""")
      elif num==1:
        show_password(conn)
      elif num==2:
        del request,num,url
        settings(conn)
      elif num==3:
        print("Restart...")
        send_response(conn,"""<meta name="viewport"content="width=device-width,initial-scale=2">Restarting...""")
        sleep(1)
        reset()
      elif num==4:
        car_remote(conn,url,port)
    except NameError:
      password=""
      response_error(conn,"Authentication ERROR!")
  else:
    password=""
    print("Password ERROR")
    response_error(conn,"Authentication ERROR!")
  return password
