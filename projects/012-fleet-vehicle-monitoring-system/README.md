# Fleet Vehicle Monitoring System

## Project Specifications:

The Fleet Vehicle Monitoring System is designed to provide comprehensive monitoring and management capabilities for a fleet of vehicles. Below are detailed specifications for the key functionalities:

1. **Vehicle Information Management:**
   - **Description:** Capture and manage essential information about each vehicle in the fleet.
   - **Features:**
     - Record license plate, model, current GPS location, engine status, fuel level, and mileage.
     - Ensure real-time updates for critical vehicle parameters.

2. **Real-time Monitoring:**
   - **Description:** Enable administrators to monitor the fleet's status in real time.
   - **Features:**
     - Track vehicles on a map with dynamic updates.
     - Receive instant alerts for critical events such as engine issues or low fuel levels.
     - View aggregated statistics for the entire fleet.

3. **Integration with Maintenance Services:**
   - **Description:** Facilitate communication with maintenance service providers to ensure timely and effective vehicle maintenance.
   - **Features:**
     - Implement SOAP web services for requesting and updating scheduled maintenance information.
     - Generate alerts for upcoming maintenance tasks.
     - Confirm the execution of maintenance interventions.

4. **User Authentication and Authorization:**
   - **Description:** Implement a secure user authentication system to control access to the system.
   - **Features:**
     - User roles (e.g., Administrator, Technician) to control access levels.
     - Secure storage and validation of user credentials.
     - User session management for enhanced security.

5. **Flexible Querying with GraphQL:**
   - **Description:** Implement a GraphQL-based API to provide flexible querying capabilities for administrators.
   - **Features:**
     - GraphQL queries for obtaining fleet information, real-time vehicle location, and customized reports.
     - Dynamic and interactive user interface powered by GraphQL.

## SOAP and GraphQL Specifications:

**SOAP Integration:**
- Implement SOAP web services for communication with maintenance service providers.
- Services:
  - `GetScheduledMaintenance`: Retrieve scheduled maintenance information.
  - `UpdateMaintenanceStatus`: Update the status of a maintenance task.
  - `MaintenanceAlert`: Receive alerts for critical maintenance issues.

**GraphQL Integration:**
- Implement a GraphQL schema with the following capabilities:
  - Query for fleet information.
  - Query for real-time location of a specific vehicle.
  - Execute queries for customized reports on fuel consumption or mileage.
  - Interactive user interface powered by dynamic GraphQL queries.

## Database Schema:

```sql
-- Create Vehicles table
CREATE TABLE Vehicles (
    VehicleID INT PRIMARY KEY,
    LicensePlate VARCHAR(255),
    Model VARCHAR(255),
    CurrentLocationLatitude DECIMAL(10, 7),
    CurrentLocationLongitude DECIMAL(10, 7),
    EngineStatus TINYINT,
    FuelLevel FLOAT,
    Mileage INT
);

-- Insert data into Vehicles table
INSERT INTO Vehicles (VehicleID, LicensePlate, Model, CurrentLocationLatitude, CurrentLocationLongitude, EngineStatus, FuelLevel, Mileage)
VALUES
    (1, 'ABC123', 'Sedan', 40.7128, -74.0060, 1, 80.5, 50000),
    (2, 'XYZ789', 'SUV', 34.0522, -118.2437, 0, 65.2, 60000),
    (3, 'DEF456', 'Truck', 41.8781, -87.6298, 1, 75.0, 70000),
    (4, 'GHI789', 'Coupe', 37.7749, -122.4194, 0, 60.8, 45000),
    (5, 'JKL012', 'Van', 33.4484, -112.0740, 1, 90.2, 80000),
    (6, 'MNO345', 'Convertible', 32.7767, -96.7970, 0, 55.5, 55000),
    (7, 'PQR678', 'Hatchback', 30.2672, -97.7431, 1, 78.3, 60000),
    (8, 'STU901', 'Motorcycle', 39.9526, -75.1652, 0, 70.1, 30000),
    (9, 'VWX234', 'Electric', 45.5051, -122.6750, 1, 85.5, 40000),
    (10, 'YZA567', 'Crossover', 42.3601, -71.0589, 0, 65.0, 65000);

-- Create Maintenance table
CREATE TABLE Maintenance (
    MaintenanceID INT PRIMARY KEY,
    VehicleID INT,
    Description VARCHAR(255),
    ScheduledDate DATE,
    Status VARCHAR(255),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID)
);

-- Insert data into Maintenance table
INSERT INTO Maintenance (MaintenanceID, VehicleID, Description, ScheduledDate, Status)
VALUES
    (1, 1, 'Oil Change', '2023-01-15', 'Scheduled'),
    (2, 2, 'Brake Inspection', '2023-02-20', 'Completed'),
    (3, 3, 'Tire Rotation', '2023-03-10', 'Scheduled'),
    (4, 4, 'Transmission Service', '2023-04-05', 'Completed'),
    (5, 5, 'Air Filter Replacement', '2023-05-22', 'Scheduled'),
    (6, 6, 'Spark Plug Change', '2023-06-15', 'Completed'),
    (7, 7, 'Coolant Flush', '2023-07-30', 'Scheduled'),
    (8, 8, 'Chain Adjustment', '2023-08-18', 'Completed'),
    (9, 9, 'Battery Replacement', '2023-09-25', 'Scheduled'),
    (10, 10, 'Wheel Alignment', '2023-10-12', 'Completed');

-- Create Users table
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255),
    Password VARCHAR(255),
    Role VARCHAR(255)
);

-- Insert data into Users table
INSERT INTO Users (UserID, Username, Password, Role)
VALUES
    (1, 'admin', 'hashed_password', 'Administrator'),
    (2, 'technician', 'hashed_password', 'Technician'),
    (3, 'driver1', 'hashed_password', 'Driver'),
    (4, 'driver2', 'hashed_password', 'Driver'),
    (5, 'manager1', 'hashed_password', 'Manager'),
    (6, 'manager2', 'hashed_password', 'Manager'),
    (7, 'supervisor1', 'hashed_password', 'Supervisor'),
    (8, 'supervisor2', 'hashed_password', 'Supervisor'),
    (9, 'user1', 'hashed_password', 'User'),
    (10, 'user2', 'hashed_password', 'User');

-- Create UserSessions table
CREATE TABLE UserSessions (
    SessionID INT PRIMARY KEY,
    UserID INT,
    Token VARCHAR(255),
    ExpiryDateTime DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Insert data into UserSessions table
INSERT INTO UserSessions (SessionID, UserID, Token, ExpiryDateTime)
VALUES
    (1, 1, 'token_admin', '2023-01-01 12:00:00'),
    (2, 2, 'token_technician', '2023-01-01 14:00:00'),
    (3, 3, 'token_driver1', '2023-01-02 09:30:00'),
    (4, 4, 'token_driver2', '2023-01-02 11:45:00'),
    (5, 5, 'token_manager1', '2023-01-03 14:30:00'),
    (6, 6, 'token_manager2', '2023-01-03 16:45:00'),
    (7, 7, 'token_supervisor1', '2023-01-04 10:15:00'),
    (8, 8, 'token_supervisor2', '2023-01-04 12:30:00'),
    (9, 9, 'token_user1', '2023-01-05 08:00:00'),
    (10, 10, 'token_user2', '2023-01-05 10:30:00');

```
