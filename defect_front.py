#!/usr/bin/env python
# encoding: utf-8


import json
import jsonpath
from  sample_data_config import export_result_front_iphone_copy
from  sample_data_config import export_result_front
import requests
import operator
import time

def front():
    yellow_low = ''
    black_high = ''
    light_off_white = ''
    info = export_result_front_iphone_copy.export_result_front_iphone
    # info = export_result_front.export_result_front
    count = 0
    different_defectType = []
    different_defectLength = []

    for i in range(len(info['data'])):
        count += 1
        defect_info = info['data'][i]['defect_info']
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
               {  "black_high": black_high,
                  "yellow_low": yellow_low,
                  "light_off_white": light_off_white
               },
               "phoneType":phoneType
        }
        url = "http://192.168.100.93:8101/defect_detection/surface/text"
        data = json.dumps(body, ensure_ascii=False)
        # print(data)
        time.sleep(3)
        response = requests.request("POST", url, headers={'Content-Type': 'application/json', 'Connection': 'close'}, data=data)
        if response.status_code == 200:
            print("第%s次请求成功" % (count))
        else:
            print("第%s次请求失败" % (count))
        res = json.loads(response.text)
        paths_summary_dict = {}
        for j in range(len(jsonpath.jsonpath(res, '$..defectList')[0])):
            if jsonpath.jsonpath(res, '$..defectList')[0][j].get('defectType') not in paths_summary_dict.keys():
                paths_summary_dict[jsonpath.jsonpath(res, '$..defectList')[0][j].get('defectType')] = jsonpath.jsonpath(res, '$..defectList')[0][j].get('defectLength')
            else:
                if jsonpath.jsonpath(res, '$..defectList')[0][j].get('defectLength') > paths_summary_dict[jsonpath.jsonpath(res, '$..defectList')[0][j].get('defectType')]:
                    paths_summary_dict[jsonpath.jsonpath(res, '$..defectList')[0][j].get('defectType')] = jsonpath.jsonpath(res, '$..defectList')[0][j].get('defectLength')
                else:
                    pass
        if operator.eq(eval(defect_info), paths_summary_dict):
            pass
        elif paths_summary_dict.keys() == eval(defect_info).keys() and paths_summary_dict.values() != eval(defect_info).values():
            different_defectLength.append([{"更新前结果": defect_info},{"更新后结果": paths_summary_dict},{"图片URL": body.get('photoUrls')}])
            # print('缺陷长度不同')
        else:
            different_defectType.append([{"更新前结果": defect_info}, {"更新后结果": paths_summary_dict}, {"图片URL": body.get('photoUrls')}])
            # print('缺陷类型不同')
            # print(paths_summary_dict, defect_info, body.get('photoUrls'))
    return different_defectType,different_defectLength

if __name__ == '__main__':
    result = front()
    print(
        '----front----'
        '\n''检测准确率：%.4f' % ((3-len(result[0])-len(result[1])) / 3),
        '\n''缺陷长度不同:', result[1],
        '\n''缺陷类型不同:', result[0]
    )