import os
def FindXSS(rules_name):

    #rules="community.rules"
    f=open(rules_name,"r")
    lines=f.readlines()
    #print(lines)
    for i in lines:
        #print(i)
        #break
        if i.lower().find("xss")>=0:
            print(i)
#print(1)

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.rules':
                    FindXSS(full_filename)
    except PermissionError:
        pass

search("C:\programing\Python\MUZE")
