import random

from mcal import logs
import app.pipe_line.signals as signals
from hal import speaker as speaker
import time
import json
import app.look_up_keys as look_up_keys
import app.pipe_line.timing as timing
import constants.assets_manager as assets_manager


def speaker_task():
    look_up_table = json.load(open(assets_manager.LOOK_UP_TABLE_PATH))
    intents_batch = []

    while True:
        try:

            cur_intents = signals.speaker_queue.get_all()

            if len(cur_intents) > 0:
                intents_batch.extend(cur_intents)

                # Remove the duplicates
                intents_batch = list(set(intents_batch))

                # Sort them again
                intents_batch.sort(key=look_up_keys.get_priority, reverse=False)

            if len(intents_batch) > 0:
                intent_to_run = intents_batch.pop(-1)  # Pick Most important one

                all_possible_responses = look_up_table.get(intent_to_run, [])

                if len(all_possible_responses) > 0:
                    random_response = random.choice(all_possible_responses)
                    speaker.speaker(str(random_response))

        except Exception as e:
            logs.add_log(f"speaker_task: error {e}", logs.LogLevel.ERROR)

        time.sleep(timing.SPEAKER_TASK_SLEEP_TIME)
