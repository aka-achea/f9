#!/usr/bin/python
#coding:utf-8
# tested in Win
# Version: 20190507


import time,os,sys
from docx import Document
from docx.shared import Inches
import comtypes.client

"""
Serial Number:          6CU830G700
Site:   SHANGHAI
Area/Building/Room:
IDX2/A24/GSHFRB024A2/Bay9
"""

wp = os.path.dirname(os.path.realpath(__file__))

model_dict = {
    'bl9':('813198-B21','ProLiant BL460c Gen9'),
    'bl10':('','ProLiant BL460c Gen10'),
    'dl10':('868703-B21','ProLiant DL380 Gen10')
}

gsite = ''
gmodel = ''
gdc = ''
grack = ''
genclosure = ''

def sir(srv_dict):
    SIR = os.path.join(wp,'SIR.docx')
    out_file = os.path.join(wp,'%s.pdf' % srv_dict['name'])

    doc = Document(SIR)
    tables = doc.tables

    tinfo = tables[0]
    cName = tinfo.cell(0,0) # (row,column)
    cName.text = 'System Name:      '+srv_dict['name'].upper()
    cSN = tinfo.cell(0,1)
    cSN.text = 'Serial Number:          '+srv_dict['SN'].upper()
    cSite = tinfo.cell(1,0)
    cSite.text = 'Site:   '+srv_dict['site'].upper()
    cloc = tinfo.cell(1,1)
    cloc.text = 'Area/Building/Room:\n'+srv_dict['loc'].upper()

    tmodel = tables[1]
    cProduct = tmodel.cell(1,0)
    cProduct.text = srv_dict['model'][0]
    cDescription = tmodel.cell(1,2)
    cDescription.text = srv_dict['model'][1]

    tsign = tables[3]
    cdate = tsign.cell(1,1)
    cdate.text = '\n'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+'\n'

    # sig = r'E:\UT\signature.png'
    # s = t1.cell(1,2).add_paragraph()
    # r = s.add_run()
    # r.add_picture(sig,width = Inches(0.5), height = Inches(0.5) )

    try:
        doc.save(SIR)
    except PermissionError as e:
        print(e)
        print('Is file being opened?')

    # os.startfile(SIR,'print')

    wdFormatPDF = 17
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(SIR)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()


def main():

    global gsite
    global gmodel
    global gdc
    global grack
    global genclosure

    opt = """
    1. ProLiant BL460c Gen10
    2. ProLiant DL380 Gen10
    3. ProLiant BL460c Gen9
    """
    print(opt)

    m = input('default choice 1 >>>>')
    if m == '3':
        model = model_dict['bl9']
    elif m == '2':
        model = model_dict['dl10']
    elif m == '1' or m == '':
        model = model_dict['bl10']
    else:
        pass

    name = input('Server Name >>>> ')
    SN = input('Serial Number >>>> ')
    site = input('Site (default Shanghai) >>>> ')    
    if site == '': site = 'Shanghai'
    # loc = input('eg:IDX2/A24/GSHFRB024A2/Bay7 >>> ')
    DC = input('DataCenter (default IDX2) >>>>')
    if DC == '': DC = 'IDX2'
    Rack = input('Rack required >>>>')
    if Rack == '' : raise 'Rack info missing'
    loc = f'{DC}/{Rack}'

    if m == '1' or m == '3':
        Enclosure = input('Enclosure >>>>')
        genclosure = Enclosure
        Bay = input('Bay number >>>>')
        if Enclosure != '' and Bay != '':
            loc = f'{loc}/{Enclosure}/Bay {Bay}'

    gsite = site
    gmodel = model
    gdc = DC
    grack = Rack

    srv_dict = {
        'name':name,
        'SN':SN,
        'site':site,
        'loc':loc,
        'model':model
    }

    return srv_dict 

if __name__=='__main__':
    try:
        while True:
            srv_dict = main()
            # sir(srv_dict)
            again = input('One more ? (y or n) ')
            if again == 'y':
                continue
            else:
                break

    except KeyboardInterrupt:
        print('ctrl + c')

