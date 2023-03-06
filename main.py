from flask import Flask, jsonify
from flask import request

# import starting function
from setup import start

app = Flask(__name__)

# check for uptime
@app.route('/')
def index():
    return jsonify({"Status": "running"})

# route to start the scraper
@app.route('/config', methods = ['POST'])
def config():
    data = request.json
    config = dict(pages = data['pages'], subpage = data['subpage'], voucher = data['voucher'], min_price = data['min_price'], max_price = data['max_price'], keywords = data['keywords'], blacklist = data['blacklist'])

    start(config)

    return 'started'

# run the api
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)