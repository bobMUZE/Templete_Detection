import webview

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