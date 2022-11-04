import network,config
from time import sleep
from ure import search
from machine import Pin,reset
from os import uname
from lib2 import head,last,response_error,write_file
hotspot=network.WLAN(network.AP_IF)
wifi=network.WLAN(network.STA_IF)
port=int(config.ap_web_port)
def settings(conn):
  print("Settings")
  with open("/www/settings.html",'r') as f:
    send_response(conn,str(f.read().format(str(config.ap_name),str(config.ap_password),str(config.ap_gateway),str(config.ap_subnet),str(config.ap_dns),str(config.ap_channel),str(config.ap_web_ip),str(config.ap_web_port),str(config.admin_password),str(config.timeout),str(config.auto_connect))))
def save_settings(conn,request,url):
  memory_var=["ap_name","ap_password","ap_gateway","ap_subnet","ap_dns","ap_channel","ap_web_ip","ap_web_port","admin_password","timeout","auto_connect"]
  number=["0","1","2","3","4","5","6","7","8","9"]
  url=[]
  for i in memory_var:
    try:
      match=search("{0}=([^&]*)".format(str(i)),request)
    except:
      response_error(conn,"Label {0} is empty".format(i))
      return False
    try:
      id=str(match.group(1).decode("utf-8").replace("%3F","?").replace("%21","!"))
    except Exception:
      id=str(match.group(1).replace("%3F","?").replace("%21","!"))
    if str(id)=="":
      response_error(conn,"Label {0} is empty".format(i))
      return False
    else:
      if (str(i)=="ap_password") and ((len(str(id))<8) or (len(str(id))>63)):
        response_error(conn,"Password must be [8-63] characters")
        return False
      else:
        if (str(i)=="ap_gateway") or (str(i)=="ap_subnet") or (str(i)=="ap_web_ip"):
          temp1=""
          temp=str(id)
          for i in temp:
            if str(i) in number:
              continue
            else:
              temp1+=str(i)
          temp=temp.replace(".","")
          try:
            temp=int(temp)
            if str(temp1=="...")=="False":
              temp=int("khanhnguyen9872")
            del temp,temp1
          except:
            response_error(conn,"Your IP input is Error")
            return False
          url.append(str(id))
        elif (str(i)=="auto_connect"):
          if (str(id)=="0") or (str(id)=="1"):
            url.append(str(id))
          elif (str(id).upper()=="FALSE") or (str(id).upper()=="TRUE"):
            url.append(str(id).upper())
          else:
            url.append(str("0"))
        else:
          url.append(str(id))
  file=open("/config.py","w",encoding='utf-8')
  for i in range(0,len(memory_var),1):
    file.write("{0}=\"{1}\"\n".format(memory_var[i],url[i]))
  file.close()
  print("Saved settings!")
  with open("/www/save_settings.html",'r') as f:
    send_response(conn,str(f.read()))
def send_response(conn,payload,status_code=200):
  content_length=len(payload)
  conn.sendall("HTTP/1.0 {} OK\r\nContent-Type: text/html\r\n".format(status_code))
  if content_length is not None:
    conn.sendall("Content-Length: {}\r\n".format(content_length))
  conn.sendall("\r\n")
  if content_length>0:
    conn.sendall(payload)
  conn.close()
def not_found(conn,url):
  print("Not found: "+str(url))
  with open("/www/404.html",'r') as f:
    send_response(conn,str(f.read().format(uname()[1].upper(),hotspot.ifconfig()[0],str(port))),status_code=404)
def info_device(conn,request):
  print("View info request")
  request=request.decode('utf-8')
  html="""{0}<pre>
""".format(str(head("Info your request")))
  for i in [v.strip() for v in request.replace('\r\n', ';').split(';') if v.strip()]:
    if str(i)=="":
      continue
    else:
      html+="""{0}
""".format(str(i))
  html+="""</pre>
{0}""".format(str(last(port)))
  send_response(conn,html)
def show_password(conn):
  print("Show password")
  html="""{0}<pre>
""".format(str(head("Show password")))
  file=open("/wifi.txt","r")
  count=0
  for i in file.readlines():
    if str(i)=="":
      continue
    else:
      html+="""{0}
""".format(str(i))
      count+=1
  if count==0:
    html+="""No passwords are saved here
"""
  html+="""</pre>
</body></html>"""
  send_response(conn,html)
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
      print("TIMEOUT {0}s: {1}".format(str(timeout),ssid))
      with open("/www/cannot_connect.html",'r') as f:
        response=str(f.read().format(ssid,str(timeout)))
    else:
      Pin(2,Pin.OUT)
      print("SUCCESS: {0}\nIP: {1}\nSubnet: {2}\nGateway: {3}\nDNS: {4}".format(ssid,wifi.ifconfig()[0],wifi.ifconfig()[1],wifi.ifconfig()[2],wifi.ifconfig()[3]))
      write_file(ssid,password)
      with open("/www/connected.html",'r') as f:
        response=str(f.read().format(ssid,wifi.ifconfig()[0],wifi.ifconfig()[1],wifi.ifconfig()[2],wifi.ifconfig()[3],"/","Home"))
  return response
def auth(conn):
  print("Password required!")
  with open("/www/auth.html",'r') as f:
    send_response(conn,str(f.read()))
def verify_auth(conn,request,url,num):
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
  print("Input Admin password: "+str(password))
  if str(password)==str(config.admin_password):
    try:
      if int(num)==0:
        wifi.active(False)
        wifi.active(True)
        send_response(conn,"""<meta http-equiv='refresh' content='0; URL=/'>""")
      elif int(num)==1:
        show_password(conn)
      elif int(num)==2:
        del request,num,url
        settings(conn)
      elif int(num)==3:
        print("Restart...")
        send_response(conn,"Restarting...")
        reset()
    except NameError:
      response_error(conn,"Authentication ERROR!")
  else:
    print("Password ERROR")
    response_error(conn,"Authentication ERROR!")

