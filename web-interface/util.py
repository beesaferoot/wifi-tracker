import pickle
import os

STORE_PATH = os.path.join(os.path.abspath('.'), 'store/')
def create_store(filename : str) -> None:
    abs_path = os.path.join(STORE_PATH, filename)
    with open(abs_path, 'wb') as devices:
        pickle.dump({}, devices)

def store_exists(filename: str) -> bool:
    return os.path.exists(os.path.join(STORE_PATH, filename))

def device_info():
    if not store_exists('devices.pickle'):
        create_store('devices.pickle')
    
    abs_path = os.path.join(STORE_PATH, 'devices.pickle')
    return retrieve_store(abs_path)

def save_device_info(key, value):
    store, path = device_info()
    store[key] = value
    update_store(path, store)

def delete_device_info(key):
    store, path = device_info()
    if store.get(key, None) is not None:
        store.pop(key)
        update_store(path, store)

def retrieve_store(path):
    with open(path, 'rb') as devices:
        store = pickle.load(devices)
    return store, path

def update_store(path, store):
    with open(path, 'wb') as devices:
        pickle.dump(store, devices)
    
