import config,network,md5
from time import sleep
from ure import search
from machine import Pin,reset
from os import uname
from lib2 import *
from program import *
hotspot=network.WLAN(network.AP_IF)
wifi=network.WLAN(network.STA_IF)
port=int(config.ap_web_port)
def settings(conn):
  print("Settings")
  with open("/www/settings.html",'r') as f:
    send_response(conn,f.read().format(config.ap_name,config.ap_password,config.ap_gateway,config.ap_subnet,config.ap_dns,config.ap_channel,config.ap_web_ip,config.ap_web_port,config.admin_pass,config.timeout,config.auto_connect))
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
    id=h(match)
    if id=="":
      response_error(conn,"Label {} is empty".format(i))
      return False
    else:
      if i=="ap_password" and (len(id)<8 or len(id)>63):
        r(3)
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
              temp=int("")
            del temp,temp1
          except:
            response_error(conn,"Your IP input is Error")
            return False
        elif i=="auto_connect":
          if id=="0" or id=="1":
            pass
          elif id.upper()=="FALSE" or id.upper()=="TRUE":
            id=id.upper()
          else:
            id="0"
        elif i=="admin_passmd5":
          if (len(id)<3 or len(id)>20):
            r(2)
            return False
          else:
            real=id
            id=md5.digest(id)
    url.append(id)
  file=open("/config.py","w",encoding='utf-8')
  for i in range(0,len(memory_var)):
    file.write("{}=\"{}\"\n".format(memory_var[i],url[i]))
    if memory_var[i]=="admin_passmd5":
      file.write("admin_pass=\"{}\"\n".format(real))
  file.close()
  print("Saved settings!")
  with open("/www/save_settings.html",'r') as f:
    send_response(conn,f.read())
def verify_auth(conn,request,url,num,port,z):
  match=search("password=([^&]*)",request)
  if match is None:
    r(0)
    return False
  password=h(match)
  if len(password)==0:
    r(0)
    return False
  print("Input Admin password: "+password)
  password=md5.digest(password)
  if password==config.admin_passmd5:
    try:
      try:
        k=z[hotspot.ifconfig()[0]]
      except:
        k=random()
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
        with open("/www/restart.html",'r') as f:
          send_response(conn,f.read())
        sleep(1)
        reset()
      elif num==4:
        car_remote(conn,url,port,k)
        return k
    except NameError:
      r(1)
  else:
    print("Password ERROR")
    r(1)
  return ''
