from vehicle_model import VehicleModel
import encoders

vehicle = VehicleModel()
state = vehicle.update()

print("Original vehicle state:")
print(state)

messages = [
    encoders.encode_engine_speed_rpm(state),
    encoders.encode_engine_temperature(state),
    encoders.encode_battery_voltage_current(state),
    encoders.encode_battery_temperature(state),
    encoders.encode_brake_status(state)
]

print("\nEncoded CAN messages:")

for msg in messages:
    print(msg)