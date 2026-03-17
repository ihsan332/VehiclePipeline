## Summary 

**Data Abstraction Layer**:
Kuksa is used in this section and acts as the entry point for all vehicle data from our simulations. It is shown to receive raw vehicle signals published by the vehicle simulator from feed.py. These signals are normalized and stored according to the VSS and then bridged to Zenoh, forwarding updated values when received.

**Communication Layer**:
Using Zenoh as the middleware communication layer, it is responsible for transporting vehicle signal data between Kuksa and Ditto. Zenoh has two bridge components, first from Kuksa to Zenoh where it subscribes to any data changes and then from Zenoh to Ditto where it receives messages and formats them as uProtocol payloads and sends them to Ditto via HTTP Rest API calls. Neither Kuksa nor Ditto interacts with the other, decoupling the data layer from the digital twin backend.

**Digital Twin/ Backend State Management**:
Ditto is used as a backend digital twin framework, maintaining the vehicle's current state at all times. It receives the vehicle signal updates from Zenoh by Kuksa via HTTP REST API calls that can update the digital twin to match. The digital twin is continuously updated, and during fault injection, Ditto correctly accepts and stores the injected abnormal values. When the injection is over, the signal is returned to normal, as demonstrated by live vehicle states

**Vehicle Data Source**:
The vehicle data source for this pipeline is implemented using python based simulator. This is called feed.py. This script generates and publishes raw vehicle data telemetry to represent real-time driving conditions. These data variables are speed, tire pressure and various other OBD metrics. This being the origin point of the system's data flow, the simulator pushes their raw signals to the Eclipse Kuksa Data Abstraction layer, where the signals are received and normalized, and stored and passed along the pipeline.

## Prerequisites

- Windows with WSL2 enabled
- Docker Desktop installed and running (with WSL2 backend enabled)
- Python 3.10+ installed in WSL
- Run the following in WSL: pip3 install kuksa-client eclipse-zenoh up-python requests
- Visual Studio Code (Reccomended)


## Setup (Running the System and Reproducing Pipeline Behavior)

 1. Clone this repository 

 2. Clone the Ditto repository (in a WSL Ubuntu terminal) with
    - git clone https://github.com/eclipse-ditto/ditto.git

 3. Run the following commands 
    - cd ditto/deployment/docker
    - cp dev.env .env

 4. Go to ditto/deployment/docker/.env and replace its contents with the following:
    - DITTO_VERSION=3.7.0

 5. Run 
    - docker compose up -d 

 6. Go back to the root directory of the repo with 
    - cd .. 

 7. Once your back in VehiclePipeline run docker compose up -d again 

 8. Run 
    - bash dittoextra/bootstrap.sh

 9. Run each of the following files from a seperate WSL terminal in the following order (If experiencing difficulties try running will the full path which would start along the lines of /mnt/c/...../VehiclePipeline)
    - python3 kuksa/sim/feed.py
    - python3 zenoh/bridge/kuksa2zenoh.py
    - python3 dittoextra/zenoh2ditto.py
 
 10. The pipeline should be successfully running! you can check resource utilization in Docker Desktop 


