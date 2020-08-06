#!/usr/bin/python3
#!python*
#coding = utf-8

import os
import time
import requests
import json
from collections import deque

tmp = deque(maxlen=5)
year = input('Enter the race year[yyyy]: ')
month = input('Enter the race month[mm]: ')
day = input('Enter the race day[dd]: ')
racecourse = input('Enter the racecourse[st|hv]: ') 
race_no = input('Enter the race[1-11]: ') 
second = input('Enter the refresh seconds[30-60]:') 
command = ['clear', 'cls'][os.name == 'nt']

def get_odds(a):
    if len(a) == 1:
        return list(zip([0]*len(a[0]), a[0]))
    elif len(a) == 2:
        x, y = a
        return list(zip(x, y))
    elif len(a) == 3:
        x, y, z = a
        return list(zip(x, y, z))
    elif len(a) == 4:
        x, y, z, i = a
        return list(zip(x, y, z, i))
    elif len(a) == 5:
        x, y, z, i, j = a
        return list(zip(x, y, z, i, j))
    
def main(year, month, day, racecourse, race_no, second):
 
    session = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    #url = 'https://bet.hkjc.com/racing/getJSON.aspx?type=win&date={}-{}-{}&venue={}&raceno={}'.format(year, month, day, racecourse, race_no)
    url = 'https://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date={}-{}-{}&venue={}&start={}&end=11'.format(year, month, day, racecourse, race_no)

    html = session.post(url=url, headers=headers)
    datas = json.loads(html.text)
    datas1 = datas['OUT'].split(';')
    datas2 = [float(x.split('=')[1]) for x in datas1[1:]]
    min_odds = min(datas2)
    tmp.append(datas2)
    odds_tuple = get_odds(tmp)
    for index, odds in enumerate(odds_tuple, 1):
        if odds[-2] > odds[-1]:
            rate = round((odds[-2] - odds[-1]) / odds[-2]*100, 2)
            thumb = '↓'
        else:
            rate = ''
            thumb = ''
        if odds[-1] == min_odds:
            print(index, '***', odds, thumb, rate)
        else:
            print(index, '->', odds, thumb, rate)
    print('Current race {}'.format(race_no))
    print('[Ctrl + C] to change the race no......')
    time.sleep(int(second))
    
while True:
    os.system(command)
    try:
        main(year, month, day, racecourse, race_no, second)
    except KeyboardInterrupt:
        race_no = input('Enter the Race: ')
        tmp = deque(maxlen=5)
    except ValueError:
        input('Odds has not started yet,please wait.')
    except:
        input('Undefined error......')
