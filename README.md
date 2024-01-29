# moos-tak

`moos-tak` is a Python application that subscribes to MOOS NODE_REPORT messages and publishes their names and locations via Cursor on Target (CoT) to an ATAK network of your choice. It utilizes Docker for easy deployment and environment consistency.

## Features

- **MOOS Integration**: Subscribes to NODE_REPORT messages from MOOS.
- **CoT Publication**: Publishes location data to an ATAK network.
- **Friend/Foe Identification**: Differentiates based on naming conventions in CoT messages.

## Installation

To set up `moos-tak`, follow these steps:

1. Clone the repository or download the source code.
2. Navigate to the `moos-tak` directory, containing the Dockerfile.

## Building the Docker Container

Build the Docker container with the following command in the `moos-tak` directory:

```bash
sudo docker build -t moos-tak .
```

## Using the Software
`moos-tak` subscribes to MOOSDB NODE_REPORT messages and sends CoT messages as friendly or hostile based on the agents name (i.e. if the name starts with 'blue' or 'red'). If the agents do not have a name starting with blue or red they will be identified as a neutral CoT message. 

Default IP address is tcp://137.184.101.150:8087

1. Start a moos simulation, the one used for this repo is ./launch demo in /moos-ivp-aquaticus/missions/jervis-2023.
2. Run the following in your `moos-tak` directory
```bash
sudo docker run --network host moos-tak
```
