from machine import Pin
up,down,left,right=False,False,False,False
## Motor (Pin)
m1,m2=False,False
m3,m4=False,False
## dict main
car_remote_dict={
	## touch ##
	"up":"""up=True
if down==True:
  print("up+down, stop car")
elif left==True:
	print("up+left")
elif right==True:
	print("up+right")
else:
	print("up")
""",
	"down":"""down=True
if up==True:
  print("up+down, stop car")
elif left==True:
	print("down+left")
elif right==True:
	print("down+right")
else:
	print("down")
""",
	"left":"""left=True
if right==True:
  print("right+left, stop car")
elif up==True:
  print("up+left")
elif down==True:
  print("down+left")
else:
  print("left")
""",
	"right":"""right=True
if left==True:
  print("right+left, stop car")
elif up==True:
  print("up+right")
elif down==True:
  print("down+right")
else:
  print("right")
""",
	## release ##
	"end_up":"""up=False
print("end_up")
if down==True:
  if left==True:
    print("down+left")
  elif right==True:
    print("down+right")
  else:
    print("down")
""",
	"end_down":"""down=False
print("end_down")
if up==True:
  if left==True:
    print("up+left")
  elif right==True:
    print("up+right")
  else:
    print("up")
""",
	"end_left":"""left=False
print("end_left")
if up==True:
  if left==True:
    print("up+left")
  elif right==True:
    print("up+right")
  else:
    print("up")
elif down==True:
  if left==True:
    print("down+left")
  elif right==True:
    print("down+right")
  else:
    print("down")
elif right==True:
  print("right")
""",
	"end_right":"""right=False
print("end_right")
if up==True:
  if left==True:
    print("up+left")
  elif right==True:
    print("up+right")
  else:
    print("up")
elif down==True:
  if left==True:
    print("down+left")
  elif right==True:
    print("down+right")
  else:
    print("down")
elif left==True:
  print("left")
"""
}
