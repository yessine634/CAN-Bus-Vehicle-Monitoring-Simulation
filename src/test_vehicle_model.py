from vehicle_model import VehicleModel

vehicle = VehicleModel()

for i in range(10):
    state = vehicle.update()
    print(f"Sample {i + 1}: {state}")