import pandas as pd


def generate_diagnostic_summary(csv_path="data/can_log.csv"):
    df = pd.read_csv(csv_path, encoding="utf-8")

    print("\n========== DIAGNOSTIC SUMMARY ==========")

    total_messages = len(df)
    print(f"Total logged messages: {total_messages}")

    fault_df = df[df["fault_code"].notna() & (df["fault_code"] != "")]

    print(f"Total faults detected: {len(fault_df)}")

    if not fault_df.empty:
        print("\nFault count by code:")
        print(fault_df["fault_code"].value_counts())

        print("\nFault count by priority:")
        print(fault_df["priority"].value_counts())

    speed_df = df[df["speed"].notna()].copy()
    if not speed_df.empty:
        speed_df["speed"] = pd.to_numeric(speed_df["speed"])
        print(f"\nMaximum speed: {speed_df['speed'].max()} km/h")

    rpm_df = df[df["rpm"].notna()].copy()
    if not rpm_df.empty:
        rpm_df["rpm"] = pd.to_numeric(rpm_df["rpm"])
        print(f"Maximum RPM: {rpm_df['rpm'].max()} RPM")

    engine_temp_df = df[df["engine_temp"].notna()].copy()
    if not engine_temp_df.empty:
        engine_temp_df["engine_temp"] = pd.to_numeric(engine_temp_df["engine_temp"])
        print(f"Maximum engine temperature: {engine_temp_df['engine_temp'].max()} °C")

    battery_voltage_df = df[df["battery_voltage"].notna()].copy()
    if not battery_voltage_df.empty:
        battery_voltage_df["battery_voltage"] = pd.to_numeric(
            battery_voltage_df["battery_voltage"]
        )
        print(f"Minimum battery voltage: {battery_voltage_df['battery_voltage'].min()} V")

    battery_temp_df = df[df["battery_temp"].notna()].copy()
    if not battery_temp_df.empty:
        battery_temp_df["battery_temp"] = pd.to_numeric(battery_temp_df["battery_temp"])
        print(f"Maximum battery temperature: {battery_temp_df['battery_temp'].max()} °C")

    print("========================================")


if __name__ == "__main__":
    generate_diagnostic_summary()