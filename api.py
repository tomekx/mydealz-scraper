from flask import Flask
from flask import request

from main import main

app = Flask(__name__)

@app.route("/run")
def run():
    main()
    return {"res": "started script"}

@app.route('/config', methods = ['POST'])
def config():
    data = request.form.to_dict(flat=False)
    print(data['Hello'][0])
    return 'heeloi'

app.run()