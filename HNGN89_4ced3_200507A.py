def W_cool():
	Troom=20
	Hcond=0.2
	W=Hcond*(dT+Ttarget-Troom)
	return W

###+++++++++++++##########################

from matplotlib import pyplot as plt
from matplotlib import animation as animation
import numpy as np
import serial
import time
import sys
import re

# strPort = '/dev/tty.usbserial-A7006Yqh'
print ("pls input port name = M5Stck, ARDUINO, file_name.csv")
print ("use LS command to find port name") 

# plot parameters
#analogData = AnalogData(100)
#analogPlot = AnalogPlot(analogData)

#tc1 = [0] * 100
#tc2 = [0] * 100
#cnv = [0]*100
t=np.linspace(0.0,10.0,100)
# open serial port
strPort1 = sys.argv[1];
strPort2 = sys.argv[2];
file1=sys.argv[3];
ser1 = serial.Serial(strPort1, 115200) # M5Stack Serial Speed
ser2 = serial.Serial(strPort2, 115200) # Arduino Serial Speed
f=open(file1,"w+")

while True:
  data=[]
  for i in range(0,100):
    data=[]
    regex = re.compile('\d+')
    line = ser1.readline()
    try:
      match = regex.findall(str(line))
      data.append(float(match[1])*60.0+float(match[2])+float(match[3])*0.1)
      data.append(float(match[4]+"."+match[5]))
      data.append(float(match[6]+"."+match[7]))
      data.append(float(match[8]+"."+match[9]))
      data.append(float(match[10]+"."+match[11]))
      data.append(float(match[12]+"."+match[13]))
      data.append(float(match[14]+"."+match[15]))
      data.append(float(match[16]+"."+match[17]))
      data.append(float(match[18]+"."+match[19]))
      data.append(float(match[20]+"."+match[21]))
      data.append(float(match[22]+"."+match[23]))

    except:
      print(line); #print(word)
      exit()

  ims = []
  dt = 0.05
  Kp = 0.0			
  Kd = 0.0
  Ki = 0.0	
  for j in range(1):
    dT_list = []
    t_list = []
    if Kp < 0.0:		#比例ゲイン
      Kp += 0.01
    elif Ki < 0.001:	#積分ゲイン
      Ki += 0.001
    elif Kd < 0.5:		#微分ゲイン
      Kd += 0.01
					
  Q=2000 #initial condition
  Qmax=300 #NiCr wire power at 100V
  H=3.36
  T=Q/H-273
  print("T=Treal=",'f{T:/4f}')
  W_heat=280 #initial condition
  Ttarget=T_target_degC=400 
  dT=T-Ttarget
		
  for i in range(int(50/dt)):
    t = i*dt
    dT=T-Ttarget
	
    print("W_cool=",f'{W_cool():.4f}')
    print("W_heat=",f'{W_heat:.4f}')
    Kp=0.05; Ki=0.0; Kd=0.2
    W_heat += -Kp*(dT) -Kd*(W_heat/H) -Ki*(dT*dt)  
    #{200912}
    #Kd term is in-correct (slow),   
    # Ki is important   (integral is necessary) 
    print("W_heat=",f'{W_heat:.4f}')
    Q +=W_heat-W_cool()
    #W_heat=Input_of_Control_Loop=heater_power_input
    print("dT=",f'{dT:.4f}')
#  ser =serial.Serial("/dev/cu.usbmodem1414401", 9600)
  time.sleep(2)
  val=val_2_arduino=Q*255//Qmax #integer
#  print(val)
  a = int(val).to_bytes(1, byteorder="little") # 0-255 ==> one byte HEX ==> ARDUINO
  ser2.write(a) #ARDUINO Port
  print(a)
#  ser.close()
  dT_list.append(dT)
  t_list.append(t)
		

