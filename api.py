from flask import Flask, jsonify, request

app = Flask(__name__)

monsters = []

@app.route('/api/monsters', methods=['GET'])
def get_monsters():
    return jsonify(monsters)

@app.route('/api/monsters', methods=['POST'])
def add_monster():
    monster = request.json
    monsters.append(monster)
    return jsonify(monster), 201

@app.route('/api/monsters/<int:monster_id>', methods=['DELETE'])
def delete_monster(monster_id):
    global monsters
    monsters = [m for m in monsters if m['id'] != monster_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)