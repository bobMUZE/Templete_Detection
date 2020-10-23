import socket
import logging
import re


def TempleteReceive(conn):
    templete_as_bytes = conn.recv(1024)

    #TCP 전송시 byte형태로 전송됨으로 str로 convert
    templete=templete_as_bytes.decode()
    print(templete)
    conn.close()
    return templete

def SocketConnect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ServerHost, PORT))
    s.listen(2)
    conn, addr = s.accept()
    #mylogger.info(addr, "Now Connected")
    # 접속 알람
    print(addr, "Now Connected")

    # 접속 확인 메시지 전송
    conn.send(b"Thank you for connecting")
    return conn

# 정규표현식을 활용한 문자열 검색
def Search_Re(pattern,search_str):
    mylogger.debug(pattern)
    p = re.compile(pattern,re.I)
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

    # 로깅 레벨
    mylogger.setLevel(level)
    stream_hander = logging.StreamHandler()
    mylogger.addHandler(stream_hander)
    mylogger.info("logging start!!!")
    return mylogger

def main():
    detection_char = 'document.cookie'
    conn=SocketConnect()
    templete=TempleteReceive(conn)
    pattern=Apply_Special_Char(detection_char)
    re_result=Search_Re(pattern,templete)

if __name__ == '__main__':
    ServerHost = "192.168.0.13"
    PORT = 12345
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
