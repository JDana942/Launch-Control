#!/usr/bin/python

# Code Rev001
from RPi import GPIO # For use in IDE
#import RPi.GPIO as GPIO # For use in RPi
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
  time.sleep(1)
  while (True):
    usr_t = str(input("Please select one of the following operations.\n  1. Logout\n  2. System Check\n  3. Initate Launch\n  4. Static motor test\n"))
    if (usr_t == "1"):
      _exit()
    elif (usr_t == "2"):
      preLaunch()
    elif (usr_t == "3"):
      usr_L= str(input("Enter Ignition Key Buster for ignition\n"))
      if (usr_L == "Buster"):
        _launch()
      else:
        print("Incorrect Launch Key")
    elif (usr_t == "4"):
      usr_L= str(input("Enter Ignition Key Buster for ignition\n"))
      if (usr_L == "Buster"):
        _cal()
      else:
        print("Incorrect Launch Key")
    else:
      print("Good job bud we are so proud of you!\n But try again...")

def preLaunch():
  print("Pre-launch system is under development")

def _launch():
  preLaunch()
  print("Launch sequence initated.\nLaunching in...")
  Lcount = 10
  for i in range(10):
    print(Lcount)
    time.sleep(1)
    Lcount -= 1
  print("Ignition")
  GPIO.setup(IGN, GPIO.OUT)
  GPIO.output(IGN, 1)
  time.sleep(3)
  GPIO.output(IGN, 0)
  #_postIgnition()
  terminal()
  # Include additional post ingnition check and options for re-ignition

def _postIgnition():
  print("Post Ignition under development")

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
  zero_1 = []
  zero_2 = []
  for i in range (3):
    zero_1.append(_read())
    zero_f1 = mean(zero_1)
  for i in range (3):
    zero_2.append(_read()-zero_f1)
  zero_f2 = mean(zero_2)
  zero_factor = zero_f1 + zero_f2
  signal.signal(signal.SIGINT, s)
  _staticTest(zero_factor)
  # scallingFactor = 
  # Add Scalling Factor

def _staticTest(zero_factor):
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
  ignOn = time.time()
  print("TMP Ready")
  while(True):
    measure = round((_read()-zero_factor)/1000, 2)
    ignOff = time.time()
    ignTimer = ignOff-ignOn
    if (ignTimer > 3 and ignTimer < 3.01):
      GPIO.output(IGN,0)
    if (ignTimer > 10):
      while(True):
        usr_reign = str(input("Ignition Failed \nReattempt? Y or N\n"))
        if (usr_reign == "Y"):
          print("Re-attempting Ignition. DO NOT APPROCH MOTOR")
          _staticTest(zero_factor)
        elif (usr_reign == "N"):
          print("Ignition Aborted")
          terminal()
        else:
          print("Incorrect Response")
    if(measure > 5.0):
      measure = round((_read()-zero_factor)/1000, 2)
      GPIO.output(IGN,0)
      if(measure > 5.0):
        print("Recording")
        starttime = time.time()
        while(True):
          measure = round((_read()-zero_factor)/1000, 2)
          print(measure)
          b += 1
          Force.append(measure)
          Time.append(b)
          if(measure < 5.0 and measure > -10.0):  # condition to break loop
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
  try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    print("Accessing the Launch Control System...")
    time.sleep(2)
    access()
  finally:
    _exit()

if __name__ == "__main__":
  main()
