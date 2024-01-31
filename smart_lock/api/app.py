from flask import Flask, request

import sys         
sys.path.append('/home/pi/my-app')  

from controller import Door 

door = Door()


app = Flask(__name__)




@app.route('/on')
def on():
    door.open()
    return {"Door": True}

@app.route('/off')
def off():
    door.close()
    return {"Door": False}

