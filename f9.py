#!/usr/bin/python3
#coding:utf-8
"""
BIOS Setup Automation Tool
Support HP BL460 G9, BL660 G9
"""

import time , os
import pyautogui as auto

g10sys = 'g10sys'
g9sys = 'sys'
f9 = 'F9-old'
flom = 'FLOM'

os_dict = {
    'w':'Windows (WSOE)',
    'l':'Linux (LSOE)',
    'v':'VMware (VSOE)',
    's':'Suse (SSOE)'
}
#sys = 'C:\\bk\\SIR\\BIOS\\sys.png'
# f9pic = r'c:\D\GitHub\f9\F9-old.png'
 
auto.size()
width, height = auto.size()
#print(width,height)
auto.PAUSE = 1

def capture(wp,img,trys=20):    
    pic = os.path.join(wp,img+'.png')
    # print(pic)
    trytime = 1
    while trytime < trys:
        try:
            button = auto.locateCenterOnScreen(pic,grayscale=True)
            time.sleep(15)
            print('Find '+img)
            #print(button)
            auto.click(button)
            break            
        except TypeError:
            time.sleep(15)
            trytime += 1
            print(f'try to locate {img} {str(trytime)}')
            continue
    else:
        print("Max tries reach")
        return False
    return True

#print(srv)
#os.makedirs(srv)
#os.chdir(srv)


def screenshot(srv,w,step):
    auto.screenshot(srv+"_"+w+"_"+step+".png",region=(0,0, 1000, 900))


class iLO4():
    def WSOE(self,srv):
        w = 'WSOE'
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
        step = 'virtconfig'
        screenshot(srv,w,step) 
        # auto.screenshot(srv+'_virtconfig.png',region=(0,0, 1000, 900))
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
        step = 'EMS'
        screenshot(srv,w,step) 
        # auto.screenshot(srv+'_EMS.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(1)
        auto.typewrite(['down','down','\n']) #->Advance option
        time.sleep(1)
        auto.typewrite(['down','down','down','\n']) #->advanced ROM
        time.sleep(1)
        auto.typewrite(['\n','down','\n']) #disable NMI
        time.sleep(1)
        step = 'NMI'
        screenshot(srv,w,step) 
        # auto.screenshot(srv+'_NMI.png',region=(0,0, 1000, 900))
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
        step = 'port'
        screenshot(srv,w,step) 
        # auto.screenshot(srv+'_port.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['esc']) #->Network
        time.sleep(1)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(1)
        auto.typewrite(['esc']) #->EXIT
        time.sleep(1)
        auto.typewrite('Y') #->EXIT
        time.sleep(1)
        self.reboot()

    def VSOE(self,srv):
        w = 'VSOE'
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
        step = 'Serial'
        screenshot(srv,w,step)
        # auto.screenshot(srv+'_serial.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['esc']) #->system option
        time.sleep(1)
        auto.typewrite(['down','down','down','down','\n']) #-> virtualization option
        time.sleep(1)
        auto.typewrite(['down','\n','down','\n']) #disable VT-d
        time.sleep(1)
        auto.typewrite(['down','\n','down','\n']) #disable SR-IOV
        time.sleep(1)
        step = 'virtconfig'
        screenshot(srv,w,step)
        # auto.screenshot(srv+'_virtconfig.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['esc']) #->system option
        time.sleep(1)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(1)
        auto.typewrite(['down','down','down','down','down','\n']) #-> power management
        time.sleep(1)
        auto.typewrite(['\n','down','down','\n']) #Set Max Perf
        time.sleep(1)
        step = 'powermax'
        screenshot(srv,w,step)
        # auto.screenshot(srv+'_powermax.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['up','\n']) #->Advanced Power
        time.sleep(1)
        auto.typewrite(['up','up','\n','down','\n']) #->Advanced Power
        time.sleep(1)
        step = 'powercoll'
        screenshot(srv,w,step)        
        # auto.screenshot(srv+'_powercoll.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['esc']) #->power management
        time.sleep(1)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(1)
        auto.typewrite(['down','down','down','down','\n']) #-> Srv Availability
        time.sleep(1)
        auto.typewrite(['\n','down','\n']) #Disable ASR
        time.sleep(1)
        step = 'ASR'
        screenshot(srv,w,step) 
        # auto.screenshot(srv+'_ASR.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(1)
        auto.typewrite(['down','\n']) #->EMS
        time.sleep(1)
        auto.typewrite(['down','down','\n','up','up','up','up','\n']) # change Rate
        time.sleep(1)
        auto.typewrite(['down','\n','\n','up','\n']) # disable console
        time.sleep(1)
        step = 'EMS'
        screenshot(srv,w,step) 
        # auto.screenshot(srv+'_EMS.png',region=(0,0, 1000, 900))
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
        step = 'port'
        screenshot(srv,w,step) 
        # auto.screenshot(srv+'_port.png',region=(0,0, 1000, 900))
        time.sleep(1)
        auto.typewrite(['esc']) #->Network
        time.sleep(1)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(1)
        auto.typewrite(['esc']) #->EXIT
        time.sleep(1)
        auto.typewrite('Y') #->EXIT
        time.sleep(1)
        self.reboot()

    def LSOE(self,srv):
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
        self.reboot()

    def reboot(self):
        auto.typewrite('\n') #->System config
        time.sleep(1)
        auto.typewrite(['esc']) #->Utilities
        time.sleep(1)
        auto.typewrite(['esc']) #->EXIT
        time.sleep(1)
        auto.typewrite(['\n']) #->reboot
        time.sleep(1)
        auto.typewrite(['\n']) #->reboot


class iLO5():
    def __init__(self,srv,waitsec=3,model='blade',FLOM='no'):
        self.interval = waitsec
        self.model = model
        self.FLOM = FLOM
        self.srv = srv
        print(f'{self.srv} server model is {self.model} has {self.FLOM} FlexLOM installed')

    def go_bios(self):
        # time.sleep(self.interval)
        # auto.typewrite('\n') #-> system config no need, click when find sysconfig
        time.sleep(20)  # need some time to load device
        auto.typewrite('\n') #-> BIOS    
        
    def WSOE(self,srv):
        self.go_bios()
        w = 'WSOE'
        time.sleep(15)
        auto.typewrite(['\n','up'])  #-> change workload for general power efficient
        time.sleep(3)
        auto.typewrite(['\n','\n'])  #-> change workload for general power efficient
        step = 'workload'
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> system option
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> serial port
        time.sleep(self.interval)
        auto.typewrite(['\n'])  #-> EMS
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','down','\n'])  #-> serial port
        step = 'EMS'
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #-> serial port


        if self.model == 'rack mounted':
            time.sleep(self.interval)
            auto.typewrite(['down','\n','up','\n'])  #-> for DL serial port
            step = 'DL serial port'
            screenshot(self.srv,w,step) 
            time.sleep(self.interval)

        auto.typewrite(['esc']) #->system option
        time.sleep(self.interval)
        auto.typewrite(['up']) #->back to boot time postion
        time.sleep(self.interval)                    
        auto.typewrite(['down','down','\n'])  #-> USB Option
        time.sleep(self.interval)
        auto.typewrite(['down','down','down','\n','down','\n'])  #-> Disable SD card
        step = 'sdcard'
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->system option
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> Server availability
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','\n','down','\n'])  #-> disable WoL
        step = 'WoL'
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->system option
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','down','down','\n'])  #-> Virtualization Option
        time.sleep(self.interval)
        auto.typewrite(['\n','down','\n'])  #-> disable VT
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','\n'])  #-> disable VTd
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','\n'])  #-> disable SRIOV
        step = 'virt'
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> boot option
        time.sleep(self.interval)
        auto.typewrite(['\n','\n','down','\n','\n'])  #-> use UEFI pending reboot
        step = 'UEFI'
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> network option
        time.sleep(self.interval)
        auto.typewrite(['\n'])  #-> network boot option
        time.sleep(self.interval)
        auto.typewrite(['down','down','down','down','down','down','\n','down','\n'])  #-> disable LOM1
        time.sleep(self.interval)
    
        if self.FLOM == 'yes':
            auto.typewrite(['down','down','down','down','\n','down','\n'])  #-> disable FLOM1 
            time.sleep(self.interval)

        step = 'NIC'
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc','esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n'])  #-> power option
        time.sleep(self.interval)       
        step = 'power'
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc']) #->BIOS

        # auto.typewrite(['esc','\n','\n'])  #-> save config
        # time.sleep(self.interval)
        # auto.typewrite(['esc'])  #-> system utilites
        # time.sleep(self.interval) 
        # auto.press('f12')    


    def VSOE(self,srv):
        self.go_bios()
        time.sleep(self.interval)
        time.sleep(self.interval)
        #virtual max perf

    def LSOE(self,srv):
        self.go_bios()
        auto.typewrite(['down','\n'])  #-> iLO option 
        time.sleep(self.interval)
        auto.typewrite(['down','down','down','\n'])  #-> setting option 
        time.sleep(self.interval) 

    def reboot(self):
        pass

def selectOS(wp,ilo,osv,srv,model='blade',FLOM='no'):
    if ilo == '4':
        ilo = iLO4()
        img = g9sys
    elif ilo == '5':
        ilo = iLO5(srv=srv,model=model,FLOM=FLOM)
        img = g10sys
    else:
        pass

    print(f"Configuring BIOS for {os_dict[osv]}")

    buttonf9 = capture(wp,f9)
    if buttonf9:
        auto.press('f9')
    else:
        exit()

    buttonsys = capture(wp,img)
    if buttonsys:
        if osv == "w":
            ilo.WSOE(srv)
        elif osv == "l":
            ilo.LSOE(srv)
        elif osv == "v":
            ilo.VSOE(srv)
        else:
            print("Wrong Input")
        print("BIOS Configuration Complete")
    else:
        exit()

def main():
    wp = os.path.dirname(os.path.realpath(__file__))
    os.chdir(wp)
    ilo = input('iLO 4 or 5 ?>> ')
    print("w=Windows ; l=Linux ; v=VMware >>")
    osv = input("Select your OS version >>")
    srv = input("Input server name >>  ")
    model = input('Rack(d) or Blade(b) (default b)>> ')
    if model == '' or model == 'b':
        model = 'blade'
    elif model == 'd':
        model = 'rack mounted'
    else:
        print('invalid input')
        exit()
    FLOM = input('Additional FlexLOM card installed ? (Y or N default N) >>')
    if FLOM == '' or FLOM == 'N' or FLOM == 'n':
        FLOM = 'no'
    elif FLOM == 'Y' or FLOM == 'y':
        FLOM = 'yes'
    else:
        print('invalid input')
        exit()    
    
    selectOS(wp,ilo,osv,srv,model,FLOM)

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stop")


"""
Change log:
2019.5.7 create iLO4 class v1.4
2017.12.28 add F9 press function v1.3
2017.6.28 add screen shot funtion v1.2
2017.6.24 add function for WSOE,LSOE v1.1
2017.6.19 build basic function for bl460g9 for VSOE v1.0


Note:
Use this tool after iLO configured
SAN connection is not disabled in BIOS by this tool
From iLO remote console, reset the server
"""
