from otree.api import *
from . import *
import random

class PlayerBot(Bot):

    def play_round(self):
        # Assuming the bot is allowed to view the page
        
        # Provide responses for the exit survey
        yield Exit_survey, {
            'Exit_1': 'This was a rewarding experience.',
            'Exit_2': 'The instructions were clear.',
            'Exit_3': 'No difficulties encountered.'
        }

        # Provide responses for the pilot survey (only if it's a pilot test)
        yield Pilot, {
            'Pilot_1': 'Everything was straightforward.',
            'Pilot_2': 'The timing of the tasks was appropriate.',
            'Pilot_3': 'I found the tasks engaging.',
            'Pilot_4': 'There were no technical issues.',
            'Pilot_5': 'The layout was visually appealing.',
            'Pilot_6': 'The overall pace was good.'
        }

    # Optionally define any helper methods here if needed for complex operations
