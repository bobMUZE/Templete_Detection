import webview
from bs4 import BeautifulSoup
import requests

'''
Function List..

1. 선택 or id 속성 값 Template화 (완료)
2. HTML Injection을 이용한 웹 데이터 제어 (완료)
3. Response 기능 추가로 반환 값을 이용한 Beautifulsoup 데이터 제어 추가 (완료)
4. href 기능 비활성화 (완료)
'''
def IdRun(target, select_target):
    req = requests.get(target)
    req.encoding = 'utf-8'
    res = req.text

    soup = BeautifulSoup(res, 'html.parser')
    try:
        text = soup.find('div', class_=select_target).attrs
        GetTemplate(text)
    except:
        GetTemplate('Selector is Not Defined...')

def TemplateRun(target):
    window = webview.create_window('Template', target, js_api=api)
    webview.start(HTMLInjection, window)
    Preprocessing(api.pyhtml)

def Preprocessing(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        text = soup.find('div').attrs
        GetTemplate(text)
    except:
        GetTemplate('Selector is Not Defined...')
    

def GetTemplate(text):
    if type(text) == str:
        print(text)
    elif text.get('id') and text.get('class'):
        print('id:', text['id'], 'class:', text['class'])
    elif text.get('id'):
        print('id:', text['id'])
    elif text.get('class'):
        print('class:', text['class'])
    else:
        print('Selector is Not Defined...')

def HTMLInjection(window):
    window.move(200, 100)
    window.resize(1500, 850)
    result = window.evaluate_js(
        r"""
        var arr = [];
        var d = document.getElementsByTagName('div');
        var div_blacklist = [undefined, null, "", "container", "NM_INT_LEFT"];
        var ptag_blacklist = [undefined, "BODY"];

        for (var i in d) {
            if (div_blacklist.indexOf(d[i].id) == -1){
                if (ptag_blacklist.indexOf(d[i].parentNode.tagName) == -1){
                    arr.push(document.getElementById(d[i].id));
                }
            }
        }

        for (var j in arr) {
            arr[j].setAttribute("onclick", "template(this)");
            arr[j].setAttribute("onmouseover", "this.style.backgroundColor=\"rgba(255, 99, 71, 0.7)\"; this.style.borderWidth=\"thick\"; this.style.borderColor=\"rgba(255, 99, 71, 0.7)\"");
            arr[j].setAttribute("onmouseout", "this.style.backgroundColor=''; this.style.borderWidth=''; this.style.borderColor=''");
        }

        function template(test) {
            var pyhtml = test.outerHTML;
            pywebview.api.GetJSValue(pyhtml, 1);
        }
        """
    )
    api.SetDestory(window)

class Api:
    def __init__(self):
        self.flag = 0
        self.pyhtml = ''

    def GetJSValue(self, pyhtml, flag):
        self.pyhtml = pyhtml
        self.flag = flag
        if self.flag == 1:
            try:
                self.window.destroy()
                exit(0)
            except:
                exit(0)
            
    def SetDestory(self, window):
        self.window = window
        
'''
0 : Run Template
1 : input id Attribute
'''
def TemplateFunction(num, target, select_target):
    if num == 1:
        IdRun(target, select_target)
    else:
        TemplateRun(target)

if __name__ == '__main__':
    # Webview Setting
    api = Api()

    # Web Site
    # 네이버, 워드프레스, 그누보드, 제로보드
    target_url = ['https://www.naver.com/', 'http://218.146.55.65/wordpress/index.php/about/', \
    'http://218.146.55.65/g5/', 'http://218.146.55.65/xe/']

    # Web Site DIV Tag Attribute (id, class)
    select_target = 'group_title'
    #select_target = 'a'

    # 0 is Run Webview Template
    # 1 is Run input id Attribute Template
    # TemplateFunction(TemplateStyle, SiteURL, IDAttribute)
    TemplateFunction(0, target_url[0], select_target)