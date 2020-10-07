import webview

'''
To Be..

0. href 제거
1. ClassName 구분자 추가
2. id attribute input으로 템플릿 선택 기능 추가
3. Response 기능 추가로 반환 값을 이용한 Beautifulsoup 데이터 제어 추가

'''
def IdRun(target):
    print(target)

def TemplateRun(target):
    window = webview.create_window('Template', target)
    webview.start(evaluate_js, window, debug=True)

def evaluate_js(window):
    window.move(240, 100)
    window.resize(2000, 1400)
    result = window.evaluate_js(
        r"""
        var arr = [];
        var d = document.getElementsByTagName('div');

        for (var i in d) {
            if (d[i].id != "" && d[i].id != null && d[i].id != "container" && d[i].id != "NM_INT_LEFT" && d[i].parentNode.tagName != "BODY"){
                arr.push(document.getElementById(d[i].id));
            }
            //if (d[i].id == "" && d[i].parentNode.tagName != "BODY"){
            //    arr.push(document.getElementsByClassName(d[i].className));
            //}
        }

        for (var j in arr) {
            arr[j].setAttribute("onclick", "template(this)");
            arr[j].setAttribute("onmouseover", "this.style.backgroundColor=\"rgba(255, 99, 71, 0.7)\"; this.style.borderWidth=\"thick\"; this.style.borderColor=\"rgba(255, 99, 71, 0.7)\"");
            arr[j].setAttribute("onmouseout", "this.style.backgroundColor=''; this.style.borderWidth=''; this.style.borderColor=''");
        }

        function template(test) {
            console.log(test.outerHTML);
        }
        """
    )
    #window.destroy()

'''
0 : Run Template
1 : input id Attribute
'''
def start(num, target):
    if num == 1:
        IdRun(target)
    else:
        TemplateRun(target)

if __name__ == '__main__':
    # 네이버, 워드프레스, 그누보드, 제로보드
    target_url = [ 'https://www.naver.com/', 'http://218.146.55.65/wordpress/index.php/about/', \
    'http://218.146.55.65/g5/', 'http://218.146.55.65/xe/' ]
    start(0, target_url[0]);