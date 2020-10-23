import os
def FindXSS(rules_name):

    #rules="community.rules"
    f=open(rules_name,"r")
    lines=f.readlines()
    f.close()
    #print(lines)
    for rule in lines:
        #print(i)
        #break
        if rule.lower().find("xss")>=0:
            rule=rule[rule.find("alert"):]
            #rule=rule.strip()
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
                if ext == '.rules':
                    FindXSS(full_filename)
    except PermissionError:
        pass

def RuleWrite(rule):
    with open("snort_xss.rules","a") as f:
        f.writelines(rule)
rule_path="C:/recent_programing/MUZE/snort-rules-master/snortrules-snapshot-3000"
Search(rule_path)
