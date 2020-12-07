import re
myStr = "Active App: Hot Baked Bread (priority 34)"
regex = re.compile("Active App: ([^\(]*)(\([^)]*\))")
match = regex.search(myStr)
print(match.group(3))
#print(appStr.group(1))
#print(appStr.group(1).rstrip())
