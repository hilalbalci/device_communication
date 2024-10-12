# Device Communication API

This repository contains a FastAPI-based project for managing device communication through a GraphQL interface. It includes a TCP server for receiving device data, a consumer for processing the data using RabbitMQ, and a Docker Compose setup for easy deployment.

## Features

- **FastAPI**: Web framework for building APIs with Python.
- **GraphQL**: API endpoints are exposed through GraphQL, allowing clients to fetch data with flexible queries.
- **TCP Server**: Handles incoming device data, such as location information, and forwards it to the consumer for processing.
- **Consumer**: Processes the data received from the TCP server via RabbitMQ.
- **RabbitMQ**: Acts as a message broker, enabling communication between the TCP server and the consumer.
- **Docker Compose**: Easily manage the deployment of the FastAPI server, database, TCP server, RabbitMQ, and the consumer.

### Installation

   ```
   git clone https://github.com/hilalbalci/device_communication.git
   docker-compose up --build
   docker-compose run web alembic upgrade head
   ```


This will start:

The FastAPI server exposing the GraphQL API.
The TCP server that listens for incoming device data.
RabbitMQ for message brokering.
Database for keeping data.
The consumer that processes messages from the TCP server via RabbitMQ.

### Simulating Device Data

The project assumes that devices send their location information to the TCP server. To simulate this behavior, you can use the following command in your terminal:

  ```
   echo '{"device_id": 10, "latitude": 42.7128, "longitude": -73.0060}' | nc localhost 12345
  ```
This command sends a JSON payload containing device_id, latitude, and longitude to the TCP server running on localhost at port 12345.

### GraphQL Endpoints

There are 5 endpoints on GraphQL for this application

1.Create Device

 ```
   mutation MyMutation {
  createDevice(name: "test_name") {
    description
    id
    name
  }
}
 ```

2. Delete Device
 ```
 mutation MyMutation {
  deleteDevice(deviceId: 10)
}
 ```

3. List Devices
  ```
 query MyQuery {
  listDevices {
    description
    id
    name
  }
}
 ```
4. ListLocationsByDevice
```query MyQuery {
  listLocationByDevice(deviceId: 10) {
    deviceId
    latitude
    longitude
    timestamp
  }
}
```

5. ListLocations
 ```query MyQuery {
  listLocations {
    deviceId
    latitude
    longitude
    timestamp
  }
}
```
