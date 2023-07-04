#!/usr/bin/python3
#coding:utf-8

__version__ = 20210301

from bs4 import BeautifulSoup as bs
from openlink import op_simple,ran_header

import requests


host = "https://bitbk.roche.com"
header = ran_header(ref=host,host=host)
print(header)

def analyze_page(url):
    # bsobj = bs(op_simple(url,header)[0],'html.parser')
    # data = requests.get(url, verify=False, headers=header)
    print(data)
    bsobj = bs(data,'html.parser')
    print(bsobj)
    repo = bsobj.find_all('span',{'class':'repository-name'})
    print(repo)


if __name__ == "__main__":
    url = 'https://bitbk.roche.com/projects/ALICLOUD'
    analyze_page(url)
 