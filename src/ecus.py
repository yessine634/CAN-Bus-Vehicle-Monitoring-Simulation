import time
import threading

import encoders


class BaseECU(threading.Thread):
    def __init__(self, name, bus, vehicle_model, interval):
        super().__init__()
        self.name = name
        self.bus = bus
        self.vehicle_model = vehicle_model
        self.interval = interval
        self.running = True

    def stop(self):
        self.running = False


class EngineECU(BaseECU):
    def run(self):
        while self.running:
            state = self.vehicle_model.update()

            messages = [
                encoders.encode_engine_speed_rpm(state),
                encoders.encode_engine_temperature(state)
            ]

            for msg in messages:
                self.bus.send(msg)
                print(f"[{self.name}] Sent CAN ID {hex(msg.arbitration_id)}")

            time.sleep(self.interval)


class BatteryECU(BaseECU):
    def run(self):
        while self.running:
            state = self.vehicle_model.update()

            messages = [
                encoders.encode_battery_voltage_current(state),
                encoders.encode_battery_temperature(state)
            ]

            for msg in messages:
                self.bus.send(msg)
                print(f"[{self.name}] Sent CAN ID {hex(msg.arbitration_id)}")

            time.sleep(self.interval)


class BrakeECU(BaseECU):
    def run(self):
        while self.running:
            state = self.vehicle_model.update()

            msg = encoders.encode_brake_status(state)
            self.bus.send(msg)

            print(f"[{self.name}] Sent CAN ID {hex(msg.arbitration_id)}")

            time.sleep(self.interval)