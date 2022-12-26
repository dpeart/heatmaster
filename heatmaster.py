import os, logging
import time
import threading
from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)
server = os.environ['boilerip']

my_lock = threading.Lock()
my_dict = {
    'Heatmaster': {
        'status': "",
        'temp': 0,
        'O2': 0,
        'Top_Air': 0,
        'Bottom_Air': 0
    }
}

def my_own_wait_for_selector(page, selector, time_out):
    try:
        page.wait_for_selector(selector, timeout=time_out)
        return True
    except:
        return False

def getData():
    global my_dict, my_lock
    while True:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=50)
            page = browser.new_page()
            page.goto('http://' + server + '/logo_td_01.shtm')
            page.fill('input#input_password', 'heatmaster')
            page.click('button[id=button_login]')
            x = 0
            # with a 5 second delay, restart browser after 1 hour for stability
            while x <= 720:
                x = x + 1
                page.is_visible('.msg_tline>>nth=1')
                message = page.inner_text('.msg_tline>>nth=0')
                furnace = page.inner_text('.msg_tline>>nth=1')

                # Only look for additional params if not in TIMER mode
                if furnace.find('TIMER') < 0:
                    param_0 = page.inner_text('id=param_0')
                    # if param=1 isn't loaded in 1 second, do a page reload and try again
                    while not my_own_wait_for_selector(page, 'id=param_1', 1000):
                        page.reload()
                    param_1 = page.inner_text('id=param_1')
                    param_2 = page.inner_text('id=param_2')
                    param_3 = page.inner_text('id=param_3')

                    # print('message:', message)
                    # print('status:', furnace)
                    # print('temp:', param_0)
                    # print('O2:', param_1)
                    # print('Top Air:', param_2)
                    # print('Bot Air:', param_3)

                    try:
                            # Acquire a lock before modifying the object state
                            # print('my_dict acquire lock')
                            my_lock.acquire()

                            my_dict = {
                                'Heatmaster': {
                                    'status': furnace.strip(),
                                    'temp': float(param_0),
                                    'O2': float(param_1),
                                    'Top_Air': float(param_2),
                                    'Bottom_Air': float(param_3)
                                }
                            }

                    finally:
                        # Release the lock in any case
                        my_lock.release()

                time.sleep(5)
                page.reload()

@app.route("/")

def returnData():
    global my_dict, my_lock, x
    
    if x.is_alive():
        try:
            # print('returnData acquire lock')
            my_lock.acquire()
            local_dict = jsonify(my_dict)
            return (local_dict)
        
        finally:
            # print('returnData released lock')
            my_lock.release()    
    else:
        x = threading.Thread(target=getData, daemon=True)
        x.start()
     
if __name__ == '__main__':
    x = threading.Thread(target=getData, daemon=True)
    x.start()
    # Delay for 5 seconds to get the first data before serving it
    time.sleep(5)
    app.run(host="0.0.0.0", port=5000)