
import aiohttp
import pandas as pd 
from glob import glob
from os import curdir,getcwd
import asyncio
"""
простой запрос на получение данных из ВК по адресу из списка csv
строка с адресом в столбце "Описание"
работает медленно
нет картинок

time python3 req_vk.py                                                                                     1

real    17,41s
user    0,63s
sys     0,08s
cpu     4%


"""

def read_too_pd():
    """
    читаю *.csv в глубину
    start_loop(html_ref) --> из столбца описание передаю строки в start_loop (str 31)
    """
    cur=glob(getcwd()+'/**/**.csv', recursive=True)
    
    for i in cur:
        try:    
            table=pd.read_csv(i,sep=';')
            start_loop(set(table['Описание']))
        except UnicodeDecodeError:
            print('ошибка в {}',format(i))


async def cor(html):
    """
    корутины
    """
    tasks=[main(i) for i in html]
    for task in asyncio.as_completed(tasks):
        await task


def start_loop(html_ref):
    """

    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cor(html_ref))

async def main(txt:str):
    """
    получениеданных
    забираю данные с сайта
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(txt) as response:
            with open(getcwd()+'/out/1111111{}.html'.format(txt.split('/')[-1]),'w') as f:
                #print("Status:", response.status)
                #print("Content-type:", response.headers['content-type'])

                html = await response.text()
                #print("Body:", html[:15], "...")
                f.write(html)

if __name__=="__main__":
    read_too_pd()

