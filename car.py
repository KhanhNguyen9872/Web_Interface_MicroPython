from carclass import *
from machine import Pin,PWM
## motor 1 is right, motor 2 is left
## ENA -> D6, IN1 -> D7, IN2 -> D8
## ENB -> D5, IN3 -> D3, IN4 -> D0
co=remote(Motor(Pin(16,Pin.OUT),Pin(0,Pin.OUT),PWM(Pin(14),15000)),Motor(Pin(13,Pin.OUT),Pin(15,Pin.OUT),PWM(Pin(12),15000)),40)
up,down,left,right=False,False,False,False
car_remote_dict={
	## touch ##
	"u":"""up=True
if (left==True and right==True) or down==True:
  co.s()
elif left==True:
	co.l()
elif right==True:
	co.r()
else:
	co.u()
""",
	"d":"""down=True
if (left==True and right==True) or up==True:
  co.s()
elif left==True:
	co.l()
elif right==True:
	co.r()
else:
	co.d()
""",
	"l":"""left=True
if (up==True and down==True) or right==True:
  co.s()
else:
  co.l()
""",
	"r":"""right=True
if (up==True and down==True) or left==True:
  co.s()
else:
  co.r()
""",
	## release ##
	"eu":"""up=False
if left==True and right==True:
  co.s()
elif down==True:
  if left==True:
    co.l()
  elif right==True:
    co.r()
  else:
    co.d()
else:
  co.s()
""",
	"ed":"""down=False
if left==True and right==True:
  co.s()
elif up==True:
  if left==True:
    co.l()
  elif right==True:
    co.r()
  else:
    co.u()
else:
  co.s()
""",
	"el":"""left=False
if up==True and down==True:
  co.s()
elif up==True:
  if left==True:
    co.l()
  elif right==True:
    co.r()
  else:
    co.u()
elif down==True:
  if left==True:
    co.l()
  elif right==True:
    co.r()
  else:
    co.d()
elif right==True:
  co.r()
else:
  co.s()
""",
	"er":"""right=False
if up==True and down==True:
  co.s()
elif up==True:
  if left==True:
    co.l()
  elif right==True:
    co.r()
  else:
    co.u()
elif down==True:
  if left==True:
    co.l()
  elif right==True:
    co.r()
  else:
    co.d()
elif left==True:
  co.l()
else:
  co.s()
"""
}
