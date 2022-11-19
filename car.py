from machine import Pin,PWM
class Motor:      
  def __init__(self,pin1,pin2,enable_pin):
    self.pin1=pin1
    self.pin2=pin2
    self.enable_pin=enable_pin
    self.min_duty=150
    self.max_duty=1023
  def forward(self,speed):
    self.speed=speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(1)
    self.pin2.value(0)
  def backwards(self, speed):
    self.speed=speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(0)
    self.pin2.value(1)
  def stop(self):
    self.enable_pin.duty(0)
    self.pin1.value(1)
    self.pin2.value(1)
  def duty_cycle(self,speed):
   if self.speed<=0 or self.speed>100:
    duty_cycle=0
   else:
    duty_cycle=int(self.min_duty+(self.max_duty-self.min_duty)*((self.speed-1)/(100-1)))
    return duty_cycle
## motor 1 is right, motor 2 is left
## ENA -> D6, IN1 -> D7, IN2 -> D8
## ENB -> D5, IN3 -> D3, IN4 -> D0
motor1=Motor(Pin(16,Pin.OUT),Pin(0,Pin.OUT),PWM(Pin(14),15000))
motor2=Motor(Pin(13,Pin.OUT),Pin(15,Pin.OUT),PWM(Pin(12),15000))
speed_mt=40
up,down,left,right=False,False,False,False
car_remote_dict={
  ## touch ##
  "up":"""motor1.forward(speed_mt)
motor2.forward(speed_mt)
""",
  "down":"""motor1.backwards(speed_mt)
motor2.backwards(speed_mt)
""",
  "left":"""motor1.forward(speed_mt+10)
motor2.backwards(speed_mt+10)
""",
  "right":"""motor1.backwards(speed_mt+10)
motor2.forward(speed_mt+10)
""",
  ## release ##
  "end":"""motor1.stop()
motor2.stop()
"""
}