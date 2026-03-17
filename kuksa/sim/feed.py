import time, random
from kuksa_client.grpc import VSSClient, Datapoint

SIGNALS = [
    ("Vehicle.Speed",                        60.0),
    ("Vehicle.OBD.EngineLoad",               45.2),
    ("Vehicle.OBD.CoolantTemperature",       90.0),
    ("Vehicle.OBD.ThrottlePosition",         30.1),
    ("Vehicle.OBD.FuelPressure",             350.0),
    ("Vehicle.OBD.ShortTermFuelTrim1",       -2.3),
    ("Vehicle.Chassis.Axle.Row1.Wheel.Left.Tire.Pressure",  230.0),
]

def main():
    with VSSClient("127.0.0.1", 55555) as client:
        print("[sim] Connected to Kuksa. Feeding signals...")
        while True:
            for path, value in SIGNALS:
                jittered = value + random.uniform(-0.5, 0.5)
                client.set_current_values({path: Datapoint(jittered)})
                print(f"[sim] SET {path} = {jittered:.2f}")
            time.sleep(2)

if __name__ == "__main__":
    main()