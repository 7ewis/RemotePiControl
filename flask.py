# Import Modules
import time
import cgi
import json
from flask import Flask
from flask import request
from flask import jsonify
from tellcore.telldus import TelldusCore

# Start Flask with Debugging
app = Flask(__name__)
app.debug = True

# Define Telldus Variables
core = TelldusCore()
devices = core.devices()

# API Location
@app.route("/API/v1.0/power",methods=['POST'])

# Function to Power Device
def powerOnDevice():

        # Error Handling
        payload = {}
        payload['success'] = False
        payload['message'] = "An unspecified error occured"

        # Define recieved JSON as Variable
        jsonData = request.get_json()

        # Checks to see if deviceID is valid
        try:
                device = devices[int(jsonData['deviceID'])]
        except:
                payload['message'] = "Invalid deviceId specified"
                return jsonify(**payload)

        # Checks to see if powerAction is specified and valid
        try:
                powerAction = jsonData['powerAction']

                if (jsonData['powerAction'] == "on" or jsonData['powerAction'] == "off"):
                        powerAction = jsonData['powerAction']
        except:
                payload['message'] = "Incorrect powerAction specified"
                return jsonify(**payload)

        # Checks to see if time has been specified and valid
        try:
                poTime = jsonData['poTime']
                poTime = int(poTime)

        except:
                payload['message'] = "Invalid time specified"
                return jsonify(**payload)


        # Checks to see if password is correct
        if (jsonData['password'] == "support"):

                # If time is greater than 0, it turns on for the specified amount of time
                if poTime > 0:
                        device.turn_on()
                        time.sleep(poTime)
                        device.turn_off()
                        payload['success'] = True
                        payload['message'] = "Device turned on for: {} seconds".format(poTime)
                        return jsonify(**payload)

                # If time isn't greater than 0
                else:
                        # Check to see if powerAction is on/off
                        if powerAction == "on":
                                try:
                                        device.turn_on()
                                        payload['success'] = True
                                        payload['message'] = "Device turned on"
                                        return jsonify(**payload)
                                except:
                                        payload['success'] = False
                                        return jsonify(**payload)

                        elif powerAction == "off":
                                try:
                                        device.turn_off()
                                        payload['success'] = True
                                        payload['message'] = "Device turned off"
                                        return jsonify(**payload)
                                except:
                                        payload['success'] = False
                                        return jsonify(**payload)

        # If the password is incorrect
        else:
                payload['message'] = "Incorrect password"
                return jsonify(**payload)

# Flask API/Host Config
app.run(host='0.0.0.0', port=81, debug=True)
