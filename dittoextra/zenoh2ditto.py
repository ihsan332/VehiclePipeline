# ditto/setup/zenoh_to_ditto.py
import zenoh, json, requests

DITTO_BASE = 'http://localhost:8080/api/2/things/my.namespace:vehicle-01'
AUTH = ('ditto', 'ditto')

ZENOH_TO_FEATURE = {
    'Vehicle/Speed':                'speed/properties/value',
    'Vehicle/OBD/EngineLoad':        'obd/properties/engineLoad',
    'Vehicle/OBD/CoolantTemperature':'obd/properties/coolantTemp',
    'Vehicle/OBD/ThrottlePosition':  'obd/properties/throttle',
    'Vehicle/OBD/Status/DTCCount':   'diagnostics/properties/dtcCount',
}

def on_message(sample):
    key = str(sample.key_expr)
    raw = bytes(sample.payload)
    try:
        payload = json.loads(raw)
        value = payload['payload']['value']
    except Exception as e:
        print(f'[debug] parse failed: {e}')
        return
    feature_path = ZENOH_TO_FEATURE.get(key)
    if not feature_path: return
    url = f'{DITTO_BASE}/features/{feature_path}'
    r = requests.put(url, json=value, auth=AUTH)
    print(f'[ditto] PATCH {feature_path} = {value}  ({r.status_code})')

def main():
    conf = zenoh.Config()
    conf.insert_json5("connect/endpoints", '["tcp/127.0.0.1:7447"]')
    conf.insert_json5("mode", '"client"')
    session = zenoh.open(conf)
    session.declare_subscriber('Vehicle/**', on_message)
    print('[ditto] Subscribed to Zenoh. Updating twin...')
    import time
    while True: time.sleep(1)

if __name__ == '__main__':
    main()
