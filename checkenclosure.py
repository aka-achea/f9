# !/usr/bin/python3
# coding:utf-8
# tested in Win

__version__ = 20200511

import re,subprocess,os,configparser,openpyxl



confile = r'E:\ptool\enclosure\setting.txt'
config = configparser.ConfigParser()
config.read(confile)
workpath = config['setting']['workpath']
plink = config['setting']['plink']
enlist = os.path.join(workpath,config['setting']['enclosurelist'])
puttycmd = os.path.join(workpath,config['setting']['puttycmd'])
puttylog = os.path.join(workpath,config['setting']['puttylog'])
filterlog = os.path.join(workpath,config['setting']['filterlog'])
xls = os.path.join(workpath,config['setting']['layout'])
user = config['setting']['user']
password = config['setting']['pass']


def get_xls_num(xls):
    '''Get Enclosure list with blades number from inventory'''
    wb = openpyxl.load_workbook(xls,data_only=True)
    sheet = wb['Overview']
    max = sheet.max_row
    edict = {
        sheet.cell(row=x,column=4).value :
        sheet.cell(row=x,column=6).value 
        for x in range(7,max+1)
        }
    # print(edict)
    return edict


def pquery():
    '''Putty to check enclosure blade '''
    if os.path.exists(puttylog):
        os.remove(puttylog)
    with open(enlist,'r') as e:
        for x in e.readlines():
            oa = x.split('\n')[0]
            cmd = f'echo y | {plink} -ssh -m {puttycmd} -pw {password} {user}@{oa} >> {puttylog} 2>&1'
            # print(cmd)
            subprocess.run(cmd,shell=True)


def filter_log(edict):
    '''Filter putty log and compare with inventory'''
    if os.path.exists(filterlog):
        os.remove(filterlog)
    ndict = {}
    with open(filterlog,'w') as o:
        with open(puttylog,'r') as f:
            for x in f.readlines():
                if re.search('\[SCRIPT MODE\]> show server names',x):
                    ename = x.split()[0][:-3].upper()
                    if ename == 'SHPFRB009J32': ename = 'SHPFRB009J3'
                    if ename == 'OA-9457A55F5': ename = 'SICFRB005CE2'
                    print(ename,file=o)
                elif re.search('Totals',x):
                    total = x.split('\n')[0]
                    print(total,file=o)                     
                    ndict[ename] = total.split(' ')[1]
                    # print(edict[ename])
                    if int(ndict[ename]) != int(edict[ename]):
                        print(f'!!!!!!!!!!! Blade number from {edict[ename]} to {ndict[ename]} !!!!!!!!!!!',file=o)
                    else:
                        pass
                        # print('SAME',file=o)
                    print('-'*10,file=o)
                else:
                    pass


def main():
    edict = get_xls_num(xls)
    pquery()
    filter_log(edict)


if __name__ == "__main__":
    main()