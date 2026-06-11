import can_ids


def decode_message(msg):
    can_id = msg.arbitration_id
    data = list(msg.data)

    if can_id == can_ids.ENGINE_SPEED_RPM:
        speed = data[0]
        rpm = (data[1] << 8) | data[2]

        return {
            "source": "Engine ECU",
            "parameter": "speed_rpm",
            "speed": speed,
            "rpm": rpm
        }

    elif can_id == can_ids.ENGINE_TEMPERATURE:
        engine_temp = data[0]

        return {
            "source": "Engine ECU",
            "parameter": "engine_temp",
            "engine_temp": engine_temp
        }

    elif can_id == can_ids.BATTERY_VOLTAGE_CURRENT:
        battery_voltage = data[0] / 10
        battery_current = data[1]

        return {
            "source": "Battery ECU",
            "parameter": "battery_voltage_current",
            "battery_voltage": battery_voltage,
            "battery_current": battery_current
        }

    elif can_id == can_ids.BATTERY_TEMPERATURE:
        battery_temp = data[0]

        return {
            "source": "Battery ECU",
            "parameter": "battery_temp",
            "battery_temp": battery_temp
        }

    elif can_id == can_ids.BRAKE_STATUS:
        brake_status = data[0]

        brake_text = {
            0: "Normal",
            1: "Brake Applied",
            2: "Brake Fault"
        }.get(brake_status, "Unknown")

        return {
            "source": "Brake ECU",
            "parameter": "brake_status",
            "brake_status": brake_status,
            "brake_text": brake_text
        }

    else:
        return {
            "source": "Unknown",
            "parameter": "unknown",
            "raw_id": hex(can_id),
            "raw_data": data
        }