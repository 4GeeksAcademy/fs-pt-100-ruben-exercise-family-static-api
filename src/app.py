"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# for member in initial_members:
#     jackson_family.add_member(member)

# print(jackson_family.get_all_members())
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "Family",
                     "family": members}
    return jsonify(response_body), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def one_member(member_id):
    # This is how you can use the Family datastructure by calling its methods
    member_founded = jackson_family.get_member(member_id)
    response_body = {"hello": "Member",
                     "family": member_founded}
    if not member_founded:
        return jsonify({"msg":"no se encontró al miembro"})
    return jsonify(response_body), 200


@app.route('/members', methods=['POST'])
def add_member():
    # This is how you can use the Family datastructure by calling its methods
    add_new_member = request.json
    
    jackson_family.add_member(add_new_member)
    response_body = {"hello": "New Member",
                     "family": add_new_member}
    if not add_new_member:
        return jsonify({"msg":"no se creo al miembro"})
    return jsonify(response_body), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    # This is how you can use the Family datastructure by calling its methods
    delete_one_member = jackson_family.delete_member(member_id)
    if "done" in delete_one_member:
        return jsonify({"msg":"se eliminó al miembro"}), 200
    
    return jsonify({"msg":"no se eliminó al miembro"}), 400
    # return jsonify({"msg":"se eliminó al miembro"}), 200

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    # This is how you can use the Family datastructure by calling its methods
    member_update = request.json
    member_family_update = jackson_family.update_member(member_id, member_update)
    response_body = {"hello": "Member Update",
                     "family": member_family_update}
    if not member_family_update:
        return jsonify({"msg":"no se actualizo al miembro"})
    return jsonify(response_body), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
