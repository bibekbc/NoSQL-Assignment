from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost", 
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info() # trigger exception if cannot connect to db

except:
    print("ERROR - Cannot connect to db")

#################
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        # print(data)
        return Response(
            response=json.dumps(data),
            # response=json.dumps([{"id": 1}, {"id": 2}]),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot read users"}),
            status=500,
            mimetype="application/json"
        )


#################
# @app.route('/')
@app.route('/users', methods=["POST"])
def create_user():
    try:
        # user = {"name": "A", "lastName": "AAA"}
        user = {
            "name": request.form["name"], 
            "lastName": request.form["lastName"]
            # "jobTitle": request.form["jobTitle"]
            # "skills":request.form["skills"]
        }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response=json.dumps(
                {"message": "user_created", 
                "id": f"{dbResponse.inserted_id}"
                }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("***************")
        print(ex)
        print("***************")
    # return "Hello World!"

####################
@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},            
            {"$set":{"name": request.form["name"]}}
            # upsert=True                    
        )
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}****")
        if dbResponse.modified_count >= 1 and dbResponse.modified_count <= 2: 
            return Response(
                response=json.dumps({"message": "user updated"}),
                status=200,
                mimetype="application/json"
            )        
        return Response(
            response=json.dumps({"message": "nothing to update"}),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print("***************")
        print(ex)
        print("***************")
        return Response(
            response=json.dumps({"message": "sorry cannot update user"}),
            status=500,
            mimetype="application/json"
        )
    # return id

#####################
# @app.route("/users/<id>", methods=["PATCH"])
@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1: 
            return Response(
                response=json.dumps({"message": "user deleted", "id": f"{id}"}),
                status=200,
                mimetype="application/json"
            )        
        return Response(
            response=json.dumps({"message": "user not found", "id": f"{id}"}),
            status=200,
            mimetype="application/json"
        ) 
    except Exception as ex:
        print("**********")
        print(ex)
        print("**********")
        return Response(
            response=json.dumps({"message": "sorry cannot delete user"}),
            status=500,
            mimetype="application/json"
        )

#####################
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug = True)
