import random
from dataclasses import dataclass


@dataclass
class VehicleState:
    speed: int
    rpm: int
    engine_temp: int
    battery_voltage: float
    battery_current: int
    battery_temp: int
    brake_status: int


class VehicleModel:
    def __init__(self):
        self.speed = 0
        self.rpm = 900
        self.engine_temp = 75
        self.battery_voltage = 12.6
        self.battery_current = 5
        self.battery_temp = 30
        self.brake_status = 0
        self.tick = 0

    def update(self):
        self.tick += 1

        # Speed slowly increases/decreases
        self.speed += random.randint(-3, 8)
        self.speed = max(0, min(self.speed, 140))

        # RPM depends on speed
        self.rpm = 800 + self.speed * 35 + random.randint(-100, 150)
        self.rpm = max(800, min(self.rpm, 5500))

        # Engine temperature changes based on speed
        if self.speed > 80:
            self.engine_temp += random.randint(0, 2)
        else:
            self.engine_temp += random.randint(-1, 1)

        self.engine_temp = max(70, min(self.engine_temp, 120))

        # Battery current changes randomly
        self.battery_current = random.randint(5, 40)

        # Battery voltage slowly drops
        self.battery_voltage += random.uniform(-0.05, 0.02)
        self.battery_voltage = round(max(10.0, min(self.battery_voltage, 12.8)), 1)

        # Battery temperature depends on current
        if self.battery_current > 25:
            self.battery_temp += random.randint(0, 2)
        else:
            self.battery_temp += random.randint(-1, 1)

        self.battery_temp = max(25, min(self.battery_temp, 60))

        # Brake status
        # 0 = normal, 1 = brake applied, 2 = brake fault
        self.brake_status = random.choices(
            population=[0, 1, 2],
            weights=[75, 20, 5]
        )[0]

        return VehicleState(
            speed=self.speed,
            rpm=self.rpm,
            engine_temp=self.engine_temp,
            battery_voltage=self.battery_voltage,
            battery_current=self.battery_current,
            battery_temp=self.battery_temp,
            brake_status=self.brake_status
        )