iimport json
import time
from method import *
import requests
import re
from datetime import date


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

def today_menu(place):

    if place == "복지관":
        num = 2
        title = "복지관2F 교직원 오늘의 식단"
    elif place == "웅지관":
        num = 3
        title = "웅지관1F 한식뷔페 오늘의 식단"

    today = date.today()
    weekday_number = today.weekday()  # 월요일 0 일요일 6

    if weekday_number == 6:
        weekday_number -=6
    else:
        weekday_number += 1

    #date1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))


    response = {
        'restaurant_seq': num,
        'menu_date': date1
    }

    responses = requests.post('https://daegu.ac.kr/restaurant/menu/list', headers = headers, data=response)
    res = responses.json()


    menu_total = []
    temp = res[weekday_number-1]
    #print(temp)
    temp = temp['menu_content']
    
    hangul = re.compile('[^ ㄱ-ㅣ가-힣+]+') # 한글과 띄어쓰기를 제외한 모든 글자
    result = hangul.sub('', temp) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
    result = result.split()

    if len(result) <= 3:
        menu_total.append("등록된 식단이 없습니다")
        #print(menu_total)
    else:
        for j in range(3, len(result)):
            menu_total.append(result[j])
        #print(menu_total)

    menu = '\n'.join(str(e) for e in menu_total)
    response = insert_card(title , menu)
    response = insert_button_text(response, "이번주 식단", "이번주 {}식단".format(place))
    print(response)

    return response

def week_menu(place):

    if place == "복지관":
        num = 2
        title = "복지관2F 교직원 이번주 식단"
    elif place == "웅지관":
        num = 3
        title = "웅지관1F 한식뷔페 이번주 식단"

    today = date.today()
    weekday_number = today.weekday()  # 월요일 0 일요일 6

    if weekday_number == 6:
        weekday_number -=6
    else:
        weekday_number += 1

    date1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    response = {
        'restaurant_seq': num,
        'menu_date': date1
    }

    responses = requests.post('https://daegu.ac.kr/restaurant/menu/list', headers = headers, data=response)
    res = responses.json()
    dateDict = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}

    response = {'version': '2.0', 'template': {
        'outputs': [{"simpleText": {"text": title}},
                    {"carousel": {"type": "basicCard", "items": []}}], 'quickReplies': []}}


    for i in range(len(res)):
        menu_total = []
        temp = res[i]
        temp = temp['menu_content']
        hangul = re.compile('[^ ㄱ-ㅣ가-힣+]+') # 한글과 띄어쓰기를 제외한 모든 글자
        result = hangul.sub('', temp) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
        result = result.split()

        if len(result) <= 3:
            menu_total.append("등록된 식단이 없습니다")
            #print(menu_total)
        else:
            for j in range(3, len(result)):
                menu_total.append(result[j])
            #print(menu_total)

        menu = '\n'.join(str(e) for e in menu_total)
        response = insert_carousel_card(response,"({})".format(dateDict[i]), menu)
        #print(response)
    return response

def cafeteria_parser(content):
    place = content['action']['detailParams']['place_cafeteria']["value"]
    place = ''.join(str(e) for e in place)
    place = place.replace(" ", "")
    print(place)

    if (content['action']['detailParams']['sys_date']) == None:
        response  = today_menu(place)
    else:
        date = content['action']['detailParams']['sys_date']["value"]
        date = ''.join(str(e) for e in date)
        date = date.replace(" ", "")
        if date == '이번주':
            response = week_menu(place)
            print(response)
        else:
            response  = today_menu(place)
            print(response)
    return response 

#content = {'bot': {'id': '646c530b4b9f7d07f1ca18bc!', 'name': 'DU_chatbot'}, 'intent': {'id': '64734812318d31192baf5dbc', 'name': '학식', 'extra': {'reason': {'code': 1, 'message': 'OK'}}}, 'action': {'id': '6473494a6ce345751ec2939a', 'name': '학식메뉴', 'params': {'place_cafeteria': '복지관'}, 'detailParams': {'place_cafeteria': {'groupName': '', 'origin': '복지관', 'value': '복지관'}}, 'clientExtra': {}}, 'userRequest': {'block': {'id': '64734812318d31192baf5dbc', 'name': '학식'}, 'user': {'id': '3aea02e1baec45006253bf44be9a72232d6c1a0b93badd2ce1448159c732e10aed', 'type': 'botUserKey', 'properties': {'botUserKey': '3aea02e1baec45006253bf44be9a72232d6c1a0b93badd2ce1448159c732e10aed', 'bot_user_key': '3aea02e1baec45006253bf44be9a72232d6c1a0b93badd2ce1448159c732e10aed'}}, 'utterance': '복지관', 'params': {'ignoreMe': 'true', 'surface': 'BuilderBotTest'}, 'lang': 'ko', 'timezone': 'Asia/Seoul'}, 'contexts': []}

#cafeteria_parser(content)
