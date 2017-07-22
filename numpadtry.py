import RPi.GPIO as GPIO
import time
import lcdtry
import IRAtwitter

num = []

MATRIX = [ [1,2,3,'A'],
           [4,5,6,'B'],
           [7,8,9,'C'],
           ['*',0,'#','D'],]

ROW = [21,20,16,12]
COL = [25,24,23,18]

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line


def numpad_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    lcdtry.lcd_init()
    for j in range(4):
        GPIO.setup(COL[j],GPIO.OUT)
        GPIO.output(COL[j],1)

    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

def numinput():
    try:
        while(True):
            for j in range(4):
                GPIO.output(COL[j],0)

                for i in range(4):
                    if GPIO.input(ROW[i]) == 0:
                        if(MATRIX[i][j]=='D' and len(num)==0):
                            pass
                        elif(MATRIX[i][j]=='D' and len(num)!=0):
                            num.pop()
                            string = ''.join(str(e) for e in num)
                            lcdtry.lcd_string(string,LCD_LINE_1)
                        elif(MATRIX[i][j]=='A' or MATRIX[i][j]=='B' or MATRIX[i][j]=='*' or MATRIX[i][j]=='#'):
                            pass
                        elif (MATRIX[i][j]=='C' ):
                            if(string[0]!='0' and len(string)==10):
                                #don't forget to validate string
                                apiobject = IRAtwitter.authenticate()
                                IRAtwitter.sendMessage(apiobject,string)
                                lcdtry.lcd_string("Requested",LCD_LINE_2)
                            else:
                                lcdtry.lcd_string("Invalid Number",LCD_LINE_2)
                            # else part write
                        else:
                            num.append(MATRIX[i][j])
                            string = ''.join(str(e) for e in num)
                            lcdtry.lcd_string(string,LCD_LINE_1)
                            #print(MATRIX[i][j])
                        while(GPIO.input(ROW[i]) == 0):
                            pass
                GPIO.output(COL[j],1)
                time.sleep(0.2)

    except KeyboardInterrupt:
        GPIO.cleanup()
