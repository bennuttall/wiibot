#!/usr/bin/python3

from gpiozero import CamJamKitRobot, Buzzer, DistanceSensor
import cwiid
from subprocess import check_call

def shutdown():
    buzzer.beep(0.1, 0.1, n=20, background=False)
    buttons = wii.state['buttons']
    if buttons & cwiid.BTN_B:
        check_call(['sudo', 'poweroff'])

def vibrate():
    print("vibrate")
    wii.rumble = 1

def stop_vibrate():
    print("stop vibrate")
    wii.rumble = 0

robot = CamJamKitRobot()
buzzer = Buzzer(23)
ultrasonic = DistanceSensor(echo=17, trigger=18, threshold_distance=0.1)

buzzer.beep(0.1, 0.5)
wii = None
while not wii:
    try:
        wii = cwiid.Wiimote()
    except:
        print("Hold down Wiimote buttons")

buzzer.off()
wii.rpt_mode = cwiid.RPT_BTN

ultrasonic.when_in_range = vibrate
ultrasonic.when_out_of_range = stop_vibrate

while True:
    print(ultrasonic.distance)
    buttons = wii.state['buttons']
    if buttons & cwiid.BTN_UP:
        robot.forward()
    elif buttons & cwiid.BTN_DOWN:
        robot.backward()
    elif buttons & cwiid.BTN_LEFT:
        robot.left()
    elif buttons & cwiid.BTN_RIGHT:
        robot.right()
    elif buttons & cwiid.BTN_B:
        shutdown()
    else:
        robot.stop()
