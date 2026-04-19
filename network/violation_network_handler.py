import time
from app.pipe_line import timing
from app.pipe_line import signals
from mcal import logs
from scheduler import scheduler
import mcal.wifi as wifi


# Code
def init():
    scheduler.create_task(violation_network_session_task, "violation_network_session_task")


def violation_network_session_task():
    violations_batch = []

    while True:
        try:
            # Read queue
            violations_batch.extend(signals.violations_queue.get_all())

            # Send
            if len(violations_batch) > 0:
                violation_sample = violations_batch.pop(0)

                # Send to server
                violation_class = violation_sample['class']
                violation_image = violation_sample['image']
                violation_time = violation_sample['time']

                logs.add_log(f"Violation Send: {violation_class}, {violation_time}", logs.LogLevel.WARNING)

                # In case of failure, restore the sample
                if False:
                    violations_batch.append(violation_sample)

        except Exception as e:
            logs.add_log(f"violation_network_session_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.VIOLATION_NETWORK_TASK_SLEEP_TIME)
