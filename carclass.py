class Motor:      
  def __init__(self,p1,p2,e):
    self.p1=p1
    self.p2=p2
    self.e=e
    self.mi=150
    self.ma=1023
  def up(self,s):
    self.s=s
    self.e.duty(self.du(self.s))
    self.p1.value(1)
    self.p2.value(0)
  def do(self,s):
    self.s=s
    self.e.duty(self.du(self.s))
    self.p1.value(0)
    self.p2.value(1)
  def st(self):
    self.e.duty(0)
    self.p1.value(1)
    self.p2.value(1)
  def du(self,s):
   if self.s<=0 or self.s>100:
    dut=0
   else:
    dut=int(self.mi+(self.ma-self.mi)*((self.s-1)/(100-1)))
    return dut
class remote:
  def __init__(self,m1,m2,sp):
    self.m1=m1
    self.m2=m2
    self.sp=sp
  def u(self):
    self.m1.up(self.sp)
    self.m2.up(self.sp)
  def d(self):
    self.m1.do(self.sp)
    self.m2.do(self.sp)
  def l(self):
    self.m1.up(self.sp+10)
    self.m2.do(self.sp+10)
  def r(self):
    self.m1.do(self.sp+10)
    self.m2.up(self.sp+10)
  def s(self):
    self.m1.st()
    self.m2.st()