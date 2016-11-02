# -*- coding: utf-8 -*-

# pip install bottle
# http://46.28.110.124:8111/

import os
from bottle import route, run, template
from datetime import datetime


@route('/<temp_dht:float>/<temp:float>/<humidity_dht:float>/')
def index(temp_dht, temp, humidity_dht):
    time = datetime.now().isoformat()
    with open('temps.csv', 'a') as f:
        f.write(template('{{time}},{{t1}},{{t2}},{{h}}\n', time=time, t1=temp_dht, t2=temp, h=humidity_dht))
    return 'ok'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8111))
    run(host='0.0.0.0', port=port, debug=True)
