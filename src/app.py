import os
from flask import Flask, jsonify, request

app = Flask(__name__)
app.url_map.strict_slashes = False

todos = []

@app.route('/')
def sitemap():
    return jsonify({"endpoints": [rule.rule for rule in app.url_map.iter_rules()]})

@app.route('/todos', methods=['GET', 'POST'])
def handle_todos():
    if request.method == 'GET':
        return jsonify(todos), 200
    elif request.method == 'POST':
        data = request.get_json()
        todos.append(data)
        return jsonify(data), 201

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
