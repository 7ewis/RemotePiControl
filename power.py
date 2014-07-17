# add flask here
from flask import Flask
app = Flask(__name__)
app.debug = True
# keep your code
import time
import cgi
from tellcore.telldus import TelldusCore
core = TelldusCore()
devices = core.devices()

# define a "power ON api endpoint"
@app.route("/API/v1.0/power-on/<deviceId>",methods=['POST'])
def powerOnDevice(deviceId):
    payload = {}
    #get the device by id somehow
    device = devices[deviceId]
    # get some extra parameters 
    # let's say how long to stay on
    params = request.get_json()
    try:
      device.turn_on()
      payload['success'] = True
      return payload
    except:
      payload['success'] = False
      # add an exception description here
      return payload

# define a "power OFF api endpoint"
@app.route("/API/v1.0/power-off/<deviceId>",methods=['POST'])
def powerOffDevice(deviceId):
    payload = {}
    #get the device by id somehow
    device = devices[deviceId]
    try:
      device.turn_off()
      payload['success'] = True
      return payload
    except:
      payload['success'] = False
      # add an exception description here
      return payload

app.run()
