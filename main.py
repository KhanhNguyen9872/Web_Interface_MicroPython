def configure(conn,request,url):
  global ssid,password
  id=int(-1)
  match=search("ssid=([^&]*)",request)
  if match is None:
    not_found(conn,url)
    return False
  try:
    id=int(match.group(1).decode("utf-8").replace("%3F","?").replace("%21","!"))
  except Exception:
    id=int(match.group(1).replace("%3F","?").replace("%21","!"))
  if id==int(-1):
    not_found(conn,url)
    return False
  match=search("password=([^&]*)",request)
  if match is None:
    not_found(conn,url)
    return False
  try:
    password=str(match.group(1).decode("utf-8").replace("%3F","?").replace("%21","!"))
  except Exception:
    password=str(match.group(1).replace("%3F","?").replace("%21","!"))
  try:
    ssid=str(wifi_name[id])
  except:
    not_found(conn,url)
  del id
  print("Selected SSID: "+ssid)
  print("Input Password: "+password)
  with open("/www/selected_wifi.html",'r') as f:
    send_response(conn,str(f.read().format(str(ssid))))
wifi=network.WLAN(network.STA_IF)
wifi.active(True)
from lib import search_url,send_response,write_file,info_device,show_password,process,auth,verify_auth,settings,save_settings,not_found
from config import ap_web_port,auto_connect
from ure import search
from program import program,hello_world
from os import uname
try:
  import usocket as socket
except:
  import socket
global wifi_name,wifi_signal,wifi_security,port,num
first_boot=1
port=int(ap_web_port)
pass_key=0
print("Starting web [{0}:{1}]".format(str(hotspot.ifconfig()[0]),str(port)))
try:
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  s.bind(('',port))
  s.listen(5)
except OSError as e:
  machine.reset()
while 1:
  try:
    hotspot.active(True)
    wifi.active(True)
    gc.collect()
    Pin(2,Pin.IN)
    conn,addr=s.accept()
    Pin(2,Pin.OUT)
    conn.settimeout(3.0)
    print("Accept: "+str(addr))
    request=b""
    try:
      while "\r\n\r\n" not in request:
        request+=conn.recv(512)
    except OSError:
      pass
    if "HTTP" not in request:
      continue
    conn.settimeout(None)
    url=str(search_url(request))
    print("URL: \"{}\"".format(url))
    if url=="":
      if str(wifi.isconnected())=="True":
        if ((first_boot==1) and (str(auto_connect)=="0")) or ((first_boot==1) and (str(auto_connect.upper())=="FALSE")):
          wifi.active(False)
          first_boot=0
          wifi.active(True)
          with open("/www/not_connected.html",'r') as f:
            response=str(f.read())
        else:
          with open("/www/connected.html",'r') as f:
            response=str(f.read().format(wifi.config('essid'),str(wifi.ifconfig()[0]),str(wifi.ifconfig()[1]),str(wifi.ifconfig()[2]),str(wifi.ifconfig()[3]),str("wifi_disconnect"),str("Disconnect")))
      else:
        first_boot=0
        with open("/www/not_connected.html",'r') as f:
          response=str(f.read())
      with open("/www/button_homepage.html",'r') as f:
        response+=str(f.read().format(str(uname()[1].upper())))
      send_response(conn,response)
    elif url=="khanhnguyen9872":
      configure(conn,request,url)
    elif url=="find_wifi":
      print("Searching wifi...")
      list_wifi_tuple=[x for x in wifi.scan()]
      wifi_name=[x[0].decode('utf-8') for x in list_wifi_tuple]
      wifi_signal=[x[3] for x in list_wifi_tuple]
      wifi_hidden=[x[5] for x in list_wifi_tuple]
      del list_wifi_tuple
      print("Completed wifi search!")
      with open("/www/head_find_wifi.html",'r') as f:
        response=str(f.read())
      for i in range (0,len(wifi_name),1):
        if (wifi_hidden[i]==0):
          with open("/www/wifi_select.html",'r') as f:
            response+=str(f.read().format(wifi_name[i], wifi_signal[i], i))
      with open("/www/button_find_wifi.html",'r') as f:
        response+=str(f.read())
      send_response(conn,response)
      del response, wifi_hidden
    elif url=="process":
      try:
        del wifi_name, wifi_signal
        process(conn,ssid,password)
      except:
        not_found(conn,url)
    elif url=="program":
      program(conn,url)
    elif url=="show_password":
      try:
        del wifi_name, wifi_signal
      except:
        pass
      num=int(1)
      auth(conn)
    elif url=="settings":
      try:
        del wifi_name, wifi_signal
      except:
        pass
      num=int(2)
      auth(conn)
    elif url=="save_settings":
      save_settings(conn,request,url)
    elif url=="auth":
      try:
        print("Verify auth...")
        verify_auth(conn,request,url,num)
      except NameError:
        not_found(conn,url)
    elif url=="info":
      try:
        del wifi_name, wifi_signal
      except:
        pass
      info_device(conn,request)
    elif url=="wifi_disconnect":
      num=int(0)
      auth(conn)
    elif url=="restart":
      num=int(3)
      auth(conn)
    elif url=="hello_world":
      hello_world(conn,url)
    else:
      try:
        del wifi_name, wifi_signal
      except:
        pass
      not_found(conn,url)
    del addr
    print('Connection closed!')
    conn.close()
  except ValueError as e:
    print("Error: "+str(e))
  except MemoryError as e:
    print("Error: "+str(e))
  except OSError:
    conn.close()
    print('Connection closed!')
  except KeyboardInterrupt:
    print("Exiting...")
    break


