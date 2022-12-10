from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)
import os
server = os.environ['boilerip']

@app.route("/")
def hello():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page()
        page.goto('http://' + server + '/logo_td_01.shtm')
        page.fill('input#input_password', 'heatmaster')
        page.click('button[id=button_login]')
        while 1 == 1:
            page.is_visible('id=param_0')
            page.is_visible('id=param_1')
#            page.is_visible('id=param_2')
#            page.is_visible('id=param_3')
            message = page.inner_text('.msg_tline>>nth=0')
            furnace = page.inner_text('.msg_tline>>nth=1')
            param_0 = page.inner_text('id=param_0')
            param_1 = page.inner_text('id=param_1')
            param_2 = page.inner_text('id=param_2')
            param_3 = page.inner_text('id=param_3')

            print('message:', message)
            print('status:', furnace)
            print('temp:', param_0)
            print('O2:', param_1)
            print('Top Air:', param_2)
            print('Bot Air:', param_3)

            if furnace.find('TIMER') < 0:
                my_dict = {
                    'Heatmaster': {
                        'status': furnace.strip(),
                        'temp': float(param_0),
                        'O2': float(param_1),
                        'Top_Air': float(param_2),
                        'Bottom_Air': float(param_3)
                    }
                }
                return (jsonify(my_dict))

            page.reload()

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000)
