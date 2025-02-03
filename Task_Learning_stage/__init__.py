from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Learning_stage'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    Round_length = 3600 #TODO: adjust round length to 60
    Timer_text = "Time left to complete this round:" 
    
    # Game instruction path
    Instructions_path = "_templates/global/Instructions.html"
    
    # Games paths
    Emotion_recognition_template = "_templates/global/Task_templates/Emotion.html"
    Quiz_temlpate_path = "_templates/global/Task_templates/Quiz.html"
    Math_template_path = "_templates/global/Task_templates/Math.html"
    Spot_the_difference_template_path = "_templates/global/Task_templates/Spot_2.html"
    
    
    # Task instruction paths
    Math_instructions = "_templates/global/Task_instructions/Math.html"
    Emotion_instructions = "_templates/global/Task_instructions/Emotion.html"
    Quiz_instructions = "_templates/global/Task_instructions/Quiz.html"
    Spot_the_difference_instructions = "_templates/global/Task_instructions/Spot.html"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Quiz = models.IntegerField(initial=0) #correct answers
    Emotion = models.IntegerField(initial=0) #correct answers
    Math = models.IntegerField(initial=0) #correct answers
    Math_Attempts = models.IntegerField(initial=0) #correct answers
    Spot = models.IntegerField(initial=0) #correct answers


# PAGES
class Quiz_instructions(Page):
    pass
class Emotion_instructions(Page):
    pass
class Math_instructions(Page):
    pass
class Spot_instructions(Page):
    pass


class Quiz(Page):
    form_model = 'player'
    form_fields = ['Quiz'] 
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = {
            'hidden_fields': [],
        }
        
        # Add or modify variables specific to ExtendedPage
        for _ in ['Quiz']:
            variables['hidden_fields'].append(_)
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return {'field_name': 'Quiz',
                'type': 'trial'} 
    
class Emotion(Page):
    form_model = 'player'
    form_fields = ['Emotion'] 
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = {
            'hidden_fields': [],
        }
        
        # Add or modify variables specific to ExtendedPage
        for _ in ['Emotion']:
            variables['hidden_fields'].append(_)
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return {'field_name': 'Emotion',
                'type': 'trial'} 
        
class Math(Page):
    form_model = 'player'
    form_fields = ['Math', 'Math_Attempts'] 
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = {
            'hidden_fields': [],
        }
        
        # Add or modify variables specific to ExtendedPage
        for _ in ['Math', 'Math_Attempts']:
            variables['hidden_fields'].append(_)
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return {'field_name': 'Math',} 
        
class Spot(Page):
    form_model = 'player'
    form_fields = ['Spot'] 
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = {
            'hidden_fields': [],
        }
        
        # Add or modify variables specific to ExtendedPage
        for _ in ['Spot']:
            variables['hidden_fields'].append(_)
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return {'field_name': 'Spot',
                } 


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        variables = {
            'hidden_fields': [],
            'Quiz': player.Quiz,
            'Emotion': player.Emotion,
            'Math': player.Math,
            'Spot': player.Spot,
        }
        

        return variables
    

# Page sequence
#TODO: to randomize need to redo the pages to page 1 page 2 etc and choose the instructions and games within those pages
page_sequence = [Quiz_instructions, Quiz, Emotion_instructions, Emotion, Math_instructions, Math, Spot_instructions, Spot, Results] 

