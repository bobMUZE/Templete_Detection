import re

f= open("modsec_audit.log","r")
modsec_log = f.read()
#print(modsec_log)

#정규식
#p = re.compile('\--\w{8}\-H\--')
# modsecurity 탐지 파싱 부분 정규식
p = re.compile('[-]{2}\w{8}[-]{1}H[-]{2}')

# mod
m = p.search(modsec_log)

if m:
    print("--------------------XSS Attack Detection------------------------")
    #print(m)
    #print(m.group())
    #print(m.start())
    #print(m.end())
    #print(m.span())
    f.seek(m.end())
    detect_log=f.read()
    print(detect_log)
