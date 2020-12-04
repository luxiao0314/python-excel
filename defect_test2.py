#!/usr/bin/env python
# encoding: utf-8


import json
import jsonpath
from  sample_data_config import export_result_front_iphone_copy
from  sample_data_config import export_result_front
import requests
import operator
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime


bodylist = []
def getbody():
    yellow_low = ''
    black_high = ''
    light_off_white = ''

    info = export_result_front_iphone_copy.export_result_front_iphone
    for i in range(len(info['data'])):
        phoneType = info['data'][i]['phone_type']
        for key in (json.loads(info['data'][i]['image_info'])).keys():
            if json.loads(info['data'][i]['image_info'])[key].find('1-mta_phone'):
                black_high = key
            if json.loads(info['data'][i]['image_info'])[key].find('2-mta_phone'):
                yellow_low = key
            if json.loads(info['data'][i]['image_info'])[key].find('3-mta_phone'):
                light_off_white = key
            else:
                continue
        body = {
            "photoUrls":
                {"black_high": black_high,
                 "yellow_low": yellow_low,
                 "light_off_white": light_off_white
                 },
            "phoneType": phoneType
        }
        bodylist.append(body)
    return bodylist
# print(getbody())

def boxcolour(body):
    url = "http://192.168.100.93:8101/defect_detection/surface/text"
    data = json.dumps(body, ensure_ascii=False)
    response = requests.request("POST", url, headers={'Content-Type': 'application/json', 'Connection': 'close'}, data=data)
    res = json.loads(response.text)
    # print(1, jsonpath.jsonpath(res, '$..defectType'))
    print(1, res)

starttime = datetime.datetime.now()
THREAD_POOL = ThreadPoolExecutor(3)
with THREAD_POOL as executor:
    executor.map(boxcolour, getbody())
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)