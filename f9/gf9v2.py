import os
import PySimpleGUI as sg      
from multiprocessing import Process,freeze_support

import time
import pyautogui as auto


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
    'r10':'HP DL380 G10',
    'b10':'HP BL460 G10',
    'b9':'HP BL460 G9'
}



wp = os.path.dirname(os.path.realpath(__file__))

  
layout = [           
    [sg.InputCombo(tuple(hw_dict[x] for x in hw_dict.keys()),size=(13, 1),key='hw',default_value=hw_dict['b10'],readonly=True),
     sg.InputCombo(tuple(os_dict[x] for x in os_dict.keys()),size=(16, 1),key='osv',default_value=os_dict['v'],readonly=True) ], 
    [sg.Checkbox('Additional FlexLOM card installed', size=(30,1), default=False,key='FLOM')],
    [sg.Text('Server Name', size=(10, 1)), sg.InputText(size=(20, 1),key='srv')],    
    # [sg.Text('_'*36,justification='center')],          
    [sg.Text('',size=(36,2),key='output')],          
    # [sg.Text('_'*36,justification='center')],
    [sg.Button('Go',tooltip='Click to start'), sg.Button('Stop'),
     sg.Button('Reset',tooltip='Reset to default value'),sg.Button('Help'),sg.Button('Close')]      
]      

window = sg.Window('BIOS Config Tool', layout, default_element_size=(40, 1),
             grab_anywhere=False,size=(300,160),icon=os.path.join(wp,'img','f9.ico'))      



auto.size()
width, height = auto.size()
#print(width,height)
auto.PAUSE = 1


def capture(wp,img,trys=1):
    '''Locate image and return (x,y)'''    
    pic = os.path.join(wp,'img',img+'.bmp')
    # print(pic)
    trytime = 1
    while trytime < trys:
        try:
            button = auto.locateCenterOnScreen(pic,grayscale=True)
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
    def __init__(self,srv,waitsec=2,model='blade',FLOM='no'):
        self.interval = waitsec
        self.model = model
        self.FLOM = FLOM
        self.srv = srv
        # print(f'{self.srv} server model is {self.model} has {self.FLOM} FlexLOM installed')

    def go_bios(self):
        if capture(wp,g10bios):
            auto.typewrite('\n') #-> BIOS   
        else:
            # print('something wrong')
            return 'something wrong'

        
    def WSOE(self,srv):
        self.go_bios()
        w = 'WSOE'
        time.sleep(self.interval)
        auto.typewrite('\n')
        time.sleep(self.interval)
        auto.typewrite(['up','\n','\n'])  #-> change workload for general power efficient
        step = 'workload'
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
        time.sleep(self.interval)
        auto.press('f12')   
        auto.typewrite(['\n','\n'])  #-> save config
        # time.sleep(self.interval)
        # auto.typewrite(['esc'])  #-> system utilites
        # time.sleep(self.interval) 
        return 'BIOS configure complete'

    def LSOE(self,srv):
        self.go_bios()
        w = 'LSOE'
        time.sleep(self.interval)
        auto.typewrite('\n')
        time.sleep(self.interval)
        auto.typewrite(['up','up','\n','\n'])  #-> custom load
        step = 'workload'
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
        auto.typewrite(['down','down','down','\n'])  #-> Server availability
        time.sleep(self.interval)
        auto.typewrite(['\n','down','\n'])  #-> disable ASR
        time.sleep(self.interval)
        auto.typewrite(['down','down','\n','\n','down','\n'])  #-> disable WoL
        step = 'WoL+ASR'
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
        auto.typewrite(['down','\n','down','down','\n'])  #-> No C-state
        time.sleep(self.interval) 
        auto.typewrite(['down','\n','down','down','\n'])  #-> No package state
        time.sleep(self.interval)     
        step = 'power'
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        # auto.press('f12')   
        # auto.typewrite(['\n','\n'])  #-> save config
        return 'BIOS configure complete'

    def VSOE(self,srv):
        self.go_bios()
        w = 'VSOE'
        time.sleep(self.interval)
        auto.typewrite('\n')
        time.sleep(self.interval)
        auto.typewrite(['up','up','\n','\n'])  #-> custom load        
        step = 'workload'
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
        auto.typewrite(['down','\n','down','down','\n'])  #-> No C-state
        time.sleep(self.interval) 
        auto.typewrite(['down','\n','down','down','\n'])  #-> No package state
        time.sleep(self.interval)     
        step = 'power'
        screenshot(self.srv,w,step) 
        auto.typewrite(['esc']) #->BIOS
        time.sleep(self.interval)
        # auto.press('f12')   
        # auto.typewrite(['\n','\n'])  #-> save config
        return 'BIOS configure complete'


def selectOS(wp,ilo,osv,srv,model='blade',FLOM='no'):
    if ilo == '4':
        ilo = iLO4()
        sysconf = g9sys
    elif ilo == '5':
        ilo = iLO5(srv=srv,model=model,FLOM=FLOM)
        sysconf = g10sys
    else:
        return 'Unsupported hardware'

    print(f"Configuring BIOS for {os_dict[osv]}")

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
        if osv == "w":
            ilo.WSOE(srv)
        elif osv == "l" or osv == 's':
            ilo.LSOE(srv)
        elif osv == "v":
            ilo.VSOE(srv)
        else:
            return 'Unsupported OS edition'
    else:
        print(buttonsys)
        return buttonsys




def gf9():
    global setupbios
    setupbios = None
    while True:                 # Event Loop  
        event, values = window.Read()  
        # print(event, values)
        if event is None:            
            try:
                setupbios.terminate()
                setupbios.close() 
            finally:
                break

        elif event == 'Go':  
            if values['hw'] == hw_dict['b10']:
                ilo = '5'
                model = 'blade'
            elif values['hw'] == hw_dict['r10']:
                ilo = '5'
                model = 'rack mounted'            
            elif values['hw'] == hw_dict['b9']:
                ilo = '4'
                model = 'blade'
            else:
                pass

            if values['osv'] == os_dict['w']:   
                osv = 'w'
            elif values['osv'] == os_dict['l']:  
                osv = 'l'
            elif values['osv'] == os_dict['v']:  
                osv = 'v'
            elif values['osv'] == os_dict['s']:  
                osv = 's'
            else:
                pass

            FLOM = 'yes' if values['FLOM'] else 'no'                
            srv = values['srv']
            window.Element('output').Update(f'Configuring BIOS for {srv}')
            gobios(wp,ilo,osv,srv,model,FLOM)

            # print(result)
            # if result:
            #     # window.Element('output').Update(f'BIOS configuration complete for {srv}')
            #     window.Element('output').Update(result)
            # elif result == False:
            #     window.Element('output').Update(f'BIOS configuration failed')
            # else:
            #     window.Element('output').Update(result)

        elif event == 'Stop':  
            try:
                setupbios.terminate()
                # setupbios.join()
                setupbios.close()
                # break
            except AttributeError as e:
                # print(e) 
                pass
            except ValueError:
                window.Element('output').Update(f'Job Cancelled')
        
        elif event == 'Reset':
            try:
                setupbios.terminate()
                setupbios.close()
            except ValueError:
                pass
            window.FindElement('hw').Update(hw_dict['b10'])
            window.FindElement('osv').Update(os_dict['v'])
            window.FindElement('FLOM').Update(False)
            window.FindElement('srv').Update('')
            window.FindElement('output').Update('')

        elif event == 'Help':
            sg.Popup(
                'Recommend to run on jumpstation after iLO configured',
                'From iLO remote console, reset the server, maximize console window, place it in up/left corner', 
                '* Only support run one instance at one time',
                '* SAN connection is not disabled in BIOS by this tool',
                title='Note',icon=os.path.join(wp,'img','f9.ico')
            )

        elif event == 'Close':
            break

    window.Close()


def gobios(wp,ilo,osv,srv,model,FLOM):
    global setupbios
    setupbios = Process(target=selectOS,args=(wp,ilo,osv,srv,model,FLOM,))
    setupbios.start()
    # setupbios.join()



if __name__ == "__main__":
    freeze_support()
    gf9()