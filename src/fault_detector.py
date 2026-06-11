def detect_faults(decoded):
    faults = []

    if decoded["parameter"] == "speed_rpm":
        speed = decoded["speed"]
        rpm = decoded["rpm"]

        if speed > 100:
            faults.append({
                "code": "V001",
                "priority": "Medium",
                "message": f"Overspeed detected: {speed} km/h"
            })

        if rpm > 4000:
            faults.append({
                "code": "E001",
                "priority": "Medium",
                "message": f"High RPM detected: {rpm} RPM"
            })

    elif decoded["parameter"] == "engine_temp":
        engine_temp = decoded["engine_temp"]

        if engine_temp > 100:
            faults.append({
                "code": "E002",
                "priority": "High",
                "message": f"Engine overheating: {engine_temp} °C"
            })

    elif decoded["parameter"] == "battery_voltage_current":
        battery_voltage = decoded["battery_voltage"]

        if battery_voltage < 11.0:
            faults.append({
                "code": "B001",
                "priority": "High",
                "message": f"Low battery voltage: {battery_voltage} V"
            })

    elif decoded["parameter"] == "battery_temp":
        battery_temp = decoded["battery_temp"]

        if battery_temp > 45:
            faults.append({
                "code": "B002",
                "priority": "High",
                "message": f"Battery overheating: {battery_temp} °C"
            })

    elif decoded["parameter"] == "brake_status":
        brake_status = decoded["brake_status"]

        if brake_status == 2:
            faults.append({
                "code": "C001",
                "priority": "Critical",
                "message": "Brake system fault detected"
            })

    return faults