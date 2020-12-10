import re
import logging
import os
import json
import requests
import pymongo

MY_DETECT_URL="http://192.168.0.5"

TEMPLETE_JSON = {'timestamp': 1605365247.624045,
                 'URL': 'http://3.131.17.188/g5', 'module': 1,
                 'filepath': '/home/ubuntu/semicrawling/3.131.17.188/g5/0',
                 'xpath': '//*[@id="hd"]',
                 'request_time':0.624045,
                 'status_code':200
                 }
XSS_TEMPLETE="""
<span>DSD 파일을 갖고 계신 분들은 <em>DSF</em>, DFF 확장자 명이 2개인 것을 알고 계실 겁니다. 그런데 왜 두 종류의 파일로 되어 있는지를 알 수가 없겠다구요?</span>
"""

MODSEC_LOG_FILE="modsec_audit.log"
#MODSEC_LOG_FILE="/var/log/apache2/modsec_audit.log"
MUZE_LOG_FILE="muze_log.json"



def LastLogFind():

    with open(MODSEC_LOG_FILE,"r",encoding="utf-8") as f:
        modsec_log=f.read()

    p = re.compile('[-]{2}\w{8}[-]{1}H[-]{2}')
    m=p.findall(modsec_log)
    #offset=modsec_log.find(m[-1])
    #print(type(m[-1]))
    if m:
        offset = modsec_log.find(m[-1])
        return m[-1],offset
    else:
        return 0,None

def ModsecLogRead():
    with open(MODSEC_LOG_FILE,"r",encoding="utf-8") as f:
        modsec_log=f.read()

    return modsec_log
    #print(modsec_log)


def TempleteSend(templete):
    #templete="test"
    #mylogger.info("Send Templete!!!")
    params={"templete":templete}
    print(templete)
    #url=DETECT_URL+templete
    response = requests.post(MY_DETECT_URL,data=params)
    #response = requests.get(DETECT_URL, params=params)
    #print(response.text)
    return

def XSSLog(log_offset):
    #정규식
    #p = re.compile('\--\w{8}\-H\--')
    # modsecurity 탐지 파싱 부분 정규식
    modsec_log=ModsecLogRead()
    recent_log = modsec_log[log_offset:]
    return recent_log


def Find_Message_Column(recentLog):
    messageColumnRe = "Message: Warning. Pattern match [\s\S]*?[\\n]"
    p = re.compile(messageColumnRe)
    messages = p.findall(recentLog)
    return messages

def Find_Matched_RuleID(message):
    matchedPatternRe="\\[id \"([\S]*?)\"\\]"
    p = re.compile(matchedPatternRe)
    matchedPattern = p.search(message)
    return matchedPattern.group(1)

def Find_Matched_Data(message):
    matchedDataRe="\\[data \"Matched Data: ([\s\S]*?)found within ARGS:"
    #print(matchedDataRe)
    p = re.compile(matchedDataRe)
    matchedData = p.search(message)
    #print("##")
    #print(matchedData.group(1))
    try:
        return matchedData.group(1)
    except:
        print(message)
    #print("##")
    #return matchedData[0][21:-19]

def Find_Matched_Info(recentLog,filepath,lastLogId):
    messages=Find_Message_Column(recentLog)
    result=[]
    for message in messages:
        tmp_dict={}
        tmp_dict["submodule"]=Find_Matched_RuleID(message)
        tmp_dict["detection value"]=Find_Matched_Data(message)
        tmp_dict["filepath"] = filepath
        tmp_dict["detail"] = lastLogId
        #print(message)
        #print(matchedPattern,"--:--",matchedData)
        result.append(tmp_dict)
    return result

def Muze_Log(templete_json,log=None,detection_check=False):

    templete_json["detection"] = detection_check
    templete_json["module"] = "XSS_Detection_Server"
    templete_json["logdata"] = log

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

def main(html,msg_json):
    #최신 로그 번호 찾기
    last_log_id,last_log_offset = LastLogFind()
    #print(last_log_signature)

    #템플릿 전송
    TempleteSend(html)

    #최신 로그 번호 찾아서 비교후 다르면 공격 탐지
    recent_log_id,recent_log_offset = LastLogFind()
    #print(last_log_id,recent_log_id)
    filepath = msg_json["filepath"]
    del msg_json["filepath"]
    # 탐지될 경우
    #if (1):
    if(last_log_id!=recent_log_id):
        print("attack")
        recentLog=XSSLog(recent_log_offset)
        #print(recentLog)
        log=Find_Matched_Info(recentLog,filepath,recent_log_id)
        #print(log)
        #print(rule_and_string)
        result=Muze_Log(msg_json,log,True)


    # 미탐일 경우
    else:
        log = [{"submodule": None, "detection value": None, "filepath": filepath, "detail": None}]
        result = Muze_Log(msg_json, log, False)

    print(result)
    Json_Save(result)
    return result

        #로그 저장



if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main(XSS_TEMPLETE,TEMPLETE_JSON)
