import can
import can_ids


def encode_engine_speed_rpm(state):
    rpm_high = (state.rpm >> 8) & 0xFF
    rpm_low = state.rpm & 0xFF

    return can.Message(
        arbitration_id=can_ids.ENGINE_SPEED_RPM,
        data=[state.speed, rpm_high, rpm_low],
        is_extended_id=False
    )


def encode_engine_temperature(state):
    return can.Message(
        arbitration_id=can_ids.ENGINE_TEMPERATURE,
        data=[state.engine_temp],
        is_extended_id=False
    )


def encode_battery_voltage_current(state):
    voltage_scaled = int(state.battery_voltage * 10)

    return can.Message(
        arbitration_id=can_ids.BATTERY_VOLTAGE_CURRENT,
        data=[voltage_scaled, state.battery_current],
        is_extended_id=False
    )


def encode_battery_temperature(state):
    return can.Message(
        arbitration_id=can_ids.BATTERY_TEMPERATURE,
        data=[state.battery_temp],
        is_extended_id=False
    )


def encode_brake_status(state):
    return can.Message(
        arbitration_id=can_ids.BRAKE_STATUS,
        data=[state.brake_status],
        is_extended_id=False
    )