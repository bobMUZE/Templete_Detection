import requests
import logging
import re

#DETECT_URL="http://210.117.90.186/"
MY_DETECT_URL="http://192.168.0.5"
TEMPLETE="""
<div id="test">

<p><object align="left" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0" height="123" hspace="12" vspace="123" width="123"><param name="allowFullScreen" value="true"><param name="quality" value="high"><param name="wmode" value="window"><param name="allowScriptAccess" value="always"><param name="scale" value="showall"><param name="movie" value="/media/uploads/2020/12/06/psnliq.jpg"><embed allowfullscreen="true" allowscriptaccess="always" height="123" hspace="12" pluginspage="http://www.macromedia.com/go/getflashplayer" quality="high" scale="showall" src="/media/uploads/2020/12/06/psnliq.jpg" type="application/x-shockwave-flash" vspace="123" width="123" wmode="window"></object></p>

</div>
"""

def ModsecLogRead(f):
    modsec_log = f.read()
    return modsec_log
    #print(modsec_log)

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
    with open("txt/templete.txt", "r", encoding="utf-8") as f:
        templete=f.read()
        return TEMPLETE

##
def TempleteSend(templete):
    #templete="test"
    mylogger.info("Send Templete!!!")
    params={"templete":templete}
    print(templete)
    #url=DETECT_URL+templete
    response = requests.post(MY_DETECT_URL,data=params)
    #response = requests.get(DETECT_URL, params=params)
    #print(response.text)
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

    #modsec_file="modsec_audit.log"
    #f = open(modsec_file, "r")
    #modsec_log=ModsecLogRead(f)
    #XSSLog(modsec_log,f)
if __name__ == '__main__':
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
