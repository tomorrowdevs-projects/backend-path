# Wind Turbine Monitoring System

## Project Description

This educational project aims to develop a simplified system for monitoring the performance of wind turbines. We will leverage both NoSQL and relational databases, architectural design patterns, and implement security measures, testing, and scalability management.

## Project Specifications

### Required Features

1. **Turbine Registration:**
   - Capability to input basic information for a turbine: name, location, and operational status.
   - Use of a NoSQL database to store basic turbine data.

2. **Operational Data Monitoring:**
   - Creation of an endpoint to record operational data, such as wind speed and power production.
   - Utilization of a relational database to store operational data.

3. **Simple Analysis and Reporting:**
   - Implementation of a function calculating the average power production of turbines.
   - Creation of an endpoint returning this average.
   - Utilization of appropriate architectural design patterns to organize the code (e.g., MVC).

4. **Advanced Security:**
   - Implementation of JWT token-based authentication mechanisms.
   - Protection of APIs against SQL injection and XSS attacks through proper data validation and sanitization.

5. **Testing and Debugging:**
   - Implementation of unit tests to verify the correctness of functionalities.
   - Utilization of debugging tools to analyze and resolve any issues.

6. **Scalability Management:**
   - Configuration for horizontal scalability using distributed databases and cloud computing services.
   - Utilization of architectural design patterns to efficiently handle horizontal growth.

7. **Cache and CDN:**
   - Implementation of caching to temporarily store frequently requested data.
   - Integration of CDN for the global distribution of static content, improving resource loading speed.

## Database Schema

```sql
-- Relational Schema
CREATE TABLE turbines (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  operational_status VARCHAR(50) NOT NULL
);

CREATE TABLE operational_data (
  id SERIAL PRIMARY KEY,
  turbine_id INTEGER REFERENCES turbines(id),
  wind_speed DECIMAL(5, 2) NOT NULL,
  power_production INTEGER NOT NULL,
  timestamp TIMESTAMP NOT NULL
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL
);
```

## Initial Migration file

```sql
-- Initial Migration

-- Turbines Table
INSERT INTO turbines (name, location, operational_status) VALUES
  ('Turbine A', 'Location A', 'Operational'),
  ('Turbine B', 'Location B', 'Under Maintenance'),
  ('Turbine C', 'Location C', 'Operational'),
  ('Turbine D', 'Location D', 'Under Maintenance'),
  ('Turbine E', 'Location E', 'Operational'),
  ('Turbine F', 'Location F', 'Operational'),
  ('Turbine G', 'Location G', 'Under Maintenance'),
  ('Turbine H', 'Location H', 'Operational'),
  ('Turbine I', 'Location I', 'Under Maintenance'),
  ('Turbine J', 'Location J', 'Operational');

-- Operational Data Table
INSERT INTO operational_data (turbine_id, wind_speed, power_production, timestamp) VALUES
  (1, 10.5, 200, '2023-01-01 08:00:00'),
  (2, 8.0, 150, '2023-01-01 08:05:00'),
  (3, 12.3, 250, '2023-01-01 08:10:00'),
  (4, 9.8, 180, '2023-01-01 08:15:00'),
  (5, 11.2, 220, '2023-01-01 08:20:00'),
  (6, 10.0, 200, '2023-01-01 08:25:00'),
  (7, 8.5, 160, '2023-01-01 08:30:00'),
  (8, 13.1, 280, '2023-01-01 08:35:00'),
  (9, 9.2, 190, '2023-01-01 08:40:00'),
  (10, 10.8, 210, '2023-01-01 08:45:00');

-- Users Table
INSERT INTO users (username, password) VALUES
  ('admin', 'hashed_admin_password'),
  ('operator1', 'hashed_operator_password'),
  ('operator2', 'hashed_operator_password');
``````