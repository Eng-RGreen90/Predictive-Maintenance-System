CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL NOT NULL,
    pressure REAL NOT NULL,
    vibration REAL NOT NULL,
    rotation_speed REAL NOT NULL,
    tool_wear REAL NOT NULL,
    failure INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL NOT NULL,
    pressure REAL NOT NULL,
    vibration REAL NOT NULL,
    rotation_speed REAL NOT NULL,
    tool_wear REAL NOT NULL,
    failure_probability REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);