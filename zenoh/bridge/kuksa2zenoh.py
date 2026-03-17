import zenoh, json
from kuksa_client.grpc import VSSClient
from uprotocol.uuid.factory.uuidfactory import Factories

WATCH_PATHS = [
    "Vehicle.Speed",
    "Vehicle.OBD.EngineLoad",
    "Vehicle.OBD.CoolantTemperature",
    "Vehicle.OBD.ThrottlePosition",
    "Vehicle.OBD.FuelPressure",
    "Vehicle.OBD.ShortTermFuelTrim1",
    "Vehicle.OBD.Status.DTCCount",
]

def vss_to_zenoh_key(path: str) -> str:
    return path.replace(".", "/")

def build_umessage(path: str, value: float, timestamp: str) -> dict:
    return {
        "specversion": "1.0",
        "id":          str(Factories.UPROTOCOL.create()),
        "source":      f"up://vehicle/1/vss.{path}/1",
        "type":        "pub.v1",
        "ttl":         5000,
        "payload": {
            "path":      path,
            "value":     value,
            "timestamp": timestamp,
        }
    }

def main():
    conf = zenoh.Config()
    conf.insert_json5("connect/endpoints", '["tcp/127.0.0.1:7447"]')
    conf.insert_json5("mode", '"client"')
    session = zenoh.open(conf)
    with VSSClient("127.0.0.1", 55555) as kuksa:
        print("[bridge] uProtocol/Zenoh bridge running...")
        for updates in kuksa.subscribe_current_values(WATCH_PATHS):
            for path, datapoint in updates.items():
                key     = vss_to_zenoh_key(path)
                msg     = build_umessage(path, datapoint.value, str(datapoint.timestamp))
                payload = json.dumps(msg)
                session.put(key, payload)
                print(f"[bridge] PUB {key}  id={msg['id'][:8]}  val={datapoint.value:.2f}")
    session.close()

if __name__ == "__main__":
    main()