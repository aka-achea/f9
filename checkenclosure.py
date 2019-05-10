# !/usr/bin/python3
# coding:utf-8
# tested in Win

import re,subprocess,os,configparser



confile = r'E:\ptool\enclosure\setting.txt'
config = configparser.ConfigParser()
config.read(confile)
workpath = config['setting']['workpath']
plink = config['setting']['plink']
enlist = config['setting']['enclosurelist']
puttycmd = os.path.join(workpath,config['setting']['puttycmd'])
puttylog = os.path.join(workpath,config['setting']['puttylog'])
filterlog = os.path.join(workpath,config['setting']['filterlog'])
user = config['setting']['user']
password = config['setting']['pass']

if os.path.exists(puttylog):
    os.remove(puttylog)
if os.path.exists(filterlog):
    os.remove(filterlog)

with open(enlist,'r') as l:
    for x in l.readlines():
        oa = x.split('\n')[0]
        cmd = 'echo y | {plink} -ssh -m {puttycmd} -pw {password} {user}@{oa} >> {puttylog} 2>&1'
        subprocess.run(cmd,shell=True)

with open(filterlog,'w') as o:
    with open(puttylog,'r') as f:
        for i in f.readlines():
            if re.search('\[SCRIPT MODE\]> show server names',i):
                ename = i.split()[0][:-3].upper()
                print(ename,file=o)
            elif re.search('Totals',i):
                total = i.split('\n')[0]
                print(total,file=o)
                print('='*10,file=o)
                number = total.split(' ')[1]

            else:
                pass
