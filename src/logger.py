import csv
import os
from datetime import datetime


class CANLogger:
    def __init__(self, filepath="data/can_log.csv"):
        self.filepath = filepath

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "source",
                "parameter",
                "speed",
                "rpm",
                "engine_temp",
                "battery_voltage",
                "battery_current",
                "battery_temp",
                "brake_status",
                "brake_text",
                "fault_code",
                "priority",
                "message"
            ])

    def log(self, decoded, faults):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not faults:
            self._write_row(timestamp, decoded, "", "", "")

        for fault in faults:
            self._write_row(
                timestamp,
                decoded,
                fault["code"],
                fault["priority"],
                fault["message"]
            )

    def _write_row(self, timestamp, decoded, fault_code, priority, message):
        row = [
            timestamp,
            decoded.get("source", ""),
            decoded.get("parameter", ""),
            decoded.get("speed", ""),
            decoded.get("rpm", ""),
            decoded.get("engine_temp", ""),
            decoded.get("battery_voltage", ""),
            decoded.get("battery_current", ""),
            decoded.get("battery_temp", ""),
            decoded.get("brake_status", ""),
            decoded.get("brake_text", ""),
            fault_code,
            priority,
            message
        ]

        with open(self.filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)