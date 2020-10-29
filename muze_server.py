import socket
import logging
import re

PATTERN_LIST=[
    #[1,2,3] = 클수록  위험
    "(?i)([<＜]script[^>＞]*[>＞][\s\S]*?)", #3
    "(?i)(j[\s]*a[\s]*v[\s]*a[\s]*s[\s]*c[\s]*r[\s]*i[\s]*p[\s]*t:[^>＞]*[>＞][\s\S]*?)", #2
    "(?i)(document[\s]*.[\s]*cookie)", #2
    "&#0000106|&#0000097|&#0000118|&#0000097|&#0000115|&#0000099|&#0000114|&#0000105|&#0000112|&#0000116|&#0000058|&#0000097|&#0000108|&#0000101|&#0000114|&#0000116|&#0000040|&#0000039|&#0000088|&#0000083|&#0000083|&#0000039|&#0000041",#2
    "&#106;|&#97;|&#118;|&#97;|&#115;|&#99;|&#114;|&#105;|&#112;|&#116;|&#58;|&#97;|&#108;|&#101;|&#114;|&#116;|&#40;|&#39;|&#88;|&#83;|&#83;|&#39;|&#41;",#2
    "&#x6A|&#x61|&#x76|&#x61|&#x73|&#x63|&#x72|&#x69|&#x70|&#x74|&#x3A|&#x61|&#x6C|&#x65|&#x72|&#x74|&#x28|&#x27|&#x58|&#x53|&#x53|&#x27|&#x29",#2
]

def TempleteReceive(conn):
    templete_as_bytes = conn.recv(1024)

    #TCP 전송시 byte형태로 전송됨으로 str로 convert
    templete=templete_as_bytes.decode()
    mylogger.debug(templete)
    conn.close()
    return templete

def SocketConnect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ServerHost, PORT))
    s.listen(2)
    conn, addr = s.accept()
    #mylogger.info(addr, "Now Connected")
    # 접속 알람
    mylogger.debug(str(addr)+ " Now Connected")

    # 접속 확인 메시지 전송
    conn.send(b"Thank you for connecting")
    return conn

# 정규표현식을 활용한 문자열 검색
def Search_Re(pattern_list,search_str):
    mylogger.debug(pattern_list)

    for pattern in pattern_list:
        #mylogger.info(pattern)
        p = re.compile(pattern)
        m=p.search(search_str)
        if m:
            mylogger.info(m)
            mylogger.info("find signaure : "+m.group())
            mylogger.info("find text : " + search_str[m.start()-20:m.end()+20])



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

    # 로깅 레벨
    mylogger.setLevel(level)
    stream_hander = logging.StreamHandler()
    mylogger.addHandler(stream_hander)
    mylogger.info("logging start!!!")
    return mylogger

def main():
    conn=SocketConnect()
    templete=TempleteReceive(conn)
    #pattern=Apply_Special_Char(detection_char)
    re_result=Search_Re(PATTERN_LIST,templete)

if __name__ == '__main__':
    ServerHost = "192.168.0.181"
    PORT = 12345
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
