from flask import Flask, render_template, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/monitoring')
def home():
    with open('apis.json') as f:
        data = json.load(f)
    api_statuses = []
    for api in data['apis']:
        status, time, code = check_api_status(api['uri'])
        api_statuses.append({'name': api['name'], 'status': status, 'time': time, 'code': code})
    return render_template('index.html', api_statuses=api_statuses)

@app.route('/api-status')
def api_status():
    with open('apis.json') as f:
        data = json.load(f)
    api_statuses = []
    for api in data['apis']:
        status, time, code = check_api_status(api['uri'])
        api_statuses.append({'name': api['name'], 'status': status, 'time': time, 'code': code})
    return jsonify(api_statuses)

def check_api_status(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return 'API is working', response.elapsed.total_seconds(), 10
        elif response.status_code == 502:
            return 'API is not working', response.elapsed.total_seconds(), 20
        else:
            return 'API is working', response.elapsed.total_seconds(), 10
    except:
        return 'API is not working', 'N/A', 20


if __name__ == '__main__':
    app.run(debug=True)
