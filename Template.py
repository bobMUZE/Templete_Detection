import webview

'''
참고 정리 코드
1. HTML Code Injection
document.getElementsByTagName("div")[1].onclick = alert('test'); // div 태그 모든 정보 호출

document.getElementById('NM_NEWSSTAND_TITLE').onclick = function(event) {  // HTML Injection 동작 테스트 완료
    alert(document.getElementById('NM_NEWSSTAND_TITLE').outerHTML); // div부터 내부요소까지 출력 = Template
}

or

var sjElements = document.querySelectorAll('div');
for (var i in sjElements) {
    sjElements[i].onclick = function(event) {
    div#NM_INT_LEFT.column_left.onclick = function(event) {
        event.preventDefault();

        var scriptSource = this.getAttribute('data-href');
        var scriptTag = document.createElement('SCRIPT');
        scriptTag.src = scriptSource;

        document.body.appendChild(scriptTag);
    };
}

2. Use Webview library
import threading
import time
import sys
import random
import webview


html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

<style>
    #response-container {
        display: none;
        padding: 3rem;
        margin: 3rem 5rem;
        font-size: 120%;
        border: 5px dashed #ccc;
    }

    label {
        margin-left: 0.3rem;
        margin-right: 0.3rem;
    }

    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
        text-transform: uppercase;
    }

</style>
</head>
<body>


<h1>JS API Example</h1>
<p id='pywebview-status'><i>pywebview</i> is not ready</p>

<button onClick="initialize()">Hello Python</button><br/>
<button id="heavy-stuff-btn" onClick="doHeavyStuff()">Perform a heavy operation</button><br/>
<button onClick="getRandomNumber()">Get a random number</button><br/>
<label for="name_input">Say hello to:</label><input id="name_input" placeholder="put a name here">
<button onClick="greet()">Greet</button><br/>
<button onClick="catchException()">Catch Exception</button><br/>


<div id="response-container"></div>
<script>
    window.addEventListener('pywebviewready', function() {
        var container = document.getElementById('pywebview-status')
        container.innerHTML = '<i>pywebview</i> is ready'
    })

    function showResponse(response) {
        var container = document.getElementById('response-container')

        container.innerText = response.message
        container.style.display = 'block'
    }

    function initialize() {
        pywebview.api.init().then(showResponse)
    }

    function doHeavyStuff() {
        var btn = document.getElementById('heavy-stuff-btn')

        pywebview.api.doHeavyStuff().then(function(response) {
            showResponse(response)
            btn.onclick = doHeavyStuff
            btn.innerText = 'Perform a heavy operation'
        })

        showResponse({message: 'Working...'})
        btn.innerText = 'Cancel the heavy operation'
        btn.onclick = cancelHeavyStuff
    }

    function cancelHeavyStuff() {
        pywebview.api.cancelHeavyStuff()
    }

    function getRandomNumber() {
        pywebview.api.getRandomNumber().then(showResponse)
    }

    function greet() {
        var name_input = document.getElementById('name_input').value;
        pywebview.api.sayHelloTo(name_input).then(showResponse)
    }

    function catchException() {
        pywebview.api.error().catch(showResponse)
    }

</script>
</body>
</html>
"""


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        print(response)
        return response

    def getRandomNumber(self):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(random.randint(0, 100000000))
        }
        print(response)
        return response

    def doHeavyStuff(self):
        time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
        now = time.time()
        self.cancel_heavy_stuff_flag = False
        for i in range(0, 1000000):
            _ = i * random.randint(0, 1000)
            if self.cancel_heavy_stuff_flag:
                response = {'message': 'Operation cancelled'}
                break
        else:
            then = time.time()
            response = {
                'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now), threading.current_thread())
            }
        print(response)
        return response

    def cancelHeavyStuff(self):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = True

    def sayHelloTo(self, name):
        response = {
            'message': 'Hello {0}!'.format(name)
        }
        print(response)
        return response

    def error(self):
        raise Exception('This is a Python exception')

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('API example', html=html, js_api=api)
    webview.start()
'''

def evaluate_js(window):
    window.move(240, 100)
    window.resize(2000, 1400)
    window.load_css('div:hover {background: #CCFF33;}')
    result = window.evaluate_js(
        r"""
        var header = document.getElementById('NM_NEWSSTAND_TITLE');
        header.onclick = function(){
            alert(header.outerHTML);
        };
        """
    )
    print(result)
    #window.destroy()

if __name__ == '__main__':
    window = webview.create_window('Template', 'https://www.naver.com/')
    webview.start(evaluate_js, window, debug=True)