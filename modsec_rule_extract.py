import os

def FindXSS(rules_name):
    #rules="community.rules"
    f=open(rules_name,"r",encoding="utf-8")
    lines=f.readlines()
    f.close()
    #print(lines)
    for rule in lines:
        #print(i)
        #break
        if rule.lower().find(find_word)>=0:
            #rule=rule[rule.find("alert"):]
            #rule=rule.strip()
            print(rule)
            RuleWrite(rule)

#print(1)

def Search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                Search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                #print(full_filename)
                if ext == rule_ext:
                    print(full_filename)
                    FindXSS(full_filename)
    except PermissionError:
        pass

def RuleWrite(rule):
    with open(output_file,"a") as f:
        f.writelines(rule)

rule_path="C:\\Users\\Administrator\\Documents\\GitHub\\Templete_Detection\\modsec_xss"
rule_ext=".conf"
find_word="secrule"
output_file="C:\\Users\\Administrator\\Documents\\GitHub\\Templete_Detection\\modsec_xss\\modsec_xss.rules"

Search(rule_path)
