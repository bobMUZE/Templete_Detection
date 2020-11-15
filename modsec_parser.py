import re
import logging
import os
import json
import requests

MY_DETECT_URL="http://192.168.0.5"

TEMPLETE_JSON = {'time': '1605365247.624045', 'url': 'http://3.131.17.188/g5', 'module': 1,
                 'filepath': '/home/ubuntu/semicrawling/3.131.17.188/g5/0', 'xpath': '//*[@id="hd"]'}
XSS_TEMPLETE="""
<Video> <source onerror = "javascript: alert (XSS)">
"""

#MODSEC_LOG_FILE="modsec_audit.log"
MODSEC_LOG_FILE="/var/log/apache2/modsec_audit.log"
MUZE_LOG_FILE="muze_log.json"



def LastLogFind():

    with open(MODSEC_LOG_FILE,"r",encoding="utf-8") as f:
        modsec_log=f.read()

    p = re.compile('[-]{2}\w{8}[-]{1}\w[-]{2}')

    # modsecurity xss 공격 탐지 로그 찾기
    m = p.findall(modsec_log)
    if m:
        return m[-1]
    else:
        return 0

def ModsecLogRead():
    with open(MODSEC_LOG_FILE,"r",encoding="utf-8") as f:
        modsec_log=f.read()

    return modsec_log
    #print(modsec_log)


def TempleteSend(templete):
    #templete="test"
    mylogger.info("Send Templete!!!")
    params={"templete":templete}
    print(templete)
    #url=DETECT_URL+templete
    response = requests.get(MY_DETECT_URL,params=params)
    #response = requests.get(DETECT_URL, params=params)
    #print(response.text)
    return

def XSSLog():
    #정규식
    #p = re.compile('\--\w{8}\-H\--')
    # modsecurity 탐지 파싱 부분 정규식
    modsec_log=ModsecLogRead()
    p = re.compile('[-]{2}\w{8}[-]{1}H[-]{2}')
    xss_log=p.findall(modsec_log)

    #최신 XSS 로그 찾기
    latest_xss_log_id=xss_log[-1]
    #print(latest_xss_log)
    log_offset = modsec_log.find(latest_xss_log_id)
    # modsecurity xss 공격 탐지 로그 찾기
    m = p.search(modsec_log)

    if m:
        print("--------------------XSS Attack Detection------------------------")
        #f.seek(log_offset)
        recent_log=modsec_log[log_offset:]
        return(recent_log,latest_xss_log_id)
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

def Find_Matched_Info(recentLog,filepath,lastLogId):
    messages=Find_Message_Column(recentLog)
    result=[]
    for message in messages:
        tmp_dict={}
        tmp_dict["submodule"]=Find_Matched_Pattrn(message)
        tmp_dict["detection value"]=Find_Matched_Data(message)
        tmp_dict["filepath"] = filepath
        tmp_dict["detail"] = lastLogId
        #print(message)
        #print(matchedPattern,"--:--",matchedData)
        result.append(tmp_dict)
    return result

def Muze_Log(templete_json,log=None,detection_check=False):



    templete_json["Dtection"] = detection_check
    templete_json["module"] = "XSS_Detection_Server"
    templete_json["log"] = log
    del templete_json["filepath"]
    #print(templete_json)

    ## 넘겨줘야하는 딕션너리 최종로그 templete_json

    return templete_json

def Json_Save(json_log):
    #무제 로그파일이 존재할 경우
    if os.path.isfile(MUZE_LOG_FILE):
        json_file =  open(MUZE_LOG_FILE, "a", encoding="utf-8")
        # 무제 로그파일이 존재하지 않을 경우
    else:
        # xss_rule_and_string=raw_data
        # print(2)
        json_file = open(MUZE_LOG_FILE, "w", encoding="utf-8")
    json.dump(json_log, json_file, indent=4)
    json_file.close()

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
    #최신 로그 번호 찾기
    last_log_signature = LastLogFind()
    print(last_log_signature)

    #템플릿 전송
    TempleteSend(XSS_TEMPLETE)

    #최신 로그 번호 찾아서 비교후 다르면 공격 탐지
    last_log_signature = LastLogFind()

    recentLog,latest_log_id=XSSLog()
    #print(recentLog)
    #print(latest_xss_log_id)


    filepath = TEMPLETE_JSON["filepath"]
    # 탐지될 때
    if recentLog!=0:

        log=Find_Matched_Info(recentLog,filepath,latest_log_id)
        #print(log)
        #print(rule_and_string)
        result=Muze_Log(TEMPLETE_JSON,log,True)
        #print(result)


    # 미탐일 때
    else:
        pass

    #로그 저장
    Json_Save(result)


if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
