import requests
import logging
import re

DETECT_URL="http://192.168.0.5"
MODSEC_FILE="/var/log/apache2/modsec_audit.log"
CHEAT_SHEAT="xss_attack.txt"

def LastLogFind():

    with open(MODSEC_FILE,"r",encoding="utf-8") as f:
        modsec_log=f.read()

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
    #print(modsec_log)


def XSSAtackRead():
    with open(CHEAT_SHEAT,"r",encoding="utf-8") as f:
        xss_attacks=f.readlines()
        return xss_attacks



def XSSLog(modsec_log,f):
    #정규식
    #p = re.compile('\--\w{8}\-H\--')
    # modsecurity 탐지 파싱 부분 정규식
    p = re.compile('[-]{2}\w{8}[-]{1}H[-]{2}')

    # modsecurity xss 공격 탐지 로그 찾기
    m = p.search(modsec_log)

    if m:
        print("--------------------XSS Attack Detection------------------------")
        f.seek(m.end())
        detect_log=f.read()
        print(detect_log)

    else:
        print("------------------------ No XSS Attack -------------------------")

def TempleteSelect():
    with open("templete.txt","r",encoding="utf-8") as f:
        templete=f.read()
        return templete

def AttackSend(attacks,last_sig):
    f= open("no_detection_attack.txt","a",encoding="utf-8")
        
    for attack in attacks:
        print(attack)
        params = {"attack": attack}
        response = requests.get(DETECT_URL, params=params)
        #mylogger.debug(response.text)
        recent_sig=LastLogFind()
        if last_sig==recent_sig:
            print("No Detection")
            f.write(attack)
            print(last_sig,recent_sig)
            mylogger.debug(attack)

            #break
        else:
            print("Detection")
            print(last_sig,recent_sig)
            
            mylogger.debug(attack)
            last_sig=recent_sig
        #return
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
    xss_attacks=XSSAtackRead()
    AttackSend(xss_attacks,last_log_signature)

    #TempleteSend(templete)

    #modsec_file="modsec_audit.log"
    #f = open(modsec_file, "r")
    #modsec_log=ModsecLogRead(f)
    #XSSLog(modsec_log,f)
if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.DEBUG)
    mylogger.debug('test')
    main()
