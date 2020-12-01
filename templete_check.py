import requests
import logging
import re
import json
DETECT_URL = "http://192.168.0.5"
MODSEC_FILE = "modsec_audit.log"
TEMPLETE_SHEAT = "bravotec_content.json"


def LastLogFind():
    with open(MODSEC_FILE, "r", encoding="utf-8") as f:
        modsec_log = f.read()

    p = re.compile('[-]{2}\w{8}[-]{1}\w[-]{2}')

    # modsecurity xss 공격 탐지 로그 찾기
    m = p.findall(modsec_log)
    if m:
        return m[-1]
    else:
        return 0


def ModsecLogRead(f):
    modsec_log = f.read()
    return modsec_log
    # print(modsec_log)


def TempleteRead():
    result=[]
    with open(TEMPLETE_SHEAT, "r", encoding="utf-8") as f:

        templetes= f.readlines()
        #print(1)
        #print(templetes)
        for templete in templetes:
            dict = json.loads(templete)
            result.append(dict["content"])
        return result


def XSSLog(modsec_log, f):
    # 정규식
    # p = re.compile('\--\w{8}\-H\--')
    # modsecurity 탐지 파싱 부분 정규식
    p = re.compile('[-]{2}\w{8}[-]{1}H[-]{2}')

    # modsecurity xss 공격 탐지 로그 찾기
    m = p.search(modsec_log)

    if m:
        print("--------------------XSS Attack Detection------------------------")
        f.seek(m.end())
        detect_log = f.read()
        print(detect_log)

    else:
        print("------------------------ No XSS Attack -------------------------")


def TempleteSend(templetes, last_sig):
    f = open("attack_detection.txt", "a", encoding="utf-8")

    for templete in templetes:
        print(templete)
        params = {"templete": templete}
        response = requests.get(DETECT_URL, params=params)
        # mylogger.debug(response.text)
        recent_sig = LastLogFind()
        if last_sig == recent_sig:
            print("No Detection")

            print(last_sig, recent_sig)
            #mylogger.debug(templete)

            # break
        else:
            print("Detection")
            print(last_sig, recent_sig)
            f.write(templete)
            mylogger.debug(templete)
            last_sig = recent_sig
        # return
    f.close()


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
    last_log_signature = LastLogFind()
    mylogger.debug(last_log_signature)
    templetes = TempleteRead()
    #print(templetes)
    TempleteSend(templetes, last_log_signature)


if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.DEBUG)
    mylogger.debug('test')
    main()
