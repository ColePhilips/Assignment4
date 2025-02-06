from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mhw_db"  # MongoDB URI
mongo = PyMongo(app)
api = Api(app)

#Swagger for api docummentation
swaggerui_blueprint = get_swaggerui_blueprint('/swagger', '/static/swagger.json', config={'app_name': "Monster Hunter API"})
app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

class Monster(Resource): #Class for handeling resource requests to monsters collection. Resource is part of Flask-RESTful that handles http requests for specific resource
    
    # Create: POST /monsters
    def post(self):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        monster_type = data.get("type")
        
        if not name or not description:
            return {"message": "Name and description are required!"}, 400
        
        # Insert monster into the database with a custom "id"
        monster = {
            "id": int(mongo.db.monsters.count_documents({}) + 3),  # Custom "id" generation
            "name": name,
            "description": description,
            "type": monster_type
        }
        result = mongo.db.monsters.insert_one(monster)
        
        return jsonify({
            "id": monster["id"],
            "name": name,
            "description": description,
            "type": monster_type
        })

    # Read: GET /monsters/<id>
    def get(self, monster_id=None):
        if monster_id:
            # Ensure monster_id is treated as an integer and query by custom "id"
            monster = mongo.db.monsters.find_one({"id": int(monster_id)})
            if not monster:
                    return{"message": "Monster not found"}, 404
            return jsonify({"id": monster["id"], "name": monster["name"], "description": monster["description"], "type": monster["type"]})
        else:
            monsters = mongo.db.monsters.find()
            result = []
            for monster in monsters:
                result.append({"id": monster["id"], "name": monster["name"], "description": monster["description"], "type": monster["type"]})
            return jsonify(result)

    # Update: Put /monsters/<id>
    def put(self, monster_id):
        data = request.get_json() #user input
        name = data.get("name")
        description = data.get("description")
        monster_type = data.get("type")

        #validation
        if not name or not description:
            return {"message": "Name and description are required fields"}, 400
        
        # Update the monster in the database using custom "id"
        result = mongo.db.monsters.update_one(
            {"id": int(monster_id)},  # Ensure monster_id is treated as an integer
            {"$set": {"name": name, "description": description, "type": monster_type}}
        )
        
        if result.matched_count == 0:
            return {"message": "Monster not found!"}, 404
        
        return jsonify({
            "id": monster_id,
            "name": name,
            "description": description,
            "type": monster_type
        })

    # Delete: DELETE /monsters/<id>
    def delete(self, monster_id):
        result = mongo.db.monsters.delete_one({"id": int(monster_id)})  # Ensure monster_id is treated as an integer
        if result.deleted_count == 0:
            return {"message": "Monster not found!"}, 404
        return {"message": "Monster deleted successfully!"}, 200

# Set up the routes for the Monster resource
api.add_resource(Monster, "/monsters", "/monsters/<int:monster_id>")  # Updated to <int:monster_id>

if __name__ == "__main__":
    app.run(debug=True)