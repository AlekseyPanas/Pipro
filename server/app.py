import os
import json
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from datetime import datetime

#from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#Create a dict for JSON values, NOTE:python dict is basically json object
#{ping: [
#  {
#    id: int
#    location: [x,y]
#    active: bool
#  },
#  ...
#]}
ping_dict={"ping":[]}


@app.route('/', methods=["GET", "POST"])
def index():
    """Our excting new homepage"""
    return render_template("index.html")


@app.route('/ping-data', methods=["GET", "POST"])
def ping_add(data: list):
    """Add ping data to json file and return it"""
    if request.method == "POST":

        #first find id 
        count=1+len(ping_dict["ping"])
        #create the json object to be added
        temp={"id": count, "location": data, "active": True}
        ping_dict["ping"].append(temp)

        return ping_dict



@app.route('/ping-data', methods=["GET", "POST"])
def ping_disable(ping_id):
    """disable ping with this id"""
    if request.method == "POST":    
        for item in ping_dict["ping"]:
            if item["id"]==ping_id:
                item["active"]=False
        return ping_dict

@app.route('/data', methods=["GET", "POST"])
def get_pings():
    "return stringified data jason data"
    if request.method == "GET":
        # return jsonify("values.txt")
        #return {"tetsing":"test"}
        return ping_dict



'''
#version 1
import os
import json
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from datetime import datetime

#from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#Create a new file for json Values
f = open("values.txt", "r+")



@app.route('/', methods=["GET", "POST"])
def index():
    """Our excting new homepage"""
    return render_template("index.html")


@app.route('/ping-data', methods=["GET", "POST"])
def ping_add(data):
    """Add ping data to json file and return it"""
    if request.method == "POST":

        #read the json file
        with open("values.txt", "r+") as f:
            obj = json.load(f)

        #add item to list 
        obj["ping"].append(data)

        #return json file
        return jsonify(f)


@app.route('/ping-data', methods=["GET", "POST"])
def ping_disable(ping_id):
    """disable ping with this id"""
    if request.method == "POST":    
        with open(f"values.txt", "r+") as f:
            obj1 = json.load(f)
        # Iterate through the objects in the JSON and change                     
        #the obj once we find it.

        #list of pings
        obj=obj1["ping"]

        # Iterate through the objects in the JSON and change                     
        #the obj once we find it.
        for i in range(len(obj)):
            if obj[i]["id"] == ping_id:
                #obj.pop(i)
                obj[i]["active"] = False
                break

        # Output the updated file with JSON                                      
        f = open("values.txt", "w").write(json.dumps(obj))
        return jsonify(f)

@app.route('/data', methods=["GET", "POST"])
def get_pings():
    "return stringified data jason data"
    if request.method == "GET":
        # return jsonify("values.txt")
        return {"tetsing":"test"}

f.close()
'''


"""
@app.route('/ping', methods=["GET"])
def get_pings():
    if request.method == "GET":
        y = json.dumps(data)
        return data


    if request.method=="POST":
        ping = request.form.get("ping")
        
"""  




"""
app.post(data)  # Simulation sends ping location
    - Add ping to json with new unique id and location 
app.get("/") # Load main page
app.post(ping_id) # Disable ping with this id
app.get_pings() # Send stringified json data

{ping: [
  {
    id: int
    location: [x,y]
    active: bool
  },
  ...
]}

"""
