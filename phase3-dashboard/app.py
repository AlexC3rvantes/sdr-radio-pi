from flask import Flask, jsonify, render_template_string
import json
import os

app = Flask(__name__)

AIRCRAFT_JSON = '/tmp/dump1090/aircraft.json'

@app.route('/')
def index():
    return render_template_string(open('templates/index.html').read())

@app.route('/api/aircraft')
def aircraft():
    try:
        with open(AIRCRAFT_JSON) as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e), 'aircraft': []})

@app.route('/api/stats')
def stats():
    try:
        with open(AIRCRAFT_JSON) as f:
            data = json.load(f)
        aircraft = data.get('aircraft', [])
        with_pos = [a for a in aircraft if 'lat' in a and 'lon' in a]
        return jsonify({
            'total': len(aircraft),
            'with_position': len(with_pos),
            'messages': data.get('messages', 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
