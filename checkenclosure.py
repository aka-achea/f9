# !/usr/bin/python3
# coding:utf-8
# tested in Win

import re,subprocess,os


plink = r'C:\D\_Tool\plink.exe'
pcmd = r'E:\ptool\enclosure\puttycmd.txt'
enlist = r'E:\ptool\enclosure\enlist.txt'
en = r'E:\ptool\enclosure\en.log'
out = r'E:\ptool\enclosure\en-out.log'

if os.path.exists(en):
    os.remove(en)
if os.path.exists(out):
    os.remove(out)

with open(enlist,'r') as l:
    for x in l.readlines():
        oa = x.split('\n')[0]
        cmd = 'echo y | '+plink+' -ssh -m '+pcmd+' -pw 1Piithon$ BELANO@'+oa+'>>'+en+' 2>&1'
        # print(cmd)
        # args = shlex.split(cmd)
        # args = ['echo','y','|',plink,'-ssh','-m',pcmd,'-pw','1Piithon$','BELANO@'+oa,'>>',en,'2>&1']
        # print(args)
        subprocess.run(cmd,shell=True)

with open(out,'w') as o:
    with open(en,'r') as f:
        for i in f.readlines():
            if re.search('\[SCRIPT MODE\]> show server names',i):
                print(i.split()[0],file=o)
            elif re.search('Totals',i):
                print(i.split('\n')[0],file=o)
                print('='*10,file=o)
            else:
                pass
