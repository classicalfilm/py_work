import requests
import re
import time
import json
import winsound
import telegram
from urllib.request import urlopen

#자코모
TARGET_URL = "https://www.jakomo.co.kr/goods/goods_list.php?cateCd=008004&sort=price_asc&pageNum=30&sort=price_asc"
#마스크
#TARGET_URL = "http://www.welkeepsmall.com/shop/shopbrand.html?type=X&xcode=023"
#쿨패치
#TARGET_URL = 'http://www.welkeepsmall.com/shop/shopbrand.html?type=X&xcode=007'
#핫팩
#TARGET_URL = 'http://www.welkeepsmall.com/shop/shopbrand.html?type=X&xcode=002'
#카톡토큰번호
KAKAO_TOKEN = "teKLsEFRgEmDL4I9g9ePsan_HkVWhcKRujHGBwopb7kAAAFwe-R67g"
#텔레그램토큰번호, CHAT ID
TELEGRAM_TOKEN = "1145213299:AAGTG6XvMKzei910hRWAv9zD62T5XM1G_1c"
#HENRY SHIN 의 CHAT ID
TELEGRAM_CHAT_ID = "1090950244"

#스킵 카운트 = 목적어를 찾고 알림 메세지를 전달한 후, 일정 주기동안 알림 전달을 스킵하는 간격.
SKIP_CNT = 0
#크롤링을 반복하는 주기 (초) 기본 5분 = 60*5
CYCLE_SEC = 30

#웰킵스 사이트 접근하여 html 수집
def find_price():
    html = " "
    try:
        #f = urlopen(TARGET_URL)
        #bytes_content = f.read()
        #encoding = 'cp949'
        #html = bytes_content.decode(encoding)        
        html = requests.get(TARGET_URL).text
    except:
        print(time.strftime('%c', time.localtime(time.time())) +" : "+ "Exception...")
        return -1
    #SOLD OUT 이 아닌 금액정보 건수 수집
    cnt=0
    for partial_html in re.findall(r'루셀', html, re.DOTALL):
        cnt = cnt+1
    return cnt

#텔레그램으로 알림 보내기
class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot = telegram.Bot(token = self.token)    
    def sendMessage(self, chat_id, message):
        try:
            self.bot.sendMessage(chat_id = chat_id, text=message)
        except:
            print("Exception...Start telegram bot !!")
            return

#카톡으로 알림 보내기(나에게 보내기는 가능.알림음이 울리지 않음)
def send_to_kakao(has_price_str):
    header = {"Authorization":'Bearer ' + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send/"
    msg = "마스크가 떴다~~!! 빨리 사러가자~~"+"("+has_price_str+")"
    post = {
        "object_type":"text",
        "text":msg,
        "link":{
            "web_url":TARGET_URL,
            "mobile_web_url":TARGET_URL
        },
        "button_title":"웰킵스몰 바로가기"
    }
    data = {"template_object":json.dumps(post)}
    return requests.post(url, headers=header, data=data)

#비프음 발생
def play_beep():
    freq = 500 # Set frequency To 2500 Hertz
    dur = 1000*5 # Set duration To 1000 ms == 1 second
    winsound.Beep(freq, dur)

if __name__ == "__main__":
    #텔레그램 봇생성
    bot = TelegramBot(TELEGRAM_TOKEN)    
    #타이머 기다리며 반복 시도
    skiping_cnt = 0
    while True: 
        if skiping_cnt == 0:
            has_price = find_price()        
            print(time.strftime('%c', time.localtime(time.time())) +" : "+ str(has_price))

            if has_price > 0:
                play_beep()
                #print(send_to_kakao(str(has_price)))
                bot.sendMessage(TELEGRAM_CHAT_ID, ("마스크가 떴다~~!! 빨리 사러가자~~"+str(has_price))  )                
                skiping_cnt = skiping_cnt+1
        else:
            if skiping_cnt < SKIP_CNT:
                skiping_cnt = skiping_cnt+1
            else:
                skiping_cnt = 0            
            
        time.sleep(CYCLE_SEC)
