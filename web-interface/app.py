import json
from flask import (
Flask,
request,
jsonify,
Response
)
import util 
app = Flask(__name__)


@app.route('/location', methods=['POST'])
def location_from_router():
    return jsonify(SSID='Beesafe Router 1',
                  RSSI='-10dBm')

@app.route('/devices', methods=['GET'])
def list_devices():
    store, _ = util.retrieve_store(f'{util.STORE_PATH}/devices.pickle')
    return jsonify(**store)

@app.route('/register', methods=['POST'])
def register_device_on_map():
    result = None
    try:
        result = json.loads(request.data)
        if result.get('id', None) is None:
            raise Exception('device ID not specified')
    except json.JSONDecodeError:
        return jsonify(error='invalid post data')
    except Exception as e:
        return jsonify(error=e)
    
    util.save_device_info(result['id'], result)
    return jsonify(
        status=f'device with id {result["id"]} has been successfully saved')

@app.route('/unregister/<id>/', methods=['GET'])
def unregister_device_on_map(id):
    util.delete_device_info(id)
    return jsonify(status=f'device {id} successfully unregistered ')

if __name__ == '__main__':
    app.run(debug=True)