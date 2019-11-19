

import subprocess

import configparser
import paramiko
from pprint import pprint
import pandas as pd
import csv

confile = r'E:\ptool\ilo.ini'

config = configparser.ConfigParser()
config.read(confile)
# host = config['login']['host']
adm = config['login']['adm']
# pword = config['login']['pword']
newuser = config['user']['user']
newuserpd = config['user']['password']
logfile = config['setting']['log']
csvfile = config['setting']['csv']


paramiko.util.log_to_file(logfile,level='DEBUG')

def setup_ilo(host,adm,password):
    '''Create iLO user, get SN, Model'''
    sn,model = '',''
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        client.connect(hostname=host,username=adm,password=pword,
                        allow_agent=False,look_for_keys=False)
        cmd = f'create /map1/accounts1 username={newuser} password={newuserpd} group=admin,config,oemHPE_rc,oemHPE_power,oemHPE_vm'
        client.exec_command(cmd)

        client.connect(hostname=host,username=newuser,password=newuserpd,
                        allow_agent=False,look_for_keys=False)
        stdin, stdout, stderr = client.exec_command('show system1 name')
        output = stdout.read().decode('utf-8').split('\r\n')
        for x in output:
            if 'name=' in x:
                model = x.split('name=')[1]
        stdin, stdout, stderr = client.exec_command('show system1 number')
        output = stdout.read().decode('utf-8').split('\r\n')
        for x in output:
            if 'number=' in x:
                sn = x.split('number=')[1]  
   
    finally:
        client.close()
    return sn,model


# df = pd.read_csv(csv)
# a = df.loc[df.SIR=='Nan']
# print(a)

# sn,model = setup_ilo(host,adm,pword)
# print(sn,model)


with open(csvfile,w) as cf:
    reader = csv.DictReader(cf)
    for row in reader:
        if row['SIR'] == '':
            host = row['iLO']
            pword = row['Pass']
            print(host,pword)