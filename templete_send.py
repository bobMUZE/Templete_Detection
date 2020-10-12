import requests
import logging
DETECT_URL="http://192.168.0.5"

def TempleteSelect():
    with open("templete.txt","r",encoding="utf-8") as f:
        templete=f.read()
        return templete


def TempleteSend(templete):
    #templete="test"
    params={"templete":templete}
    #url=DETECT_URL+templete
    response = requests.get(DETECT_URL,params=params)
    print(response.text)
    return

# 로깅 함수
def Use_Logging(level):
    mylogger = logging.getLogger("my")

    # 로깅 레벨
    mylogger.setLevel(level)
    stream_hander = logging.StreamHandler()
    mylogger.addHandler(stream_hander)
    mylogger.info("logging start!!!")
    return mylogger

def main():
    templete=TempleteSelect()
    TempleteSend(templete)

if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
