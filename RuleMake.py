import csv
#file_name="not_require.csv"
file_name="require.csv"
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
            regex=f"(?i)([<＜]({tag_or}) )[\s\S]*?({event_check})[\s\S]*?[>＞]"
            print(regex)
            event_check=event
            tag_or = tag
        else:
            tag_or+="|"+tag
            #print(event)
    regex = f"(?i)([<＜]({tag_or}) )[\s\S]*?({event_check})[\s\S]*?[>＞]"
    print(regex)
        #break

        #regex=f"(?i)([<＜]({tag}) )[\s\S]*?{event}[\s\S]*?[>＞]"
        #print(regex)

    f.close()

def main():
    MakeRegex()

if __name__ == '__main__':
    main()