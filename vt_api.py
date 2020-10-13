import hashlib
import logging
import csv
import requests


#바이러스 토탈 API 키
VT_API_KEY="d10a8c46db26f4e642caaa3b248efaf57c99da1022c0c748480bf16ebd680d24"
REPORT_URL = 'https://www.virustotal.com/vtapi/v2/file/report'

# 파일 해쉬 갑 리턴 함수
def File_Hash(path):
    f = open(path, 'rb')
    data = f.read()
    f.close()
    return(hashlib.md5(data).hexdigest(),hashlib.sha1(data).hexdigest(),hashlib.sha256(data).hexdigest())



# 검사되지않은 바이러스 파일인 경우 해시값으로 바이러스 토탈 결과 확인 불가능
def Virus_Total_Search(file_path):
    csv_check=False
    detection_check=False

    file_md5, file_sha1, file_sha_256 = File_Hash(file_path)
    #mylogger.debug("VTS")
    #md5="2d75cc1bf8e57872781f9cd04a529256"
    parameters = {'resource': file_md5, 'apikey': VT_API_KEY}
    #data = urllib.parse.urlencode(parameters)
    res = requests.get(REPORT_URL, params=parameters)
    result=res.json()
    #print(result)
    #mylogger.debug(result['scans'].items())
    print (file_path)
    for key,value in result['scans'].items():
        if value['detected']==True:
            if csv_check==False:
                #WriteCSV()

                #mylogger.info(key,value)
                WriteCSVFirstLine(file_path,file_md5,file_sha1,file_sha_256,key,value["version"],value["result"],value["update"])
                csv_check=True
                detection_check=True
            else:
                WriteCSV(key,value["version"],value["result"],value["update"])
            print(key, value)
    if detection_check==False:
        NothingDetect(file_path,file_md5,file_sha1,file_sha_256)
        print("Nothing detect")



            #print(key,value)
    #print(json.dumps(result, indent="\t"))

def WriteCSVheader():
    f = open('output.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["FilePath","MD5","SHA1","SHA256","Detected","Vaccine","Version","result","update"])
    f.close()

def NothingDetect(filepath,file_md5,file_sha1,file_sha_256):
    f = open('output.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow([filepath,file_md5,file_sha1,file_sha_256,"Nothing detect"])
    f.close()



def WriteCSV(company,version,result,update):
    f = open('output.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(["","","","","True",company,version,result,update])
    f.close()

def WriteCSVFirstLine(filepath,file_md5,file_sha1,file_sha_256,company,version,result,update):
    f = open('output.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow([filepath,file_md5,file_sha1,file_sha_256,"True",company,version,result,update])
    #wr.writerow([2, "박상미", True])
    f.close()
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
    file_path1 = "C:\\recent_programing\\MUZE\\mal-test"
    file_path2 = "C:\\tool\\chromecacheview_1.77\\ChromeCacheView.exe"
    WriteCSVheader()
    Virus_Total_Search(file_path1)
    Virus_Total_Search(file_path2)

if __name__ == '__main__':
    #로깅 객체 생성
    mylogger=Use_Logging(logging.DEBUG)
    mylogger.debug('test')

    #메인 함수
    main()
