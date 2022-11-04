global num
from lib import uname,response_error,send_response,write_file,info_device,show_password,process,auth,verify_auth,settings,save_settings,not_found,search,port,wifi
wifi.active(True)
hotspot.active(True)
from config import auto_connect
from program import program,hello_world
from lib2 import wifi_scanning,configure,search_url
try:
  import usocket as socket
except:
  import socket
first_boot=1
pass_key=0
print("Starting web [{0}:{1}]".format(hotspot.ifconfig()[0],str(port)))
try:
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  s.bind((hotspot.ifconfig()[0],port))
  s.listen(5)
except OSError as e:
  print("Restart...")
  machine.reset()
while 1:
  try:
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
      print('Close: '+str(addr))
      conn.close()
      continue
    conn.settimeout(None)
    url=str(search_url(request))
    print("URL: \"http://{}/{}\"".format(hotspot.ifconfig()[0],url))
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
            response=str(f.read().format(wifi.config('essid'),wifi.ifconfig()[0],wifi.ifconfig()[1],wifi.ifconfig()[2],wifi.ifconfig()[3],"wifi_disconnect","Disconnect"))
      else:
        first_boot=0
        with open("/www/not_connected.html",'r') as f:
          response=str(f.read())
      with open("/www/button_homepage.html",'r') as f:
        response+=str(f.read().format(uname()[1].upper()))
      send_response(conn,response)
    elif url=="khanhnguyen9872":
      try:
        ssid,password,response=configure(conn,request,url,wifi_name,wifi_signal)
        send_response(conn,response)
      except NameError:
        not_found(conn,url)
    elif url=="find_wifi":
      wifi_name,wifi_signal,response=wifi_scanning(conn,wifi)
      send_response(conn,response)
    elif url=="process":
      try:
        del wifi_name,wifi_signal
        response=process(conn,ssid,password)
        send_response(conn,response)
      except:
        not_found(conn,url)
    elif url=="program":
      program(conn,url)
    elif url=="show_password":
      try:
        del wifi_name,wifi_signal
      except:
        pass
      num=int(1)
      auth(conn)
    elif url=="settings":
      try:
        del wifi_name,wifi_signal
      except:
        pass
      num=int(2)
      auth(conn)
    elif url=="save_settings":
      save_settings(conn,request,url)
    elif url=="auth":
      print("Verify auth...")
      try:
        verify_auth(conn,request,url,num)
      except NameError:
        not_found(conn,url)
    elif url=="info":
      try:
        del wifi_name,wifi_signal
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
        del wifi_name,wifi_signal
      except:
        pass
      not_found(conn,url)
    print('Close: '+str(addr))
    conn.close()
  except ValueError as e:
    print("Error: "+str(e))
  except MemoryError as e:
    print("Error: "+str(e))
  except OSError:
    conn.close()
    print('Close: '+str(addr))
  except KeyboardInterrupt:
    print("Exiting...")
    break
  except:
    pass

