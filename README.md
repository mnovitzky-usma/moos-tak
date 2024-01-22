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
