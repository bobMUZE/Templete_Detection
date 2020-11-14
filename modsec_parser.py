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
        recent_log=f.read()
        return(recent_log)
    else:
        return 0



def Find_Message_Column(recentLog):
    messageColumnRe = "Message: Warning. Pattern match [\s\S]*?[\\n]"
    p = re.compile(messageColumnRe)
    messages = p.findall(recentLog)
    return messages

def Find_Matched_Pattrn(message):
    matchedPatternRe="Pattern match \"[\s\S]*?\" at ARGS:"
    p = re.compile(matchedPatternRe)
    matchedPattern = p.findall(message)
    return matchedPattern[0][15:-10]

def Find_Matched_Data(message):
    matchedDataRe="\\[data \"Matched Data: [\s\S]*?found within ARGS:"
    #print(matchedDataRe)
    p = re.compile(matchedDataRe)
    matchedData = p.findall(message)
    #print(matchedData[0])
    return matchedData[0][21:-19]

def Find_Matched_Info(recentLog):
    messages=Find_Message_Column(recentLog)
    result={}
    for message in messages:
        matchedPattern=Find_Matched_Pattrn(message)
        matchedData=Find_Matched_Data(message)
        #print(message)
        #print(matchedPattern,"--:--",matchedData)
        result[matchedPattern]=matchedData
    return result



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
    recentLog=XSSLog(modsec_log,f)
    print(recentLog)
    if recentLog!=0:
        rule_and_string=Find_Matched_Info(recentLog)
        print(rule_and_string)


if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
