
#file_name="not_require.csv"
#file_name="require.csv"
file_name= "txt/scriptTag.txt"
def MakeRegex():
    "(?i)([<＜](xss|a) -)[\s\S]*?onactivate[\s\S]*?[>＞]"
    f = open(file_name, 'r', encoding='utf-8')
    regexs=f.readlines()
    print(regexs)

    for regex in regexs:
        yield regex.strip()



def main():
    rule_id=200000000
    with open("rule/script-tag.conf", "w", encoding='utf-8') as f:
        for i in MakeRegex():
            #print(i)
            matched_data="%{TX.0}"
            matched_var_name="%{MATCHED_VAR_NAME}"
            matched_var="%{MATCHED_VAR}"
            secRule=f'''SecRule REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/|REQUEST_COOKIES_NAMES|REQUEST_HEADERS:User-Agent|REQUEST_HEADERS:Referer|ARGS_NAMES|ARGS|XML:/* "{i}" \\
"msg:'XSS InjectionChecker: Script Tag Injection',\\
id:{rule_id},\\
severity:'CRITICAL',\\
capture,\\
phase:request,\\
t:none,t:utf8toUnicode,t:urlDecodeUni,t:htmlEntityDecode,t:jsDecode,t:cssDecode,t:removeNulls,\\
tag:'attack-xss',\\
logdata:'Matched Data: {matched_data} found within {matched_var_name}: {matched_var}'
'''
            print(secRule)
            f.write(secRule)
            f.write("\n")
            rule_id+=1


if __name__ == '__main__':
    main()
