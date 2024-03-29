#!/usr/bin/python3
#coding:utf-8
#version:20191118

"""
BIOS Setup Automation Tool
"""

import time , os
import pyautogui as auto


wp = os.path.dirname(os.path.realpath(__file__))

g10sys = 'g10sys'
g9sys = 'sys'
f9 = 'F9'
# flom = 'FLOM'
# g10power = 'g10power'
g10bios = 'g10bios'

os_dict = {
    'w':'WSOE (Windows)',
    'l':'LSOE (Linux)',
    'v':'VSOE (VMware)',
    's':'SSOE (Suse)'
}
 
hw_dict = {
    '380g10':'HP DL380 G10',
    '460g10':'HP BL460 G10',
    '460g9':'HP BL460 G9',
    '580g10':'HP DL580 G10'
}


auto.size()
width, height = auto.size()
#print(width,height)
auto.PAUSE = 1


def capture(wp,img,trys=10):
    '''Locate image and return (x,y)'''    
    pic = os.path.join(wp,'img',img+'.bmp')
    # print(pic)
    trytime = 1
    while trytime < trys:
        try:
            button = auto.locateCenterOnScreen(pic,grayscale=True,confidence=0.99)
            time.sleep(3)
            # print('Find '+img)
            #print(button)
            # auto.click(button)
            break            
        except TypeError:
            time.sleep(15)
            trytime += 1
            print(f'try to locate {img} {str(trytime)}')
            continue

        except OSError as e:
            print(e)
            return e
    else:
        print(f"Max tries reach")
        return f"Max tries reach, no find {img}"
    print(f'Find {img}')
    return button


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
        return 'BIOS configure complete'

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
        return 'BIOS configure complete'

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
        return 'BIOS configure complete'

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
    def __init__(self,srv,waitsec=2,model='blade',FLOM='no',autof9=True):
        self.interval = waitsec
        self.model = model
        self.FLOM = FLOM
        self.srv = srv
        self.autof9 = autof9
        # print(f'{self.srv} server model is {self.model} has {self.FLOM} FlexLOM installed')

    def go_bios(self):
        if capture(wp,g10bios):
            auto.typewrite('\n') #-> BIOS   
        else:
            # print('something wrong')
            return 'something wrong'

        
    def WSOE(self,srv):
        if self.autof9:
            self.go_bios()
        w = 'WSOE'
        time.sleep(3)
        auto.typewrite('\n')
        time.sleep(self.interval)
        auto.typewrite(['up','\n','\n'])  #-> change workload for general power efficient
        step = 'workload'
        time.sleep(0.5)
        screenshot(self.srv,w,step)
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> system option
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> serial port
        time.sleep(self.interval)
        auto.typewrite(['\n'])  #-> EMS
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','down','\n'])  #-> serial port 9600
        step = 'EMS'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #-> serial port

        if self.model == 'rack mounted':
            time.sleep(self.interval)
            auto.typewrite(['down','\n','up','\n'])  #-> for DL serial port
            time.sleep(0.5)
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
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->system option
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> Server availability
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','\n','down','\n'])  #-> disable WoL
        step = 'WoL'
        time.sleep(0.5)
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
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> boot option
        time.sleep(self.interval)
        auto.typewrite(['\n','\n','down','\n','\n'])  #-> use UEFI pending reboot
        step = 'UEFI'
        time.sleep(2)
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
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc','esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n'])  #-> power option
        step = 'power'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.press('f12')   
        auto.typewrite(['\n','\n'])  #-> save config
        
        # time.sleep(self.interval)
        # auto.typewrite(['esc'])  #-> system utilites
        # time.sleep(self.interval) 
        return 'BIOS configure complete'

    def LSOE(self,srv):
        if self.autof9:
            self.go_bios()
        w = 'LSOE'
        time.sleep(4)
        auto.typewrite('\n')
        time.sleep(self.interval)
        auto.typewrite(['up','up','\n','\n'])  #-> custom load
        # auto.typewrite(['up','\n','\n'])  #-> change workload for general power efficient   
        step = 'workload'
        time.sleep(1)
        screenshot(self.srv,w,step)
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> system option
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> serial port
        time.sleep(self.interval)
        auto.typewrite(['\n'])  #-> EMS
        time.sleep(self.interval)
        auto.typewrite(['\n','down','down','\n'])  #-> serial port
        step = 'EMS'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #-> serial port

        if self.model == 'rack mounted':
            time.sleep(self.interval)
            auto.typewrite(['down','\n','up','\n'])  #-> for DL serial port
            step = 'DL serial port'
            time.sleep(0.5)
            screenshot(self.srv,w,step) 
            time.sleep(self.interval)

        auto.typewrite(['esc']) #->system option
        time.sleep(self.interval)
        auto.typewrite(['up']) #->back to boot time postion
        time.sleep(self.interval)    
        auto.typewrite(['down','down','down','\n'])  #-> Server availability
        time.sleep(self.interval)
        auto.typewrite(['\n','down','\n'])  #-> disable ASR
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','\n','down','\n'])  #-> disable WoL
        step = 'WoL+ASR'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->system option
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> Processor Option
        time.sleep(self.interval)
        auto.typewrite(['\n','down','\n'])  #-> disable HyperThreading
        step = 'HT'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n'])  #-> Virtualization Option
        time.sleep(self.interval)
        auto.typewrite(['\n','down','\n'])  #-> disable VT
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','\n'])  #-> disable VTd
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','\n'])  #-> disable SRIOV
        step = 'virt'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> boot option
        time.sleep(self.interval)
        auto.typewrite(['\n','\n','down','\n','\n'])  #-> use UEFI pending reboot
        step = 'UEFI'
        time.sleep(2)
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

        auto.typewrite(['\n','\n','down','down','\n'])  # -> Static High
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','down','\n'])  #-> No C-state
        time.sleep(self.interval) 
        auto.typewrite(['down','\n','down','down','\n'])  #-> No package state
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','up','\n'])  # -> Max Perf
        time.sleep(0.5)
     
        step = 'power'
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.press('f12')   
        auto.typewrite(['\n','\n'])  #-> save config
        return 'BIOS configure complete'

    def VSOE(self,srv):
        if self.autof9:
            self.go_bios()
        w = 'VSOE'
        time.sleep(4)
        auto.typewrite('\n')
        time.sleep(self.interval)
        # auto.typewrite(['up','\n','\n'])  #-> change workload for general power efficient
        auto.typewrite(['up','up','\n','\n'])  #-> custom load       
        step = 'workload'
        time.sleep(1)
        screenshot(self.srv,w,step)
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> system option
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> serial port
        time.sleep(self.interval)
        auto.typewrite(['\n'])  #-> EMS
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','down','\n'])  #-> serial port 9600
        step = 'EMS'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #-> serial port
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','\n'])  #-> disable embed port
        time.sleep(self.interval)
        auto.typewrite(['esc']) #-> system option
        auto.typewrite(['down','down','\n'])  #-> Server availability
        time.sleep(self.interval)
        auto.typewrite(['\n','down','\n'])  #-> disable ASR
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','\n','down','\n'])  #-> disable WoL
        step = 'WoL+ASR'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->system option
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','down','down','\n'])  #-> Virtual Option
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','\n'])  #-> disable VTd
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','\n'])  #-> disable SRIOV
        step = 'virt'
        time.sleep(0.5)
        screenshot(self.srv,w,step) 
        time.sleep(self.interval)
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.typewrite(['down','\n'])  #-> boot option
        time.sleep(self.interval)
        auto.typewrite(['\n','\n','down','\n','\n'])  #-> use UEFI pending reboot
        step = 'UEFI'
        time.sleep(2)
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

        auto.typewrite(['\n','\n','down','down','\n'])  # -> Static High
        time.sleep(self.interval)
        auto.typewrite(['down','\n','down','down','\n'])  #-> No C-state
        time.sleep(self.interval) 
        auto.typewrite(['down','\n','down','down','\n'])  #-> No package state
        time.sleep(self.interval)    
        auto.typewrite(['down','down','\n','up','\n'])  # -> Max Perf
        time.sleep(0.5)

        step = 'power'
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        auto.press('f12')   
        auto.typewrite(['\n','\n'])  #-> save config
        return 'BIOS configure complete'


def selectOS(wp,ilo,osv,srv,model='blade',FLOM='no',autof9=True):
    gdir = os.path.join(wp,srv)
    if not os.path.exists(gdir):
        os.makedirs(gdir)
    os.chdir(gdir)

    if ilo == '4':
        ilo = iLO4()
        sysconf = g9sys
    elif ilo == '5':
        ilo = iLO5(srv=srv,model=model,FLOM=FLOM,autof9=autof9)
        sysconf = g10sys
    else:
        return 'Unsupported hardware'

    print(f"Configuring BIOS for {os_dict[osv]}")

    if autof9:
        buttonf9 = capture(wp,f9)
        if isinstance(buttonf9,tuple):
            auto.click(buttonf9)
            auto.press('f9')
        else:
            print(buttonf9)
            return buttonf9
        buttonsys = capture(wp,sysconf)
        if isinstance(buttonsys,tuple):
            auto.typewrite('\n')
        else:
            print(buttonsys)
            return buttonsys

    if osv == "w":
        result = ilo.WSOE(srv)
    elif osv == "l" or osv == 's':
        result = ilo.LSOE(srv)
    elif osv == "v":
        result = ilo.VSOE(srv)
    else:
        return 'Unsupported OS edition'
    print(result)
    return result


def main():
    os.chdir(wp)
    ilo = input('Gen9 or Gen 10 ? (default 10) >>>>')
    if ilo == '' or ilo == '10': 
        ilo = '5'
    elif ilo == '9':
        ilo = '4'
    else:
        print('invalid input')
        exit()

    print("w=Windows ; l=Redhat/Suse ; v=VMware ")
    osv = input("Select your OS version (default: v) >>>>")
    if osv == 'v' or osv == '':
        model = 'blade'
        FLOM = 'no'
        osv = 'v'
    else:
        model = input('Rack(d) or Blade(b) (default b) >>>>')
        if model == '' or model == 'b':
            model = 'blade'
        elif model == 'd':
            model = 'rack mounted'
        else:
            print('invalid input')
            exit()
        FLOM = input('Additional FlexLOM card installed ? (Y or N default N) >>>>')
        if FLOM == '' or FLOM == 'N' or FLOM == 'n':
            FLOM = 'no'
        elif FLOM == 'Y' or FLOM == 'y':
            FLOM = 'yes'
        else:
            print('invalid input')
            exit()    

    srv = input("Input server name >>>>  ")
    if srv == '':
        print('Server Name missing')

    selectOS(wp,ilo,osv,srv,model,FLOM)
    print("BIOS Configuration Complete")
    # again = input('One more ? (default no) >>>>')


if __name__=='__main__':
    try:
        while True:
            main()
            again = input('One more ? (y or n) ')
            if again == 'y':
                continue
            else:
                break

    except KeyboardInterrupt:
        print("Stop")


"""
Change log:
2019.8.2 add Auto F9 disable function v1.9
2019.8.1 GUI button optimize v1.8
2019.7.31 optimize GUI layout v1.7
2019.5.9 add g10 LSOE, VSOE v1.6
2019.5.8 fix screen capture bug v1.5
2019.5.7 create iLO4 class v1.4
2017.12.28 add F9 press function v1.3
2017.6.28 add screen shot funtion v1.2
2017.6.24 add function for WSOE,LSOE v1.1
2017.6.19 build basic function for bl460g9 for VSOE v1.0


Note:
Use this tool after iLO configured
From iLO remote console, reset the server, maximize the window and place it in up/left corner 
SAN connection is not disabled in BIOS by this tool
Suggest run this tool on jumpstation
"""
