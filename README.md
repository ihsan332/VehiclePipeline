## Summary 

**Data Abstraction Layer**:
Kuksa is used in this section and acts as the entry point for all vehicle data from our simulations. It is shown to receive raw vehicle signals published by the vehicle simulator from feed.py. These signals are normalized and stored according to the VSS and then bridged to Zenoh, forwarding updated values when received.

**Communication Layer**:
Using Zenoh as the middleware communication layer, it is responsible for transporting vehicle signal data between Kuksa and Ditto. Zenoh has two bridge components, first from Kuksa to Zenoh where it subscribes to any data changes and then from Zenoh to Ditto where it receives messages and formats them as uProtocol payloads and sends them to Ditto via HTTP Rest API calls. Neither Kuksa nor Ditto interacts with the other, decoupling the data layer from the digital twin backend.

**Digital Twin/ Backend State Management**:
Ditto is used as a backend digital twin framework, maintaining the vehicle's current state at all times. It receives the vehicle signal updates from Zenoh by Kuksa via HTTP REST API calls that can update the digital twin to match. The digital twin is continuously updated, and during fault injection, Ditto correctly accepts and stores the injected abnormal values. When the injection is over, the signal is returned to normal, as demonstrated by live vehicle states

**Vehicle Data Source**:
The vehicle data source for this pipeline is implemented using python based simulator. This is called feed.py. This script generates and publishes raw vehicle data telemetry to represent real-time driving conditions. These data variables are speed, tire pressure and various other OBD metrics. This being the origin point of the system's data flow, the simulator pushes their raw signals to the Eclipse Kuksa Data Abstraction layer, where the signals are received and normalized, and stored and passed along the pipeline.

### Iteration 2

**System Extension**: 
The extension that was implemented was to introduce sensor faults with abnormal or impossible values (A stated speed of 400km/h in a car that can only go 170km/h). These values were also injected repeatedly at a rate of 10 injections per second. This sharp increase in rate (from the default loop, which runs once every 2 seconds) is implemented to observe system behaviour under extremely high loads that could be caused by faulty software or a malicious attack. The default and injection values are outlined below.

**Non-Functional Testing**: 
Non-Functional tests involved measuring the CPU and memory usage during:
 - Regular system operation
 - Abnormal conditions

By running the injection script to throw abnormal values over the course of ~1.5 minutes, we can observe how the system reacts before, during and after the injections.

**Experiment Analysis**:
During normal operations CPU stayed low at around 35%. When the injection started, CPU usage spiked, reaching up to 189.7%. This is because the Zenoh bridge and Ditto Rest API were flooded with multiple PATCH requests per second, as well as the normal feed. While the script is running, the system is processing, but remains under much higher loads than normal. CPU usage stabilized after the injections were complete at 22:04:00 and maintained the same numbers as before the injection, indicating that a full recovery of the system was successfully achieved.

Before, during and after injection, memory stayed consistent throughout the test at 2.47GB. This means the pipeline has no memory leak under higher loads. This also means that Ditto, Kuksa and Zenoh were all able to manage messages without an increase in memory.

Overall, the system is CPU sensitive but remains memory stable under high injection conditions. The pipeline shows the ability to successfully process all injection signals without crashing or dropping the connections. That and the fact that signals returned to normal after injection prove the systems are still functional. 


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
    - **for iteration 2** python3 kuksa/sim/inject.py (if you want to start the injections)
 
 10. The pipeline should be successfully running! you can check resource utilization in Docker Desktop 


