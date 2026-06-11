import threading

import decoders
from fault_detector import detect_faults
from logger import CANLogger


class DashboardECU(threading.Thread):
    def __init__(self, bus):
        super().__init__()
        self.bus = bus
        self.running = True
        self.logger = CANLogger()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            msg = self.bus.recv(timeout=1.0)

            if msg is None:
                continue

            decoded = decoders.decode_message(msg)
            faults = detect_faults(decoded)

            print("[Dashboard]", decoded)

            for fault in faults:
                print(
                    f"[{fault['priority']} WARNING] "
                    f"{fault['code']} - {fault['message']}"
                )

            self.logger.log(decoded, faults)