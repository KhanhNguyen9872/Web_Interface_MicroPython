from ure import search
import config,network
from os import uname
hotspot=network.WLAN(network.AP_IF)
port=str(config.ap_web_port)
def send_response(conn,payload,status_code=200):
  content_length=len(payload)
  conn.sendall("HTTP/1.0 {} OK\r\nContent-Type: text/html\r\n".format(status_code))
  if content_length is not None:
    conn.sendall("Content-Length: {}\r\n".format(content_length))
  conn.sendall("\r\n")
  if content_length>0:
    conn.sendall(payload)
  conn.close()
def info_device(conn,request):
  print("View info request")
  request=request.decode('utf-8')
  html="""{}<pre>
""".format(str(head("Info your request")))
  for i in [v.strip() for v in request.replace('\r\n', ';').split(';') if v.strip()]:
    if str(i)=="":
      continue
    else:
      html+="""{}
""".format(str(i))
  html+="""</pre>
{}""".format(str(last(port)))
  send_response(conn,html)
def auth(conn):
  print("Password required!")
  with open("/www/auth.html",'r') as f:
    send_response(conn,str(f.read()))
def show_password(conn):
  print("Show password")
  html="""{}<pre>
""".format(str(head("Show password")))
  file=open("/wifi.txt","r")
  count=0
  for i in file.readlines():
    if str(i)=="":
      continue
    else:
      html+="""{}
""".format(str(i))
      count+=1
  if count==0:
    html+="""No passwords are saved here
"""
  html+="""</pre>
</body></html>"""
  send_response(conn,html)
def not_found(conn,url):
  print("Not found: "+str(url))
  with open("/www/404.html",'r') as f:
    send_response(conn,str(f.read().format(uname()[1].upper(),hotspot.ifconfig()[0],str(port))),status_code=404)
def write_file(name,password):
  with open("/wifi.txt",'r') as f:
    temp=str(f.read()).split("\n")
  temp2=str(str(name)+" - "+str(password))
  if temp2 in temp:
    pass
  else:
    file=open("/wifi.txt","a",encoding='utf-8')
    file.write(str(name)+" - "+str(password)+"\n")
    file.close()
def search_url(request):
    try:
      url=search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).decode("utf-8").rstrip("/")
    except Exception:
      url=search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
    return url
def configure(conn,request,url,wifi_name,wifi_signal):
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
  if (str(password)=="") or (len(password)>7):
    pass
  else:
    response_error(conn,"Password must be equal to or greater than 8. If your wifi is open, you must not enter the password dialog")
  try:
    ssid=str(wifi_name[id])
  except:
    response_error(conn,"The SSID you selected was not found from there")
  del id
  print("Selected SSID: "+ssid)
  print("Input Password: "+password)
  with open("/www/selected_wifi.html",'r') as f:
    response=str(f.read().format(str(ssid)))
  return ssid,password,response
def response_error(conn,error):
  print(str(error))
  with open("/www/error.html",'r') as f:
    send_response(conn,str(f.read().format(str(error))))
def head(name):
  with open("/www/head.html",'r') as f:
    return str(f.read().format(str(name)))
def last(port):
  with open("/www/last.html",'r') as f:
    return str(f.read().format(str(uname()[1].upper()),str(hotspot.ifconfig()[0]),str(port)))
def wifi_scanning(conn,wifi):
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
        response+=str(f.read().format(wifi_name[i],wifi_signal[i],i))
  with open("/www/button_find_wifi.html",'r') as f:
    response+=str(f.read())
  del wifi_hidden
  return wifi_name,wifi_signal,response
