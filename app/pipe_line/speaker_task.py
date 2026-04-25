import random

from mcal import logs
import app.pipe_line.signals as signals
from hal import speaker as speaker
import time
import json
import app.look_up_keys as look_up_keys
import app.pipe_line.timing as timing
import constants.assets_manager as assets_manager
from scheduler.task import Task


class SpeakerDetectorTask(Task):
    def __init__(self):
        super().__init__(
            name='SpeakerDetectorTask',
            periodicity=timing.SPEAKER_TASK_SLEEP_TIME
        )

    def start(self):
        self.look_up_table = json.load(open(assets_manager.LOOK_UP_TABLE_PATH))
        self.intents_batch = []

    def update(self):
        cur_intents = signals.speaker_queue.get_all()

        if len(cur_intents) > 0:
            self.intents_batch.extend(cur_intents)

            # Remove the duplicates
            self.intents_batch = list(set(self.intents_batch))

            # Sort them again
            self.intents_batch.sort(key=look_up_keys.get_priority, reverse=False)

        if len(self.intents_batch) > 0:
            intent_to_run = self.intents_batch.pop(-1)  # Pick Most important one

            all_possible_responses = self.look_up_table.get(intent_to_run, [])

            if len(all_possible_responses) > 0:
                random_response = random.choice(all_possible_responses)
                speaker.speaker(str(random_response))
