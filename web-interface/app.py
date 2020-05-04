import json
from flask import (
Flask,
request,
jsonify,
Response,
render_template
)
import util
from map.device import Device
from map.router import DEFAULT_ACCESS_POINTS
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def location_from_router():
    return jsonify(SSID='Beesafe Router 1',
                  RSSI='-10dBm')

@app.route('/routers', methods=['GET'])
def static_routers():
    pass


@app.route('/devices', methods=['GET'])
def list_devices():
    store, _ = util.retrieve_store(f'{util.STORE_PATH}/devices.pickle')
    return jsonify(json.dumps(store, default=lambda x: x.__dict__))

@app.route('/devices/retrieve/<id>/', methods=['GET'])
def retrive_device(id):
    store, _ = util.retrieve_store(f'{util.STORE_PATH}/devices.pickle')
    if store.get(id, None) is not None:
        return jsonify(store[id])
    return jsonify(error=f'device with id {id} not found')

@app.route('/devices/update/', methods=['POST'])
def update_device():
    store, _ = util.retrieve_store(f'{util.STORE_PATH}/devices.pickle')
    result = None
    try:
        result = json.loads(request.data)
        if result.get('id', None) is None:
            return jsonify(error='device ID not specified')
        elif result.get('rssi', None) is None:
            return jsonify(error='device rssi not specified')
    except json.JSONDecodeError:
        return jsonify(error='invalid post data')
    except Exception as e:
        return jsonify(error=e)
    
    if store.get(result['id'], None) is not None:
        try:
            d = store[result['id']]
            d.signal_strengths = result['rssi']
            d.compute_coordinate()
            util.save_device_info(result['id'], d)
            return jsonify(status='device stats successfully updated')
        except Exception as err:
            return jsonify(error='Internal server error',
                          detail=str(err))
    return jsonify(error=f'device with id {result["id"]} not found')


@app.route('/register', methods=['POST'])
def register_device_on_map():
    result = None
    try:
        result = json.loads(request.data)
        if result.get('id', None) is None:
            return jsonify(error='device ID not specified')
    except json.JSONDecodeError:
        return jsonify(error='invalid post data')
    except Exception as e:
        return jsonify(error=e)
    
    d = Device(result['id'])
    util.save_device_info(result['id'], d)
    return jsonify(
        status=f'device with id {result["id"]} has been successfully saved')

@app.route('/unregister/<id>/', methods=['GET'])
def unregister_device_on_map(id):
    util.delete_device_info(id)
    return jsonify(status=f'device {id} successfully unregistered ')

if __name__ == '__main__':
    app.run(debug=True)