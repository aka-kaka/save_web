import requests
import pandas as pd 
from glob import glob
from os import getcwd
"""
простой запрос на получение данных из ВК по адресу из списка csv
строка с адресом в столбце "Описание"
работает средне
нет картинок

time python3 req_vk1.py                                                                                  130

real    85,00s
user    0,82s
sys     0,09s
cpu     1%


"""

def read_too_pd()->set:
    cur=glob(getcwd()+'/**/**.csv', recursive=True)
    for i in cur:
        try:    
            table=pd.read_csv(i,sep=';')
            start_loop(set(table['Описание']))
        except UnicodeDecodeError:
            print('ошибка в {}',format(i))


def start_loop(html_ref:set):
    for i in html_ref:
        req = requests.get(i)
        with open(getcwd()+'/out/{}.html'.format(i.split('/')[-1]),'wb') as f:
                f.write(req._content)
                print(req.history)

if __name__=="__main__":
    read_too_pd()

