from . import *
import random

class PlayerBot(Bot):


    def play_round(self):
        case = self.case

        # Assume demographics data is fixed for simplicity
        yield Consent
        yield Demographics, {
            'age': random.randint(18, 70),
            'gender': random.choice(['Male', 'Female', 'Other/Prefer not to say']),
            'education': random.choice(['Haven’t graduated high school','GED','High school graduate','Bachelors','Masters','Professional degree (JD, MD, MBA)','Doctorate']),
            'employment': random.choice(['Employed full-time', 'Student', 'Out of work, or seeking work']),
            'income': random.choice(['$0-$10.000', '$10.000-$20.000', '$20.000-$30.000']),
            'browser': 'Chrome'
        }
        yield Instructions

        yield Comprehension_check_1, {
            'Comprehension_question_1': True,
            'Comprehension_question_2': True,
            'Comprehension_question_3': True
        }
        yield Attention_check_1, {'Attention_1': True}
        



    # Optionally define any helper methods here if needed for complex operations
