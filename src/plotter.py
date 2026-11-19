import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_column(df, column, title, ylabel, filename):
    clean_df = df[df[column].notna() & (df[column] != "")].copy()

    if clean_df.empty:
        print(f"No data available for {column}")
        return

    clean_df[column] = pd.to_numeric(clean_df[column])

    plt.figure()
    plt.plot(clean_df.index, clean_df[column])
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()


def generate_plots(csv_path="data/can_log.csv", output_dir="plots"):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_path)

    plot_column(
        df,
        "speed",
        "Vehicle Speed vs Time",
        "Speed (km/h)",
        f"{output_dir}/speed_vs_time.png"
    )

    plot_column(
        df,
        "rpm",
        "Engine RPM vs Time",
        "RPM",
        f"{output_dir}/rpm_vs_time.png"
    )

    plot_column(
        df,
        "engine_temp",
        "Engine Temperature vs Time",
        "Temperature (°C)",
        f"{output_dir}/engine_temp_vs_time.png"
    )

    plot_column(
        df,
        "battery_voltage",
        "Battery Voltage vs Time",
        "Voltage (V)",
        f"{output_dir}/battery_voltage_vs_time.png"
    )

    plot_column(
        df,
        "battery_temp",
        "Battery Temperature vs Time",
        "Temperature (°C)",
        f"{output_dir}/battery_temp_vs_time.png"
    )

    fault_df = df[df["fault_code"].notna() & (df["fault_code"] != "")]

    if not fault_df.empty:
        fault_count = fault_df["fault_code"].value_counts()

        plt.figure()
        fault_count.plot(kind="bar")
        plt.title("Fault Count by Type")
        plt.xlabel("Fault Code")
        plt.ylabel("Count")
        plt.grid(True)
        plt.savefig(f"{output_dir}/fault_count.png")
        plt.close()

    else:
        plt.figure()
        plt.text(0.5, 0.5, "No faults detected during this run",
                 ha="center", va="center", transform=plt.gca().transAxes)
        plt.title("Fault Count by Type")
        plt.axis("off")
        plt.savefig(f"{output_dir}/fault_count.png")
        plt.close()

    print("Plots generated successfully")


if __name__ == "__main__":
    generate_plots()
