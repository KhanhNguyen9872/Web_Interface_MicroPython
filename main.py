while 1:
  try:
    gc.collect()
    Pin(2,Pin.IN)
    conn,addr=s.accept()
    Pin(2,Pin.OUT)
    conn.settimeout(None)
    request=b""
    try:
      while "\r\n\r\n" not in request:
        request+=conn.recv(512)
    except OSError:
      pass
    if "HTTP" not in request:
      conn.close()
      continue
    url=str(search_url(request))
    try:
      zz=url.split("!")
      if zz[1]==z[str(addr[0])]:
        exec(car_remote_dict[zz[0]])
        conn.close()
        continue
      else:
        int("")
    except:
      print("Accept: "+str(addr))
    print("URL: \"http://{}/{}\"".format(hotspot.ifconfig()[0],url))
    if url=="":
      if str(wifi.isconnected())=="True":
        if (first_boot==1 and auto_connect=="0") or (first_boot==1 and auto_connect.upper()=="FALSE"):
          wifi.active(False)
          first_boot=0
          wifi.active(True)
          with open("/www/not_connected.html",'r') as f:
            response=f.read()
        else:
          with open("/www/connected.html",'r') as f:
            response=f.read().format(wifi.config('essid'),wifi.ifconfig()[0],wifi.ifconfig()[1],wifi.ifconfig()[2],wifi.ifconfig()[3],"wifi_disconnect","Disconnect")
      else:
        first_boot=0
        with open("/www/not_connected.html",'r') as f:
          response=f.read()
      with open("/www/button_homepage.html",'r') as f:
        response+=f.read().format(uname()[1].upper())
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
      remove()
      try:
        response=process(conn,ssid,password)
        send_response(conn,response)
      except:
        not_found(conn,url)
    elif url=="program":
      program(conn,url)
    elif url=="show_password":
      remove()
      num=1
      auth(conn)
    elif url=="settings":
      remove()
      num=2
      auth(conn)
    elif url=="save_settings":
      save_settings(conn,request,url)
    elif url=="auth":
      remove()
      print("Verify auth...")
      try:
        k=verify_auth(conn,request,url,num,port,addr,z)
        if k!='':
          z[str(addr[0])]=k
      except NameError:
        not_found(conn,url)
    elif url=="info":
      remove()
      info_device(conn,request)
    elif url=="wifi_disconnect":
      num=0
      auth(conn)
    elif url=="restart":
      num=3
      auth(conn)
    elif url=="hello_world":
      hello_world(conn,url)
    elif url=="car_remote":
      num=4
      auth(conn)
    else:
      remove()
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
    continue

