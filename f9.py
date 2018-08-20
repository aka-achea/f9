#!/usr/bin/python
#coding:utf-8
"""
Python 3
BIOS Setup Automation Tool
Support HP BL460 G9, BL660 G9
"""

import time , os
import pyautogui as auto


sys = 'sys.png'
f9 = 'F9.png'

#sys = 'C:\\bk\\SIR\\BIOS\\sys.png'
#f9 = 'C:\\bk\\SIR\\BIOS\\F9.png'

auto.size()
width, height = auto.size()
#print(width,height)
auto.PAUSE = 1

def capture(img):
    capture = 0
    trytime = 1
    while capture == 0 and trytime < 20:
        button = auto.locateCenterOnScreen(img,grayscale=True)
        time.sleep(10)
        if button:
            print('Find '+img)
            #print(button)
            auto.click(button)
            if img == f9:
                auto.press('f9')
            capture == 1
            break
        else:
            time.sleep(1)
            trytime += 1
            print(str(trytime)+' try to locate again ' +img )
            continue
    else:
        print("Time Out")
#print(srv)
#os.makedirs(srv)
#os.chdir(srv)

def g9_reboot():
    auto.typewrite('\n') #->System config
    time.sleep(1)
    auto.typewrite(['esc']) #->Utilities
    time.sleep(1)
    auto.typewrite(['esc']) #->EXIT
    time.sleep(1)
    auto.typewrite(['\n']) #->reboot
    time.sleep(1)
    auto.typewrite(['\n']) #->reboot

def screenshot(srv,w,step):
    auto.screenshot(srv+"_"+w+"_"+step+".png",region=(0,0, 1000, 900))

def WSOE():
    # auto.click(150,150,button='left')
    time.sleep(1)
    auto.typewrite('\n') #-> system config
    time.sleep(1)
    auto.typewrite('\n') #-> BIOS
    time.sleep(1)
    auto.typewrite('\n') #-> system option
    time.sleep(1)
    auto.typewrite(['down','down','down','down','\n']) #-> virtualization option
    time.sleep(1)
    auto.typewrite(['\n','down','\n']) #disable virtualization
    time.sleep(1)
    auto.typewrite(['down','\n','down','\n']) #disable VT-d
    time.sleep(1)
    auto.typewrite(['down','\n','down','\n']) #disable SR-IOV
    time.sleep(1)
    auto.screenshot(srv+'_virtconfig.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->system option
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['up','up','up','up','up','\n']) #->EMS
    time.sleep(1)
    auto.typewrite(['down','down','\n','up','up','up','up','\n']) # change Rate
    time.sleep(1)
    auto.typewrite(['down','\n','\n','up','\n']) # disable console
    time.sleep(1)
    auto.screenshot(srv+'_EMS.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['down','down','\n']) #->Advance option
    time.sleep(1)
    auto.typewrite(['down','down','down','\n']) #->advanced ROM
    time.sleep(1)
    auto.typewrite(['\n','down','\n']) #disable NMI
    time.sleep(1)
    auto.screenshot(srv+'_NMI.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->Advance option
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['down','down','down','down','down','\n']) #-> Network
    time.sleep(1)
    auto.typewrite(['\n']) #->Boot Opt
    time.sleep(1)
    auto.typewrite(['down','down','down','\n','\n','down','\n']) # Disable Port1
    time.sleep(1)
    auto.screenshot(srv+'_port.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->Network
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['esc']) #->EXIT
    time.sleep(1)
    auto.typewrite('Y') #->EXIT
    time.sleep(1)
    g9_reboot()

def VSOE():
    # auto.click(150,150,button='left')
    time.sleep(1)
    auto.typewrite('\n') #-> system config
    time.sleep(1)
    auto.typewrite('\n') #-> BIOS
    time.sleep(1)
    auto.typewrite('\n') #-> system option
    time.sleep(1)
    auto.typewrite('\n') #-> Serial option
    time.sleep(1)
    auto.typewrite(['\n','down','\n']) #disable Embedded Serial
    time.sleep(1)
    auto.typewrite(['down','\n','down','down','\n']) #disable virtual serial
    time.sleep(1)
    auto.screenshot(srv+'_serial.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->system option
    time.sleep(1)
    auto.typewrite(['down','down','down','down','\n']) #-> virtualization option
    time.sleep(1)
    auto.typewrite(['down','\n','down','\n']) #disable VT-d
    time.sleep(1)
    auto.typewrite(['down','\n','down','\n']) #disable SR-IOV
    time.sleep(1)
    auto.screenshot(srv+'_virtconfig.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->system option
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['down','down','down','down','down','\n']) #-> power management
    time.sleep(1)
    auto.typewrite(['\n','down','down','\n']) #Set Max Perf
    time.sleep(1)
    auto.screenshot(srv+'_powermax.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['up','\n']) #->Advanced Power
    time.sleep(1)
    auto.typewrite(['up','up','\n','down','\n']) #->Advanced Power
    time.sleep(1)
    auto.screenshot(srv+'_powercoll.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->power management
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['down','down','down','down','\n']) #-> Srv Availability
    time.sleep(1)
    auto.typewrite(['\n','down','\n']) #Disable ASR
    time.sleep(1)
    auto.screenshot(srv+'_ASR.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['down','\n']) #->EMS
    time.sleep(1)
    auto.typewrite(['down','down','\n','up','up','up','up','\n']) # change Rate
    time.sleep(1)
    auto.typewrite(['down','\n','\n','up','\n']) # disable console
    time.sleep(1)
    auto.screenshot(srv+'_EMS.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['down','down','down','down','down','down','down','\n']) #->Network
    time.sleep(1)
    auto.typewrite(['\n']) #->Boot Opt
    time.sleep(1)
    auto.typewrite(['down','down','down','\n','\n','down','\n']) #disable port
    time.sleep(1)
    auto.typewrite(['down','\n','\n','down','\n']) #disable port
    time.sleep(1)
    auto.screenshot(srv+'_port.png',region=(0,0, 1000, 900))
    time.sleep(1)
    auto.typewrite(['esc']) #->Network
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['esc']) #->EXIT
    time.sleep(1)
    auto.typewrite('Y') #->EXIT
    time.sleep(1)
    g9_reboot()

def LSOE():
    w = 'LSOE'
    # auto.click(150,150,button='left')
    time.sleep(1)
    auto.typewrite('\n') #-> system config
    time.sleep(1)
    auto.typewrite('\n') #-> BIOS
    time.sleep(1)
    auto.typewrite('\n') #-> system option
    time.sleep(1)
    auto.typewrite(['down','down','\n']) #->Processor Opt
    time.sleep(1)
    auto.typewrite(['\n','down','\n']) # disable Hyperthread
    time.sleep(1)
    step = 'Processor'
    screenshot(srv,w,step)
    time.sleep(1)
    auto.typewrite(['esc']) #->system option
    time.sleep(1)
    auto.typewrite(['down','down','\n']) #-> virtualization option
    time.sleep(1)
    auto.typewrite(['\n','down','\n']) #disable virtualization
    time.sleep(1)
    auto.typewrite(['down','\n','down','\n']) #disable VT-d
    time.sleep(1)
    auto.typewrite(['down','\n','down','\n']) #disable SR-IOV
    time.sleep(1)
    step = 'virtconfig'
    screenshot(srv,w,step)
    time.sleep(1)
    auto.typewrite(['esc']) #->system option
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['up','up','up','up','up','\n']) #->EMS
    time.sleep(1)
    auto.typewrite(['\n','down','down','\n']) # change Port
    time.sleep(1)
    step = 'EMS'
    screenshot(srv,w,step)
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['up','\n']) #->Srv Availability
    time.sleep(1)
    auto.typewrite(['\n','down','\n']) #Disable ASR
    time.sleep(1)
    step = 'ASR'
    screenshot(srv,w,step)
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['up','up','up','up','up','up','up','\n']) #-> Network
    time.sleep(1)
    auto.typewrite(['\n']) #->Boot Opt
    time.sleep(1)
    auto.typewrite(['down','down','down','\n','\n','down','\n']) # Disable Port1
    time.sleep(1)
    step = 'port'
    screenshot(srv,w,step)
    time.sleep(1)
    auto.typewrite(['esc']) #->Network
    time.sleep(1)
    auto.typewrite(['esc']) #->BIOS
    time.sleep(1)
    auto.typewrite(['esc']) #->EXIT
    time.sleep(1)
    auto.typewrite('Y') #->EXIT
    time.sleep(1)
    g9_reboot()

def selectversion():
    try:
        if BIOS == "w":
            print("Configuring BIOS for Windows (WSOE)")
            capture(f9)
            capture(sys)
            WSOE()
            print("BIOS Configuration Complete")
        elif BIOS == "l":
            print("Configuring BIOS for Linux (LSOE)")
            capture(f9)
            capture(sys)
            LSOE()
            print("BIOS Configuration Complete")
        elif BIOS == "v":
            print("Configuring BIOS for VMware (VSOE)")
            capture(f9)
            capture(sys)
            VSOE()
            print("BIOS Configuration Complete")
        else:
            print("Wrong Input")

    except KeyboardInterrupt:
        print("Stop")

if __name__=='__main__':
        wp = os.path.dirname(os.path.realpath(__file__))
        os.chdir(wp)
        print("Input your BIOS version")
        print("w=Windows ; l=Linux ; v=VMware")
        BIOS = input(">>")
        srv = input("Input server name>>  ")
        selectversion()

"""
Change log:
2017.6.19 build basic function for bl460g9 for VSOE v1.0
2017.6.24 add function for WSOE,LSOE v1.1
2017.6.28 add screen shot funtion v1.2
2017.12.28 add F9 press function v1.3
"""
