from django.shortcuts import render
from datetime import date, datetime

# import urllib.parse as parser
# import urllib.request as req

import requests
import xml.etree.ElementTree
import json


# DTO 클래스
class Pharmacy:
    def __init__(self, name, address, tel, latitude, longitude):
        self.name = name
        self.address = address
        self.tel = tel
        self.latitude = latitude
        self.longitude = longitude





def list(request):
    
    

    # 오늘의 요일
    week_day = date.today().weekday() + 1
    # 현재 시간을 숫자로 변환
    now = datetime.now()
    now_time = now.hour * 60 + now.minute
    
    url = 'http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire'

    # 분당에 약국이 약 260개 정도 존재하는 것 같음 (한번에 전체를 조회하기 위해 300건으로 고정하였음)
    params = {
        'serviceKey' : 'j3l4/lL9sulpZEYY467tIsTngXuIhRTIddhNB4wrTzRNtaGQ5w6eGH1Jah/mXu2JMdja84GrX0hrpsZ1dludpw==',
        'Q0' : '경기도',
        'Q1' : '분당구',
        'QT' : week_day,
        'numOfRows' : 10
    }

    # param = parser.urlencode(params)
    # url = url + param
    # res = req.urlopen(url).read()
    
    response = requests.get(url, params=params)
    response.encoding = 'utf-8'

    # print(response.text)

    trees = xml.etree.ElementTree.fromstring(response.text)

    keyword1 = 'dutyTime' + str(week_day) + 's'
    keyword2 = 'dutyTime' + str(week_day) + 'c'
    

    list = []
    # 현재 시간과 약국의 영업시간을 비교하여 오픈 상태인 약국만 걸러낸다.
    for tree in trees[1][0]:
        start_time_str = tree.find(keyword1).text
        end_time_str = tree.find(keyword2).text

        if start_time_str and end_time_str:
            start_time = int(start_time_str[0:2]) * 60 + int(start_time_str[2:])
            end_time = int(end_time_str[0:2]) * 60 + int(end_time_str[2:])
            if start_time <= now_time <= end_time:
                address = tree.find('dutyAddr').text
                name = tree.find('dutyName').text
                tel = tree.find('dutyTel1').text
                latitude = tree.find('wgs84Lat').text
                longitude = tree.find('wgs84Lon').text

                # pharm = {'name' : name, 'address' : address, 'tel' : tel, 'latitude' : latitude, 'longitude' : longitude}
                
                pharm = Pharmacy(name, address, tel, latitude, longitude)
                list.append(pharm)


    # context = {'json' : json.dumps(list, ensure_ascii=False)}
    context = {'pharm_list' : list}

    return render(request, 'pharmacy/list.html', context)
