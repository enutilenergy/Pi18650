import time
import RPi.GPIO as GPIO
import os
import sys
import subprocess

PWR_GOOD =  18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWR_GOOD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(PWR_GOOD, GPIO.FALLING)

def shutdown_callback():

	print "Shutdown request detected!! initiating shutdown"
	cmd="sudo shutdown -h now"
	subprocess.Popen(cmd, shell=True, executable='/bin/bash')

#GPIO.add_event_callback(PWR_GOOD, shutdown_callback)

while 1:

	if GPIO.event_detected(PWR_GOOD):
		print "Remote-Reboot Detected....!!!"
		shutdown_callback()
