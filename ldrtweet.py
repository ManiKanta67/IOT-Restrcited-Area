from gpiozero import LightSensor, Buzzer
from time import sleep
import datetime
import threading
import numpadtry
import IRAtwitter
import sys
import lcdtry

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

numpadtry.numpad_init()
apiobject = IRAtwitter.authenticate()
lcdtry.lcd_init()

ldr = LightSensor(4)
buzzer = Buzzer(17)
status = False

lok = threading.Lock()

def alarm():
    global ldr
    global buzzer
    global status
    global apiobject
    global LCD_LINE_1
    global LCD_LINE_2
    #timelist = []
    while(True):
        sleep(0.0001)
        #time1,status = IRAtwitter.findCommand(apiobject)
        status = IRAtwitter.findCommand(apiobject)
        if ldr.value < 0.5 and status == False:
        #if ldr.value < 0.05:
            buzzer.on()
            #don't forget to tweet
            apiobject = IRAtwitter.authenticate()
            IRAtwitter.newTweet(apiobject)
        elif ldr.value < 0.5 and status == True:
            #if time1 not in timelist
            #timelist.append(time1)
            #print(timelist)
            buzzer.off()
            lcdtry.lcd_string("Sleepmode on",LCD_LINE_1)
            lcdtry.lcd_string("For 10 Secnds",LCD_LINE_2)
            sleep(10)
        else:
            buzzer.off()

thread_alarm = threading.Thread(target=alarm)
thread_numpad = threading.Thread(target=numpadtry.numinput)

thread_alarm.start()
thread_numpad.start()
