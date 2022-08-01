import ntplib
import time

def get():
    c = ntplib.NTPClient() 
    response = c.request('time.stdtime.gov.tw') 
    ts = response.tx_time + 28800
    d = time.strftime('%Y-%m-%d',time.localtime(ts)) 
    t = time.strftime('%X',time.localtime(ts))
    localtime = d + ' ' + t

    return '台灣時間(GMT+8): ' + localtime
