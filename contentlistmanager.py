from flask import Flask, render_template
import os
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

def get_room_names():
    rooms = []
    for room in mongo.db.collection_names():
        if not room.startswith("system."):
            rooms.append(room)
    return rooms


@app.route("/")
def show_contents_list():
    rooms = get_room_names()
    
    items_by_room = {}
    for room in rooms:
        items_by_room[room]  = mongo.db[room].find()
    
    return render_template("contents_list.html", items_by_room=items_by_room)
    

@app.route("/room/<room>")
def show_room_detail(room):
    
    items = mongo.db[room].find()
    
    return render_template("room_detail.html", items=items, room=room)



if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)