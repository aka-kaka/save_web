import aiohttp
import pandas as pd 
from glob import glob
from os import getcwd
import asyncio

"""
простой запрос на получение данных из ВК по адресу из списка csv
строка с адресом в столбце "Описание"
нет картинок

кидает по 250 запросов в сек //вроде 0_о

time python3 aiohttp_req_vk.py

real    9,29s
user    0,58s
sys     0,11s
cpu     7%


"""


def read_too_pd():
    start=0
    counts=250
    """поиск """
    print(getcwd())
    cur=glob(getcwd()+'/**/**.csv', recursive=True)
    print(cur) 
    for i in cur:
        try:
            table=pd.read_csv(i,sep=';')
            stop=len(set(table['Описание']))
            data=tuple(set(table['Описание']))
            while True:
                if counts>stop:
                    counts=stop
                start_loop(data[start:counts])
                if counts==stop:
                    break
                else:
                    start,counts=counts, counts+250    
        except UnicodeDecodeError:
            print('ошибка в {}',format(i))


def edit_str_i(i:str) ->str:
    pos=i.index('//')+2
    return i[0:pos]+'m.'+i[pos:]


async def cor(html):
    tasks=[
        main(edit_str_i(i)) for i in html]
    """
    исключает страницы профиля с фото
    на них есть ограничения у ВК по колличеству запросов в сек
    """
    """
    tasks=[
        main(edit_str_i(i)) for i in html
        if 'photo' not in i]
     """
    for task in asyncio.as_completed(tasks):
        await task


def start_loop(html_ref):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cor(html_ref))


async def main(txt:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(txt) as response:
            with open(getcwd()+'/out/{}.html'.format(txt.split('/')[-1]),'w') as f:


                html = await response.text()

                f.write('<meta charset="utf-8">')
                f.write(html)


if __name__=="__main__":
    read_too_pd()

