import time
import argparse
from pathlib import Path
import can

from vehicle_model import VehicleModel
from ecus import EngineECU, BatteryECU, BrakeECU
from dashboard import DashboardECU
from plotter import generate_plots
from diagnostic_summary import generate_diagnostic_summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, default=15)
    parser.add_argument('--stop-file', type=Path)
    args = parser.parse_args()
    print("Starting CAN Bus Vehicle Monitoring Simulation...\n")

    vehicle = VehicleModel()

    engine_bus = can.Bus(interface="virtual", channel="vehicle_channel")
    battery_bus = can.Bus(interface="virtual", channel="vehicle_channel")
    brake_bus = can.Bus(interface="virtual", channel="vehicle_channel")
    dashboard_bus = can.Bus(interface="virtual", channel="vehicle_channel")

    engine_ecu = EngineECU("Engine ECU", engine_bus, vehicle, 0.5)
    battery_ecu = BatteryECU("Battery ECU", battery_bus, vehicle, 0.8)
    brake_ecu = BrakeECU("Brake ECU", brake_bus, vehicle, 0.7)
    dashboard = DashboardECU(dashboard_bus)

    engine_ecu.start()
    battery_ecu.start()
    brake_ecu.start()
    dashboard.start()

    try:
        simulation_time = max(1, min(args.duration, 300))
        print(f"Simulation running for {simulation_time} seconds...\n")
        deadline = time.monotonic() + simulation_time
        while time.monotonic() < deadline:
            if args.stop_file and args.stop_file.exists():
                break
            time.sleep(0.1)

    finally:
        print("\nStopping simulation...")

        engine_ecu.stop()
        battery_ecu.stop()
        brake_ecu.stop()
        dashboard.stop()

        engine_ecu.join()
        battery_ecu.join()
        brake_ecu.join()
        dashboard.join()

        engine_bus.shutdown()
        battery_bus.shutdown()
        brake_bus.shutdown()
        dashboard_bus.shutdown()

        print("Simulation stopped.")

        print("\nGenerating plots...")
        generate_plots()

        print("\nGenerating diagnostic summary...")
        generate_diagnostic_summary()


if __name__ == "__main__":
    main()
