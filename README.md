# CAN Bus Based Vehicle Monitoring and Fault Detection Simulation

## Overview

This project simulates CAN bus communication between multiple vehicle Electronic Control Units (ECUs) using Python. The system includes Engine ECU, Battery ECU, Brake ECU, and Dashboard ECU. Each ECU sends encoded CAN messages through a virtual CAN bus. The Dashboard ECU receives the CAN messages, decodes them, detects vehicle faults, logs the data into a CSV file, generates graphs, and displays a diagnostic summary.

This project is developed without physical CAN hardware using a virtual CAN interface.

---

## Features

* Virtual CAN bus communication using `python-can`
* Multi-ECU simulation
* CAN message encoding and decoding
* Vehicle parameter monitoring
* Fault detection system
* CSV data logging
* Graph generation using `matplotlib`
* Diagnostic summary generation
* Modular Python code structure

---

## ECUs Simulated

| ECU           | Function                                                        |
| ------------- | --------------------------------------------------------------- |
| Engine ECU    | Sends speed, RPM, and engine temperature                        |
| Battery ECU   | Sends battery voltage, battery current, and battery temperature |
| Brake ECU     | Sends brake status                                              |
| Dashboard ECU | Receives, decodes, logs, and detects faults                     |

---

## CAN ID Mapping

| CAN ID  | Message                     | Sender ECU  |
| ------- | --------------------------- | ----------- |
| `0x100` | Speed and RPM               | Engine ECU  |
| `0x101` | Engine Temperature          | Engine ECU  |
| `0x200` | Battery Voltage and Current | Battery ECU |
| `0x201` | Battery Temperature         | Battery ECU |
| `0x300` | Brake Status                | Brake ECU   |

---

## Fault Detection Logic

| Fault Condition            | Fault Code | Priority |
| -------------------------- | ---------- | -------- |
| Speed > 100 km/h           | `V001`     | Medium   |
| RPM > 4000 RPM             | `E001`     | Medium   |
| Engine Temperature > 100°C | `E002`     | High     |
| Battery Voltage < 11V      | `B001`     | High     |
| Battery Temperature > 45°C | `B002`     | High     |
| Brake Status = 2           | `C001`     | Critical |

---

## Project Workflow

```text
Vehicle Model
     ↓
Engine ECU / Battery ECU / Brake ECU
     ↓
CAN Message Encoding
     ↓
Virtual CAN Bus
     ↓
Dashboard ECU
     ↓
CAN Message Decoding
     ↓
Fault Detection
     ↓
CSV Logging
     ↓
Graph Generation
     ↓
Diagnostic Summary
```

---

## System Architecture

```text
                 ┌──────────────────┐
                 │  Vehicle Model   │
                 └────────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
 │ Engine ECU  │   │ Battery ECU │   │  Brake ECU  │
 └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
        │                 │                 │
        ▼                 ▼                 ▼
 ┌───────────────────────────────────────────────┐
 │              Virtual CAN Bus                  │
 └──────────────────────┬────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Dashboard ECU  │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌──────────┐  ┌────────────┐  ┌────────────┐
   │ Decoder  │  │ Fault Check│  │ CSV Logger │
   └──────────┘  └────────────┘  └────────────┘
                                      │
                                      ▼
                              ┌────────────┐
                              │   Graphs   │
                              └────────────┘
                                      │
                                      ▼
                              ┌────────────┐
                              │  Summary   │
                              └────────────┘
```

---

## Project Folder Structure

```text
CAN/
│
├── src/
│   ├── main.py
│   ├── can_ids.py
│   ├── vehicle_model.py
│   ├── encoders.py
│   ├── decoders.py
│   ├── ecus.py
│   ├── dashboard.py
│   ├── fault_detector.py
│   ├── logger.py
│   ├── plotter.py
│   └── diagnostic_summary.py
│
├── data/
│   └── can_log.csv
│
├── plots/
│   ├── speed_vs_time.png
│   ├── rpm_vs_time.png
│   ├── engine_temp_vs_time.png
│   ├── battery_voltage_vs_time.png
│   ├── battery_temp_vs_time.png
│   └── fault_count.png
│
├── docs/
│   └── project_report.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Software Requirements

* Python 3.12 or above
* VS Code
* `python-can`
* `pandas`
* `matplotlib`

---

## Installation and Setup

### 1. Clone or download the project

Open the project folder in VS Code.

### 2. Create virtual environment

```bash
python -m venv .venv
```

If Python is accessed using `py`, use:

```bash
py -m venv .venv
```

### 3. Activate virtual environment

For Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

If script execution is blocked, run:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```bash
.venv\Scripts\Activate.ps1
```

### 4. Install required packages

```bash
pip install -r requirements.txt
```

---

## How to Run

### Local web dashboard

From PowerShell in the project folder, run ` .\dashboard.cmd ` and open
http://127.0.0.1:8000. Keep the server running while using the app.

The HTML/CSS/JavaScript dashboard uses Python's standard-library HTTP server.
No additional packages or external web services are needed. Choose a run length,
click **Start simulation**, inspect live readings and fault events, or click
**Stop** to end early and save reports. Reports include six graphs, CSV export,
and the diagnostic summary in the expandable console. Each run replaces the
previous CSV log and generated plots.

The environment (`.venv`), caches and app logs (`.runtime`), data (`data`),
and graphs (`plots`) stay inside this project. Stop the app before deleting
the folder. The app uses the existing Python installation behind `.venv`.

### Original terminal simulation

Run the main simulation:

```bash
python src\main.py
```

The program will automatically:

```text
Start CAN simulation
Send CAN messages from ECUs
Receive and decode CAN messages
Detect faults
Save data into CSV
Generate graphs
Print diagnostic summary
```

---

## Output

The project generates the following outputs:

### 1. Terminal Output

The terminal displays CAN messages and decoded vehicle data.

Example:

```text
[Engine ECU] Sent CAN ID 0x100
[Dashboard] {'source': 'Engine ECU', 'parameter': 'speed_rpm', 'speed': 105, 'rpm': 4499}
```

### 2. Fault Warnings

Example:

```text
[Medium WARNING] V001 - Overspeed detected: 105 km/h
[Medium WARNING] E001 - High RPM detected: 4499 RPM
[High WARNING] B002 - Battery overheating: 52 °C
[Critical WARNING] C001 - Brake system fault detected
```

### 3. CSV Log File

The decoded CAN data and fault details are stored in:

```text
data/can_log.csv
```

CSV columns include:

```text
timestamp
source
parameter
speed
rpm
engine_temp
battery_voltage
battery_current
battery_temp
brake_status
brake_text
fault_code
priority
message
```

### 4. Graphs

Graphs are generated in the `plots` folder:

| Graph File                    | Description               |
| ----------------------------- | ------------------------- |
| `speed_vs_time.png`           | Vehicle speed variation   |
| `rpm_vs_time.png`             | Engine RPM variation      |
| `engine_temp_vs_time.png`     | Engine temperature trend  |
| `battery_voltage_vs_time.png` | Battery voltage trend     |
| `battery_temp_vs_time.png`    | Battery temperature trend |
| `fault_count.png`             | Fault count by type       |

### 5. Diagnostic Summary

Example:

```text
========== DIAGNOSTIC SUMMARY ==========
Total logged messages: 131
Total faults detected: 43

Fault count by code:
E001    13
B002    11
V001    11
E002     6
C001     2

Fault count by priority:
Medium      24
High        17
Critical     2

Maximum speed: 140.0 km/h
Maximum RPM: 5500.0 RPM
Maximum engine temperature: 112.0 °C
Minimum battery voltage: 12.6 V
Maximum battery temperature: 60.0 °C
========================================
```

---

## Module Explanation

### `main.py`

Controls the complete simulation. It creates the vehicle model, virtual CAN buses, ECUs, and Dashboard ECU. It starts the simulation, stops it after a fixed time, generates graphs, and prints the diagnostic summary.

### `vehicle_model.py`

Generates virtual vehicle parameters such as speed, RPM, engine temperature, battery voltage, battery current, battery temperature, and brake status.

### `can_ids.py`

Stores all CAN message IDs used in the project.

### `encoders.py`

Converts vehicle parameter values into CAN byte data.

### `decoders.py`

Converts received CAN byte data back into readable vehicle parameters.

### `ecus.py`

Contains Engine ECU, Battery ECU, and Brake ECU classes. Each ECU sends CAN messages at regular intervals.

### `dashboard.py`

Receives CAN messages, decodes them, detects faults, displays warnings, and logs data.

### `fault_detector.py`

Checks decoded values against predefined safety limits and generates fault warnings.

### `logger.py`

Stores received data and detected faults in `data/can_log.csv`.

### `plotter.py`

Reads the CSV log file and generates graphs.

### `diagnostic_summary.py`

Reads the CSV file and prints a final diagnostic summary.

---

## Applications

* Automotive communication learning
* CAN bus simulation
* ECU communication understanding
* Vehicle fault monitoring
* Embedded systems project
* Automotive diagnostics concept demonstration
* Foundation for Battery Management System communication

---

## Future Improvements

* Add Tire Pressure Monitoring ECU
* Add real-time GUI dashboard
* Add DBC file support
* Add real CAN hardware support
* Add SocketCAN support on Linux
* Add diagnostic trouble code history
* Extend the project to Battery Management System communication
* Send SOC and SOH values over CAN in future versions

---

## Conclusion

This project successfully demonstrates a software-based CAN bus vehicle monitoring and fault detection system. Multiple virtual ECUs transmit encoded CAN messages through a virtual CAN bus. The Dashboard ECU receives and decodes the messages, detects faults, logs data into a CSV file, generates graphs, and displays a diagnostic summary. The project provides practical understanding of CAN communication, ECU interaction, vehicle diagnostics, and automotive embedded system concepts without requiring physical hardware.
