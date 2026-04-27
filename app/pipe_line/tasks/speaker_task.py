import random

import app.pipe_line.signals as signals
from hal import speaker as speaker
import json
from constants import look_up_keys
import constants.assets_manager as assets_manager
from scheduler.task import Task


class SpeakerDetectorTask(Task):
    def __init__(self, name: str, periodicity: float):
        super().__init__(name, periodicity)

        self.look_up_table = json.load(open(assets_manager.LOOK_UP_TABLE_PATH))
        self.intents_batch = []

    def update(self):
        cur_intents = signals.speaker_queue.pop_all()

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
                self._play(random_response)

    def _play(self, text):
        text = str(text)

        # Replace Name
        face_recognizer_out = signals.face_clipper_recognizer_queue.get_last()
        if face_recognizer_out is not None and face_recognizer_out.driver_name is not None:
            text = text.replace('#NAME', face_recognizer_out.driver_name)
        else:
            text = text.replace('#NAME', '')

        speaker.speaker(text)
