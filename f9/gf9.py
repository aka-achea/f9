import os
import PySimpleGUI as sg      
from multiprocessing import Process,freeze_support

from f9 import selectOS,os_dict,hw_dict

wp = os.path.dirname(os.path.realpath(__file__))

  
layout = [           
    [sg.InputCombo(tuple(hw_dict[x] for x in hw_dict.keys()),size=(13, 1),key='hw',default_value=hw_dict['b10'],readonly=True),
     sg.InputCombo(tuple(os_dict[x] for x in os_dict.keys()),size=(16, 1),key='osv',default_value=os_dict['v'],readonly=True) ], 
    [sg.Checkbox('Additional FlexLOM card installed', size=(30,1), default=False,key='FLOM')],
    [sg.Text('Server Name', size=(10, 1)), sg.InputText(size=(20, 1),key='srv')],    
    # [sg.Text('_'*36,justification='center')],          
    [sg.Text('',size=(36,2),key='output')],          
    # [sg.Text('_'*36,justification='center')],
    [sg.Button('Go',tooltip='Click to start',key='go'),sg.Button('Stop',key='stop',disabled=True),
     sg.Button('Reset',tooltip='Reset to default value',key='reset'),
     sg.Button('Help'),sg.Button('Exit')]      
]      

window = sg.Window('BIOS Config Tool', layout, default_element_size=(40, 1),
             grab_anywhere=False,size=(300,160),icon=os.path.join(wp,'img','f9.ico'))      


def decision(values):
    pass


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
            window.FindElement('stop').Update(disabled=False)
            window.FindElement('go').Update(disabled=True)
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
            r = gobios(wp,ilo,osv,srv,model,FLOM)
            print(r)
            window.Element('output').Update(r)

            # print(result)
            # if result:
            #     # window.Element('output').Update(f'BIOS configuration complete for {srv}')
            #     window.Element('output').Update(result)
            # elif result == False:
            #     window.Element('output').Update(f'BIOS configuration failed')
            # else:
            #     window.Element('output').Update(result)

        elif event == 'stop':  
            window.FindElement('stop').Update(disabled=True)
            window.FindElement('go').Update(disabled=False)            
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
                window.Element('output').Update(f'Job Cancelled')
        
        elif event == 'reset':         
            try:
                setupbios.terminate()
                setupbios.close()
                window.FindElement('stop').Update(disabled=True)
                window.FindElement('go').Update(disabled=False)  
            except ValueError:
                pass
            except AttributeError as e:
                print(e) 
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
                '* Only support Java Web Start console',
                '* SAN connection is not disabled in BIOS by this tool',
                title='Note',icon=os.path.join(wp,'img','f9.ico')
            )

        elif event == 'Exit':
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