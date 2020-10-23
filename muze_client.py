import socket
import logging
import requests

def SocketConnect():

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ServerHost,PORT))
    print(s.recv(1024))
    templete = TempleteSelect()
    #소켓통신으로 데이터 전송시 byte object로 전송해야함
    #templete_as_bytes=str.encode(templete)
    #s.send(templete_as_bytes)
    return s
    #s.close()

def TempleteSend(sock,templete):
    templete_as_bytes = str.encode(templete)
    mylogger.debug(templete_as_bytes)
    sock.send(templete_as_bytes)
    sock.close()
    return

def TempleteSelect():
    with open("templete.txt","r",encoding="utf-8") as f:
        templete=f.read()
        return templete

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
    mylogger.info(templete)
    s=SocketConnect()
    TempleteSend(s,templete)

    #modsec_file="modsec_audit.log"
    #f = open(modsec_file, "r")
    #modsec_log=ModsecLogRead(f)
    #XSSLog(modsec_log,f)
if __name__ == '__main__':
    ServerHost = "192.168.0.13"
    PORT = 12345
    # 로깅 객체 생성
    mylogger = Use_Logging(logging.INFO)
    mylogger.debug('test')
    main()
