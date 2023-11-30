# Smart Building Environmental Monitoring System

## Project Description

In the context of smart buildings, the proposed IoT application aims to monitor and control various devices connected to the building environment. The goal is to optimize energy efficiency, enhance security, and provide a more comfortable environment for occupants. The application focuses on managing devices such as temperature sensors, smart lights, security systems, and energy control devices.

## Key Features

1. **Device Management:**
   - Temperature sensors, smart lights, and security devices can register with the application, providing information about their characteristics and locations.

2. **Device State Monitoring:**
   - The application continuously monitors the temperature of various rooms, the status of lights, and the operation of security systems.

3. **Communication Between Devices:**
   - Temperature sensors send data to the message broker, which routes the information to the central application.
   - Operators can use the socket for real-time interaction with devices, adjusting lights, or receiving emergency notifications.

4. **Real-Time Interaction:**
   - Occupants can use a mobile app or a web dashboard to control lights or monitor temperature in real-time.

5. **Security:**
   - Access to the application is limited to authorized operators through a token-based authentication system.
   - Commands sent through the socket are encrypted to ensure communication security.

6. **Monitoring and Analysis:**
   - Collected data, such as temperature variations and activation times of security systems, is stored in a database for trend analysis and report generation.

7. **Monitoring Dashboard:**
   - A dashboard displays real-time room temperatures, light status, and security system activities.
   - Operators can receive instant notifications in case of anomalies, such as temperature variations and suspicious activities.

8. **Scalability Management:**
   - The application is designed to handle the addition of new sensors and control devices without compromising performance.
   - The use of a distributed message broker allows horizontal scalability to manage the growing number of connected devices.

## Architecture and Technologies Used

### Message and Socket Architecture

The application will follow an architecture based on messages for communication between devices and the central platform. Simultaneously, the use of sockets will enable real-time interaction between the application and devices, providing a reliable bidirectional connection.

### Use of Design Patterns

The application will employ architectural design patterns such as the Observer Pattern to manage updates to the device's state and ensure efficient communication between components.

## IoT Data Simulator

### Instructions

1. Install dependencies by running `npm install mqtt socket.io-client`.
2. Create a file named `simulator.js` and copy the provided code into the file.
3. Ensure that your MQTT message broker is running and that your socket server is running.
4. Run the simulation application with `node simulator.js`.

The simulator will send random temperature data and light status to the MQTT message broker and socket server every 5 seconds.

Now you have a simulation application that can be run locally to generate simulated data and test the functionality of the IoT application without the need for physical devices.

## Simulator Code

```javascript
const mqtt = require('mqtt');
const io = require('socket.io-client');

// Configurazione del message broker
const mqttBroker = 'mqtt://localhost'; // Sostituisci con l'indirizzo del tuo broker MQTT
const mqttTopic = 'sensor/data';

// Configurazione del server socket
const socketServer = 'http://localhost:3000'; // Sostituisci con l'indirizzo del tuo server socket

// Funzione per generare dati casuali
function generateRandomData() {
  return {
    temperature: Math.random() * (30 - 18) + 18, // Simula la temperatura tra 18°C e 30°C
    lightStatus: Math.random() > 0.5 ? 'on' : 'off', // Simula lo stato delle luci
  };
}

// Connessione al broker MQTT
const mqttClient = mqtt.connect(mqttBroker);

mqttClient.on('connect', () => {
  console.log('Simulator connected to MQTT broker');
});

// Connessione al server socket
const socket = io.connect(socketServer);

socket.on('connect', () => {
  console.log('Simulator connected to Socket.IO server');
});

// Simulazione dell'invio di dati ogni 5 secondi
setInterval(() => {
  const sensorData = generateRandomData();

  // Invia dati al broker MQTT
  mqttClient.publish(mqttTopic, JSON.stringify(sensorData));

  // Invia dati al server socket
  socket.emit('sensorData', sensorData);

  console.log('Data sent:', sensorData);
}, 5000);

```