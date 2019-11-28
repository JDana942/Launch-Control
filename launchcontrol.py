#!/usr/bin/python

from RPi import GPIO
import os
import sys
import time
import gpiozero as gz
from statistics import mean
import signal

DT = 20
CLK = 21
IGN = 4

def access():
  atp = 3
  while(atp > 0):
    if(atp == 1):
      print("Last attempt before system lockout")
    else:
      pass
    usr = str(input("Please enter your Access Code\n"))
    if (usr == "104043"):
      print("Welcome John")
      terminal()
    elif(usr == "exit"):
      _exit()
    else:
      atp -= 1
      print("Incorrect Access Code.\n   ",atp,"attempts remaining.")
  print("Access denied system LOCKED")
  lockout()

def terminal():
  print("Accessing Control Terminal...")
  time.sleep(2)
  #bool = True
  while (True):
    usr_t = str(input("Please select one of the following operations.\n  1. Logout\n  2. System Check\n  3. Initate Launch\n  4. Static motor test\n"))
    if (usr_t == "1"):
      _exit()
    elif (usr_t == "2"):
      preLaunch()
    elif (usr_t == "3"):
      print("Launch confirmed.\nInitating pre-launch inspection.")
      launch()
    elif (usr_t == "4"):
      _cal()
    else:
      print("Good job bud we are so proud of you!\n But try again...")

def preLaunch():
  print("Pre-launch system is under development")

def launch():
  preLaunch()
  usr_L= str(input("Enter Launch Code for ignition\n"))
  if (usr_L == "Buster"):
    print("Launch sequence initated.\nLaunching in...\n")
    Lcount = 10
    for i in range(10):
      print(Lcount)
      time.sleep(1)
      Lcount -= 1
    print("Ignition")
    GPIO.output(4, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(4, GPIO.LOW)
    #postIgnition()
    terminal()
  else:
    print("Incorrect Launch Code")
  # Include additional post ingnition check and options for re-ignition

def lockout():
  time.sleep(20)
  os._exit(1)

def _read():
  i=0
  Count=0
  GPIO.setup(CLK, GPIO.OUT)
  GPIO.setup(DT, GPIO.IN)
  GPIO.output(CLK,0)
  s = signal.signal(signal.SIGINT, signal.SIG_IGN)
  while GPIO.input(DT) == 1:
      i=0
  for i in range(24):
        GPIO.output(CLK,1)
        Count=Count<<1
        GPIO.output(CLK,0)
        if GPIO.input(DT) == 0:
            Count=Count+1
  GPIO.output(CLK,1)
  Count=Count^0x800000
  GPIO.output(CLK,0)
  signal.signal(signal.SIGINT, s)
  return Count

def _cal():
  s = signal.signal(signal.SIGINT, signal.SIG_IGN)
  CAL = []
  CAL_2 = []
  for i in range (3):
    CAL.append(_read())
    cal_f1 = mean(CAL)
  for i in range (3):
    CAL_2.append(_read()-cal_f1)
  cal_f2 = mean(CAL_2)
  cal_factor = cal_f1 + cal_f2
  signal.signal(signal.SIGINT, s)
  _staticTest(cal_factor)

def _staticTest(cal_factor):
  #s = signal.signal(signal.SIGINT, signal.SIG_IGN)
  Force = ["Force", 0]
  Time = ["Time", 0]
  b = 0
  print("Ignition in...")
  cDown = 5
  for i in range(cDown):
    print(cDown)
    time.sleep(1)
    cDown -= 1
  print("Ignition")
  GPIO.setup(IGN, GPIO.OUT)
  GPIO.output(IGN,1)
  time.sleep(2)
  GPIO.output(IGN,0)
  print("Ready")
  while(True):
    measure = round((_read()-cal_factor)/1000, 2)
    if(measure > 5.0):
      measure = round((_read()-cal_factor)/1000, 2)
      if(measure > 5.0):
        print("Recording")
        starttime = time.time()
        while(True):
          measure = round((_read()-cal_factor)/1000, 2)
          print(measure)
          b += 1
          Force.append(measure)
          Time.append(b)
          if(measure < 5.0 and measure > -10.0):  # condition to break loop
              #signal.signal(signal.SIGINT, s)
              endtime = time.time()
              filetime = time.strftime("%H:%M:%S")
              totaltime = str(endtime - starttime)
              Force = str(Force).strip('[]')
              Time = str(Time).strip('[]')
              result = open("/home/pi/Documents/LoadCell_Data/LoadCell_Results.csv","a")
              result.write(Force + "\n" + Time + "\n" + totaltime + "\n" + filetime +"\n")
              result.close()
              return
          else:
           pass
      else:
        pass
    else:
      pass

def _exit():
  print("System exiting")
  time.sleep(2)
  GPIO.cleanup()
  os._exit(1)

def main():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(17, GPIO.OUT)
  GPIO.output(17, GPIO.LOW)
  print("Accessing the Launch Control System...")
  time.sleep(3)
  access()

if __name__ == "__main__":
  main()
