#version:20191118

import os
import PySimpleGUI as sg      
from multiprocessing import Process,freeze_support

from f9 import selectOS,os_dict,hw_dict

wp = os.path.dirname(os.path.realpath(__file__))
version = '2.0'
  
layout = [           
    [sg.InputCombo(tuple(hw_dict[x] for x in hw_dict.keys()),size=(13, 1),key='hw',default_value=hw_dict['460g10'],readonly=True),
     sg.InputCombo(tuple(os_dict[x] for x in os_dict.keys()),size=(16, 1),key='osv',default_value=os_dict['v'],readonly=True) ], 
    [sg.Checkbox('Additional FlexLOM card installed', size=(30,1), default=False,key='FLOM')],
    [sg.Checkbox('Enable auto F9 recognition', size=(30,1), default=True,key='autof9',tooltip='')],
    [sg.Text('Server Name', size=(10, 1)), sg.InputText(size=(20, 1),key='srv')],    
    # [sg.Text('_'*36,justification='center')],          
    [sg.Text('',size=(36,2),key='output')],          
    # [sg.Text('_'*36,justification='center')],
    [sg.Button('Go',tooltip='Click to start',key='go'),sg.Button('Stop',key='stop',disabled=True),
     sg.Button('Reset',tooltip='Reset to default value',key='reset'),
     sg.Button('Help'),sg.Button('Exit')]      
]      

window = sg.Window(f'BIOS Config Tool {version}', layout, default_element_size=(40, 1),
             grab_anywhere=False,size=(300,200),icon=os.path.join(wp,'img','f9.ico'))      



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

        elif event == 'go':  
            for x in ['go','hw','osv','FLOM','autof9','srv']:
                window.FindElement(x).Update(disabled=True)
            window.FindElement('stop').Update(disabled=False)
            if values['hw'] == hw_dict['460g10']:
                ilo = '5'
                model = 'blade'
            elif values['hw'] == hw_dict['380g10']:
                ilo = '5'
                model = 'rack mounted'            
            elif values['hw'] == hw_dict['460g9']:
                ilo = '4'
                model = 'blade'
            elif values['hw'] == hw_dict['580g10']:
                ilo = '5'
                model = 'rack mounted'
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
            autof9 = values['autof9']
            # print(autof9)
            window.Element('output').Update(f'Configuring BIOS for {srv}')
            gobios(wp,ilo,osv,srv,model,FLOM,autof9)
            # window.Element('output').Update('Complete')

            # print(result)
            # if result:
            #     # window.Element('output').Update(f'BIOS configuration complete for {srv}')
            #     window.Element('output').Update(result)
            # elif result == False:
            #     window.Element('output').Update(f'BIOS configuration failed')
            # else:
            #     window.Element('output').Update(result)

        elif event == 'stop':  
            for x in ['go','hw','osv','FLOM','autof9','srv']:
                window.FindElement(x).Update(disabled=False)
            window.FindElement('stop').Update(disabled=True)
            terminate_go()
            window.Element('output').Update(f'Job Cancelled')
        
        elif event == 'reset':  
            terminate_go()   
            for x in ['go','hw','osv','FLOM','autof9','srv']:
                window.FindElement(x).Update(disabled=False)    
            window.FindElement('stop').Update(disabled=True)
            window.FindElement('hw').Update(hw_dict['460g10'])
            window.FindElement('osv').Update(os_dict['v'])
            window.FindElement('FLOM').Update(False)
            window.FindElement('autof9').Update(True)
            window.FindElement('srv').Update('')
            window.FindElement('output').Update('')

        elif event == 'Help':
            sg.Popup(
                'Recommend to run on jumpstation after iLO configured',
                'From iLO remote console, reset the server, maximize console window, place it in up/left corner', 
                '* Only support run one instance at one time',
                '* Only support Java Web Start console',
                '* SAN connection is not disabled in BIOS by this tool',
                'More details: See README',
                title='Help',icon=os.path.join(wp,'img','f9.ico')
            )

        elif event == 'Exit':
            terminate_go()
            window.Element('output').Update(f'Job Cancelled')
            break

    window.Close()

def terminate_go():
    try:
        # setupbios.join()
        setupbios.terminate()
        setupbios.close()
        # break
    except AttributeError as e:
        print(e) 
        pass
    except ValueError as e:
        print(e)
    

def gobios(wp,ilo,osv,srv,model,FLOM,autof9):
    global setupbios
    setupbios = Process(target=selectOS,args=(wp,ilo,osv,srv,model,FLOM,autof9,))
    setupbios.start()
    # setupbios.join()



if __name__ == "__main__":
    freeze_support()
    try:
        gf9()
    except KeyboardInterrupt:
        print('ctrl + c')
    