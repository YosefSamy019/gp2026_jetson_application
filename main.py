import mcal.cache as cache
import mcal.logs as logs
import mcal.serial_comm as serial_comm
import mcal.wifi as wifi

import network.mcu_network_handler as mcu_network_handler
import network.cloud_network_handler as cloud_network_handler
import network.violation_network_handler as violation_network_handler
import models.models_init as models_init
import app.app as app
from hal import speaker as speaker


def main():
    logs.clear_logs()
    logs.add_log("Initializing...", logs.LogLevel.INFO)

    wifi.init()

    cache.init_cache()
    serial_comm.init()
    speaker.init()

    mcu_network_handler.init()
    cloud_network_handler.init()
    violation_network_handler.init()

    models_init.models_init()

    logs.add_log("Running App...", logs.LogLevel.INFO)

    # Run app in main threads
    app.app_run()


if __name__ == "__main__":
    main()
