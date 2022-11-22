from carclass import *
from machine import Pin,PWM
## motor 1 is right, motor 2 is left
## ENA -> D6, IN1 -> D7, IN2 -> D8
## ENB -> D5, IN3 -> D3, IN4 -> D0
c=remote(Motor(Pin(16,Pin.OUT),Pin(0,Pin.OUT),PWM(Pin(14),15000)),Motor(Pin(13,Pin.OUT),Pin(15,Pin.OUT),PWM(Pin(12),15000)),40)
u,d,l,r=False,False,False,False
car_remote_dict={
  ## touch ##
  "u":"""u=True
if (l==True and r==True) or d==True:
  c.s()
elif l==True:
  c.l()
elif r==True:
  c.r()
else:
  c.u()
""",
  "d":"""d=True
if (l==True and r==True) or u==True:
  c.s()
elif l==True:
  c.r()
elif r==True:
  c.l()
else:
  c.d()
""",
  "l":"""l=True
if (u==True and d==True) or r==True:
  c.s()
elif d==True:
  c.r()
else:
  c.l()
""",
  "r":"""r=True
if (u==True and d==True) or l==True:
  c.s()
elif d==True:
  c.l()
else:
  c.r()
""",
  ## release ##
  "eu":"""c.s()
u=False
if l==True and r==True:
  c.s()
elif d==True:
  if l==True:
    c.r()
  elif r==True:
    c.l()
  else:
    c.d()
elif l==True:
  c.l()
elif r==True:
  c.r()
""",
  "ed":"""c.s()
d=False
if l==True and r==True:
  c.s()
elif u==True:
  if l==True:
    c.l()
  elif r==True:
    c.r()
  else:
    c.u()
elif l==True:
  c.l()
elif r==True:
  c.r()
""",
  "el":"""c.s()
l=False
if u==True and d==True:
  c.s()
elif u==True:
  if l==True:
    c.l()
  elif r==True:
    c.r()
  else:
    c.u()
elif d==True:
  if l==True:
    c.r()
  elif r==True:
    c.l()
  else:
    c.d()
elif r==True:
  c.r()
""",
  "er":"""c.s()
r=False
if u==True and d==True:
  c.s()
elif u==True:
  if l==True:
    c.l()
  elif r==True:
    c.r()
  else:
    c.u()
elif d==True:
  if l==True:
    c.r()
  elif r==True:
    c.l()
  else:
    c.d()
elif l==True:
  c.l()
"""
}
