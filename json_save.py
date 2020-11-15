import json


templete_json = {'time': '1605365247.624045', 'url': 'http://3.131.17.188/g5', 'module': 1, 'filepath': '/home/ubuntu/semicrawling/3.131.17.188/g5/0', 'xpath': '//*[@id="hd"]'}

with open("json/student_file.json", "w") as json_file:

    json.dump(templete_json, json_file,indent=4)



