import os
import PySimpleGUI as sg      
from multiprocessing import Process

from f9 import selectOS

wp = os.path.dirname(os.path.realpath(__file__))


os_dict = {
    'w':'Windows (WSOE)',
    'l':'Linux (LSOE)',
    'v':'VMware (VSOE)',
    's':'Suse (SSOE)'
}

hw_dict = {
    'r10':'HP DL380 G10',
    'b10':'HP BL460 G10',
    'b9':'HP BL460 G9'
}
  
layout = [           
    [sg.InputCombo((hw_dict['b10'], hw_dict['b9'],hw_dict['r10']), size=(13, 1), key='hw',default_value=hw_dict['b10'],readonly=True) ,
    sg.InputCombo((os_dict['w'], os_dict['l'],os_dict['v'],os_dict['s']), size=(16, 1), key='osv',default_value=os_dict['v'],readonly=True) ], 
    [sg.Checkbox('Additional FlexLOM card installed', size=(30,1), default=False,key='FLOM')],
    [sg.Text('Server Name', size=(10, 1)), sg.InputText(size=(20, 1),key='srv')],    
    # [sg.Text('_'*36,justification='center')],          
    [sg.Text('',size=(36,2),key='output')],          
    # [sg.Text('_'*36,justification='center')],
    [sg.Button('Go',tooltip='Click to start'), sg.Cancel(),sg.Button('Help')]      
]      

window = sg.Window('BIOS Configure Tool', layout, default_element_size=(40, 1),
             grab_anywhere=False,size=(300,160),icon=os.path.join(wp,'img','f9.ico'))      


def decision(values):
    pass

def main():
    while True:                 # Event Loop  
        event, values = window.Read()  
        # print(event, values)
        if event is None or event == 'Cancel':  
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

            if values['FLOM']:
                FLOM = 'yes'
            else:
                FLOM = 'no'

            srv = values['srv']
            window.Element('output').Update(f'Configuring BIOS for {srv}')

            gobios(wp,ilo,osv,srv,model,FLOM)
            # print(result)
            # if result == True:
            #     window.Element('output').Update(f'BIOS configuration complete for {srv}')

            # elif result == False:
            #     window.Element('output').Update(f'BIOS configuration failed')

            # else:
            #     window.Element('output').Update(result)


        elif event == 'Help':
            sg.Popup(
                'Use this tool after iLO configured, suggest run it on jumpstation',
                'From iLO remote console, reset the server, maximize the window and place it in up/left corner', 
                'SAN connection is not disabled in BIOS by this tool',
                title='Note'
            )

    window.Close()


def gobios(wp,ilo,osv,srv,model,FLOM):
    global setupbios
    setupbios = Process(target=selectOS,args=(wp,ilo,osv,srv,model,FLOM,))
    setupbios.start()




if __name__ == "__main__":
    main()