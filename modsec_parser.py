import re
import logging

def ModsecLogRead(f):
    modsec_log = f.read()
    return modsec_log
    #print(modsec_log)


def XSSLog(modsec_log,f):
    #정규식
    #p = re.compile('\--\w{8}\-H\--')
    # modsecurity 탐지 파싱 부분 정규식
    p = re.compile('[-]{2}\w{8}[-]{1}H[-]{2}')
    xss_log=p.findall(modsec_log)

    #최신 XSS 로그 찾기
    latest_xss_log=xss_log[-1]
    log_offset = modsec_log.find(latest_xss_log)
    # modsecurity xss 공격 탐지 로그 찾기
    m = p.search(modsec_log)

    if m:
        print("--------------------XSS Attack Detection------------------------")
        f.seek(log_offset)
        detect_log=f.read()
        print(detect_log)

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
    modsec_file="modsec_audit.log"
    f = open(modsec_file, "r")
    modsec_log=ModsecLogRead(f)
    XSSLog(modsec_log,f)

if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
