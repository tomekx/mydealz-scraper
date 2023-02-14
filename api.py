from flask import Flask
from flask import request

from main import main

app = Flask(__name__)

@app.route('/config', methods = ['POST'])
def config():
    data = request.json
    config = dict(pages = data['pages'], subpage = data['subpage'], voucher = data['voucher'], min_price = data['min_price'], max_price = data['max_price'], keywords = data['keywords'], blacklist = data['blacklist'])

    main(config)

    return 'heedloi'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)