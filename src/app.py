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
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({"error": "No JSON body was provided"}), 400
        elif 'done' not in body or 'label' not in body:
            return jsonify({"error": "The JSON body is missing a required field"}), 400
        todos.append(body)
        return jsonify(todos), 201
    
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todo_id < 0 or todo_id >= len(todos):
        return jsonify({"error": "The todo does not exist"}), 404
    del todos[todo_id]
    return jsonify(todos), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
