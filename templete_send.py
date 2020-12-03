import requests
import logging
import re

#DETECT_URL="http://210.117.90.186/"
MY_DETECT_URL="http://192.168.0.5"
TEMPLETE="""
<article itemprop=\"articleBody\">\n<h1 content=\"\ube0c\ub77c\ubcf4 \ucee4\ubba4\ub2c8\ud2f0 \ub9e4\uc77c \ub098\ub214 \uc774\ubca4\ud2b8 12\uc6d4 \uce98\ub9b0\ub354 \uc548\ub0b4\" itemprop=\"headline\">\n<span class=\"talker-photo hidden-xs\"><img alt=\"\ube0c\ub77c\ubcf4\ud14d\" src=\"https://bravotec.co.kr/data/apms/photo/br/bravotec.jpg\"/></span>\t\t\t\ube0c\ub77c\ubcf4 \ucee4\ubba4\ub2c8\ud2f0 \ub9e4\uc77c \ub098\ub214 \uc774\ubca4\ud2b8 12\uc6d4 \uce98\ub9b0\ub354 \uc548\ub0b4\t\t</h1>\n<div class=\"panel panel-default view-head no-attach\">\n<div class=\"panel-heading\">\n<div class=\"ellipsis text-muted font-12\">\n<span content=\"\ube0c\ub77c\ubcf4\ud14d\" itemprop=\"publisher\">\n<span class=\"sv_member\">\ube0c\ub77c\ubcf4\ud14d</span> </span>\n<span class=\"hidden-xs\">\n<span class=\"sp\"></span>\n<i class=\"fa fa-tag\"></i>\r\n\t\t\t\t\t\t\t\uc774\ubca4\ud2b8\t\t\t\t\t\t</span>\n<span class=\"sp\"></span>\n<i class=\"fa fa-comment\"></i>\r\n\t\t\t\t\t0\t\t\t\t\t<span class=\"sp\"></span>\n<i class=\"fa fa-eye\"></i>\r\n\t\t\t\t\t34\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<span class=\"pull-right\">\n<i class=\"fa fa-clock-o\"></i>\n<span content=\"2020-12-01KST10:40:21\" itemprop=\"datePublished\">\r\n\t\t\t\t\t\t\t12.01 10:40\t\t\t\t\t\t</span>\n</span>\n</div>\n</div>\n</div>\n<div class=\"view-padding\">\n<div class=\"view-img\">\n</div>\n<div class=\"view-content\" itemprop=\"description\">\n<p align=\"center\" style=\"text-align:center;\"><a class=\"view_image\" href=\"https://bravotec.co.kr/bbs/view_image.php?fn=%2Fdata%2Feditor%2F2012%2Fa39b6a3adb64a858d7ef662a6136bcac_1606786798_6818.jpg\" target=\"_blank\"><img alt=\"a39b6a3adb64a858d7ef662a6136bcac_1606786798_6818.jpg\" class=\"img-tag\" content=\"https://bravotec.co.kr/data/editor/2012/a39b6a3adb64a858d7ef662a6136bcac_1606786798_6818.jpg\" itemprop=\"image\" src=\"https://bravotec.co.kr/data/editor/2012/a39b6a3adb64a858d7ef662a6136bcac_1606786798_6818.jpg\"/></a></p><p style=\"text-align:center;\"><br/></p><p><br/></p><p align=\"center\" style=\"text-align:center;\">\ube0c\ub77c\ubcf4 \ucee4\ubba4\ub2c8\ud2f0 \ub9e4\uc77c \ub098\ub214 \uc774\ubca4\ud2b8 12\uc6d4 \uce98\ub9b0\ub354\uac00 \ub4f1\ub85d\ub418\uc5c8\uc2b5\ub2c8\ub2e4. \ub9e4\uc77c\ub9e4\uc77c \uc990\uac70\uc6c0\uc774 \uac00\ub4dd\ud55c \ube0c\ub77c\ubcf4 \ucee4\ubba4\ub2c8\ud2f0\ub97c \uc9c0\uae08 \ud655\uc778\ud574\ubcf4\uc138\uc694!</p><p><br/></p><p align=\"center\" style=\"text-align:center;\"><b>\ube0c\ub77c\ubcf4 \ucee4\ubba4\ub2c8\ud2f0 \ubc14\ub85c\uac00\uae30 - <a href=\"https://cafe.naver.com/bravotec\" rel=\"nofollow\">https://cafe.naver.com/bravotec</a></b></p><div><br/></div><p><br/></p> </div>\n</div>\n<div class=\"h40\"></div>\n<div class=\"print-hide view-icon view-padding\">\n<span class=\"pull-right\">\n<img alt=\"\ud504\ub9b0\ud2b8\" class=\"cursor at-tip\" data-original-title=\"\ud504\ub9b0\ud2b8\" data-toggle=\"tooltip\" onclick=\"apms_print();\" src=\"https://bravotec.co.kr/img/sns/print.png\"/>\n</span>\n<div class=\"clearfix\"></div>\n</div>\n<div class=\"view-author-none\"></div>\n</article>
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
    response = requests.get(MY_DETECT_URL,params=params)
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
