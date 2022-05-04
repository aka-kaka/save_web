
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import pyautogui

import pandas as pd 
from glob import glob
from os import getcwd

'''
такаж фигня что и предидушие, но работате через драйвер браузера
!!!!медленно и не стабильно!!!!
создает сохраненную вэб страницу средствами браузера
должна быть папка out1 в корне браузер сам ее не создаст
сильно зависит от скорости сети

real    118,10s
user    22,84s
sys     4,65s
cpu     23%


real    152,81s
user    24,48s
sys     4,63s
cpu     19%

'''



PATH=getcwd()
DRIVER = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

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
            start=0
            data=tuple(set(table['Описание']))
            while True:
                if counts>stop:
                    counts=stop
                print(f'Всего {stop} записей.Отправляю c {start} по {counts}')
                cor(data[start:counts])
                if counts==stop:
                    break
                else:
                    start,counts=counts, counts+250    
        except UnicodeDecodeError:
            print('ошибка в {}',format(i))


def edit_str_i(i:str) ->str:
    pos=i.index('//')+2
    return i[0:pos]+'m.'+i[pos:]


def cor(html):
    count=0
    tasks=[
        main(edit_str_i(i)) for i in html]
    for task in tasks:
        task
    


def main(txt:str):
    global DRIVER, PATH
    DRIVER.get(txt)
    time.sleep(2)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.typewrite(PATH +'/out1/{}'.format(txt.split('/')[-1].split('?')[0]))
    pyautogui.hotkey('enter')
    time.sleep(1)



if __name__=="__main__":
    read_too_pd()
    DRIVER.quit()
