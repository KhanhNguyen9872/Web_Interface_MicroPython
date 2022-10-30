print("Booting...")
import uos,machine,network,gc,config
from machine import Pin
machine.freq(160000000)
hotspot=network.WLAN(network.AP_IF)
try:
  print("Starting hotspot ["+config.ap_name+"]"+" ["+config.ap_password+"]")
  hotspot.config(essid=str(config.ap_name),password=str(config.ap_password),channel=int(config.ap_channel),hidden=0)
  hotspot.ifconfig((str(config.ap_web_ip),str(config.ap_subnet),str(config.ap_gateway),str(config.ap_dns)))
except:
  pass
hotspot.active(True)
gc.collect()