import re
import logging
PATTERN_LIST=[
    "(?i)([<＜]script[^>＞]*[>＞][\s\S]*?)",
]
# 템플릿 가져오기
def Select_Templete():
    # xss 문자열 읽기
    f=open('txt/templete.txt', 'r', encoding='utf-8')
    xss_str=f.read()
    f.close()
    return xss_str

# 개행문자 제거
def Newline_Space_Remove(template_str):
    #template_str = template_str.replace("\n", "")
    #template_str = template_str.replace("\t", "")
    #template_str = template_str.replace(" ", "")
    return template_str

# 정규표현식을 활용한 문자열 검색
def Search_Re(pattern,search_str):
    mylogger.debug(pattern)
    pattern="(?i)([<＜]script[^>＞]*[>＞][\s\S]*?)"
    #p = re.compile(pattern,re.I)
    p = re.compile(pattern)
    m=p.search(search_str)
    mylogger.info(m)



# 정규표현식 특수문자 적용
def Apply_Special_Char(detection_char):
    pattern=detection_char
    if pattern.find('.')>=0:
        pattern=pattern.replace(".", "[.]")
    if pattern.find('\\')>=0:
        pattern=pattern.replace("\\", "\\\\")
    mylogger.debug(pattern)
    return pattern

# 로깅 함수
def Use_Logging(level):
    mylogger = logging.getLogger("my")

    #로깅 레벨
    mylogger.setLevel(level)
    stream_hander = logging.StreamHandler()
    mylogger.addHandler(stream_hander)
    mylogger.info("logging start!!!")
    return mylogger


def main():
    # 정규표현식 패턴
    detection_char = 'document.cookie'
    search_string = Select_Templete()
    search_string=Newline_Space_Remove(search_string)
    pattern=Apply_Special_Char(detection_char)
    re_result=Search_Re(pattern,search_string)

if __name__ == '__main__':
    #로깅 객체 생성
    mylogger=Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
