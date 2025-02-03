from otree.api import *
from . import *
import random

class PlayerBot(Bot):


    def play_round(self):
        # Provide responses for the main survey
        yield MyPage, {'Survey_1': random.choice([1, 2, 3, 4])}

        yield Attention_check_2, {'Attention_2': True}

    # Optionally define any helper methods here if needed for complex operations
