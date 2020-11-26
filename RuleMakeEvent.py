import csv
#file_name="not_require.csv"
#file_name="require.csv"
file_name= "csv/total.csv"
def MakeRegex():
    "(?i)([<＜](xss|a) -)[\s\S]*?onactivate[\s\S]*?[>＞]"
    f = open(file_name, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    event_check=""
    tag_or=""


    for line in rdr:
        event=line[0]
        tag=line[1]
        #print(tag)

        if event_check=="":
            event_check = event

        if event_check!=event:
            if tag_or[0]=="|":
                tag_or=tag_or[1:]

            #regex=f"(?i)([<＜]({tag_or})[ /])[\s\S]*?({event_check})[\s\S]*?[>＞]"
            regex = f"(?i)([<＜]({tag_or})[ ,/])[\s\S]*?({event_check})[\s\S]*?[>＞]"
            #print(regex)
            #return
            event_check=event
            tag_or = tag
            yield regex
        else:
            tag_or+="|"+tag
            #print(event)
    regex = f"(?i)([<＜]({tag_or})[ ,/])[\s\S]*?({event_check})[\s\S]*?[>＞]"
    f.close()
    yield regex

def main():
    rule_id=111111111
    with open("rule/event-handle.conf", "w", encoding='utf-8') as f:
        for i in MakeRegex():
            #print(i)
            matched_data="%{TX.0}"
            matched_var_name="%{MATCHED_VAR_NAME}"
            matched_var="%{MATCHED_VAR}"
            secRule=f'''SecRule REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/|REQUEST_COOKIES_NAMES|REQUEST_HEADERS:User-Agent|REQUEST_HEADERS:Referer|ARGS_NAMES|ARGS|XML:/* "{i}" \\
"msg:'NoScript XSS InjectionChecker: HTML Injection',\\
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
