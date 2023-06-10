# web server for hosting data viewing interface

from flask import Flask, render_template, request # import required libraries
from configs import getipkeys

ipkeys = getipkeys()
app = Flask(__name__)
bufferlen = 10

keys = list(ipkeys.keys())
values = list(ipkeys.values())

# read camera configs
kvlist = [[keys[i], values[i]]for i in range(len(keys))]

reccache = {}
   
@app.route('/', methods = ['GET']) # method for handling request
def index():
    if request.method == 'GET':
        return render_template('index.html', kvlist=kvlist)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)