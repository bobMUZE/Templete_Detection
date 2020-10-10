import hashlib
import logging
import urllib
import urllib.parse
import requests
import json
import time

#바이러스 토탈 API 키
VT_API_KEY="d10a8c46db26f4e642caaa3b248efaf57c99da1022c0c748480bf16ebd680d24"
REPORT_URL = 'https://www.virustotal.com/vtapi/v2/file/report'

# 파일 해쉬 갑 리턴 함수
def File_Hash(path):
    f = open(path, 'rb')
    data = f.read()
    f.close()
    return(hashlib.md5(data).hexdigest(),hashlib.sha1(data).hexdigest(),hashlib.sha256(data).hexdigest())

# 로깅 함수
def Use_Logging(level):
    mylogger = logging.getLogger("my")

    #로깅 레벨
    mylogger.setLevel(level)
    stream_hander = logging.StreamHandler()
    mylogger.addHandler(stream_hander)
    mylogger.info("logging start!!!")
    return mylogger

def Virus_Total_Search(md5,sha1,sha256):
    mylogger.debug("VTS")
    #md5="2d75cc1bf8e57872781f9cd04a529256"
    parameters = {'resource': md5, 'apikey': VT_API_KEY}
    #data = urllib.parse.urlencode(parameters)
    res = requests.get(REPORT_URL, params=parameters)
    result=res.json()
    mylogger.debug(result['scans'].items())
    for key,value in result['scans'].items():
        print(key)
    #print(json.dumps(result, indent="\t"))


def main():
    file_path="C:\\tool\\chromecacheview_1.77\\ChromeCacheView.exe"
    file_md5, file_sha1 ,file_sha_256 = File_Hash(file_path)
    mylogger.debug("MD5: " + file_md5)
    mylogger.debug("SHA-1: " + file_sha1)
    mylogger.debug("SHA-256: " + file_sha_256)

    Virus_Total_Search(file_md5,file_sha1,file_sha_256)

if __name__ == '__main__':
    #로깅 객체 생성
    mylogger=Use_Logging(logging.DEBUG)
    mylogger.debug('test')

    #메인 함수
    main()
