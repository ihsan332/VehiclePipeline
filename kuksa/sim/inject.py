import datetime, time
from kuksa_client.grpc import VSSClient, Datapoint

FAULTS = {
    "Vehicle.Speed": 4000000000000000000000.0,
    "Vehicle.OBD.EngineLoad": 900000000000000009.9,
    "Vehicle.OBD.CoolantTemperature": 1222222222222222222220.0, 
    "Vehicle.OBD.ThrottlePosition": 101111111111111111111111110.0,
}

with VSSClient("127.0.0.1", 55555) as client:
    for i in range(10000):
        t0 = datetime.datetime.now(datetime.timezone.utc)
        client.set_current_values({k: Datapoint(v) for k, v in FAULTS.items()})
        print(f"[{i+1}/{10000}] T0={t0.isoformat()} — fault injected")
        time.sleep(0.01)

print("Done.")