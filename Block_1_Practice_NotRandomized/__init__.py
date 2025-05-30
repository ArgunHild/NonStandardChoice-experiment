from otree.api import *
import random


doc = """
Your app description
"""

#TODO: create two rounds of trial stages each 180 seconds
#TODO: create more games for the emotion recognition
#TODO randomize the order of mechanism and attribute-survey.
# TODO: market level outcomes app: Add WTA questions for 1 out of 15 outcomes (for now)

class C(BaseConstants):
    NAME_IN_URL = 'Practice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    Round_length = 60 #TODO: adjust time 
    Timer_text = "Time left to complete this round:" 
    
    # Game instruction path
    Instructions_path = "_templates/global/Instructions.html"
    
    # Games paths
    Emotion_recognition_template = "_templates/global/Task_templates/Emotion.html"
    Quiz_template_path = "_templates/global/Task_templates/Quiz.html"
    Math_template_path = "_templates/global/Task_templates/Math.html"
    Spot_the_difference_template_path = "_templates/global/Task_templates/Spot.html"
    Spot_the_difference_template_path_2 = "_templates/global/Task_templates/Spot_2.html"

    
    # Task instruction paths
    Math_instructions = "_templates/global/Task_instructions/Math.html"
    Emotion_instructions = "_templates/global/Task_instructions/Emotion.html"
    Quiz_instructions = "_templates/global/Task_instructions/Quiz.html"
    Spot_the_difference_instructions = "_templates/global/Task_instructions/Spot.html"
        
    Bonus_1 = 0.5 #TODO: adjust the bonus for practice stage. Make sure participant knows about the bonus in the instructions.
    

        # Max achievable scores (hardcoded for now)
    Max_Math = 24         # TODO: Make dynamic based on actual task settings
    Max_Quiz = 30         # TODO: Make dynamic based on actual task settings
    Max_Spot = 10         # TODO: Make dynamic based on actual task settings
    Max_Emotion = 10      # TODO: Make dynamic based on actual task settings

    Bonus_cutoffs = {
        'Quiz': 1, #TODO: adjust these
        'Emotion': 1,
        'Math': 1,
        'Spot': 1,
    }

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
    
    Bonus_Quiz = models.FloatField(initial=0)
    Bonus_Emotion = models.FloatField(initial=0)
    Bonus_Math = models.FloatField(initial=0)
    Bonus_Spot = models.FloatField(initial=0)

    Quiz_2 = models.IntegerField(initial=0) #correct answers
    Emotion_2 = models.IntegerField(initial=0) #correct answers
    Math_2 = models.IntegerField(initial=0) #correct answers
    Math_Attempts_2 = models.IntegerField(initial=0) #correct answers
    Spot_2 = models.IntegerField(initial=0) #correct answers
    
    Bonus_Quiz_2 = models.FloatField(initial=0)
    Bonus_Emotion_2 = models.FloatField(initial=0)
    Bonus_Math_2 = models.FloatField(initial=0)
    Bonus_Spot_2 = models.FloatField(initial=0)

# PAGES
class Quiz_instructions(Page):
    pass
class Emotion_instructions(Page):
    pass
class Math_instructions(Page):
    pass
class Spot_instructions(Page):
    pass

class Quiz_instructions_2(Page):
    pass
class Emotion_instructions_2(Page):
    pass
class Math_instructions_2(Page):
    pass
class Spot_instructions_2(Page):
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
                'trial': 'trial'} 
        
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
                'trial': 'trial'}  
class Quiz_2(Page):
    form_model = 'player'
    form_fields = ['Quiz_2'] 
    
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
        return {'field_name': 'Quiz_2',
                'type': 'trial2'} 
    
class Emotion_2(Page):
    form_model = 'player'
    form_fields = ['Emotion_2'] 
    
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
        return {'field_name': 'Emotion_2',
                'trial': 'trial2'} 
        
class Math_2(Page):
    form_model = 'player'
    form_fields = ['Math_2', 'Math_Attempts'] 
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = {
            'hidden_fields': [],
        }
        
        # Add or modify variables specific to ExtendedPage
        for _ in ['Math_2', 'Math_Attempts']:
            variables['hidden_fields'].append(_)
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return {'field_name': 'Math_2',} 
        
class Spot_2(Page):
    form_model = 'player'
    form_fields = ['Spot_2'] 
    
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
        return {'field_name': 'Spot_2',
                'trial': 'trial2'}  


class Practice_Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        'calculate bonuses'
        for game in ['Quiz', 'Emotion', 'Math', 'Spot']:
            if getattr(player, game) >= C.Bonus_cutoffs[game]:
                setattr(player, f'Bonus_{game}', C.Bonus_1)
            else:
                setattr(player, f'Bonus_{game}', 0)
        
        player.participant.Bonus_1 = sum([getattr(player, f'Bonus_{game}') for game in ['Quiz', 'Emotion', 'Math', 'Spot']])
        
        variables = {
            'hidden_fields': [],
            'Quiz_1': player.Quiz,
            'Emotion_1': player.Emotion,
            'Math_1': player.Math,
            'Spot_1': player.Spot,
            'Quiz_2': player.Quiz_2,
            'Emotion_2': player.Emotion_2,
            'Math_2': player.Math_2,
            'Spot_2': player.Spot_2,

            'Max_Quiz': C.Max_Quiz,
            'Max_Emotion': C.Max_Emotion,
            'Max_Math': C.Max_Math,
            'Max_Spot': C.Max_Spot,
            #
            # 'We do not display bonuses at this stage to avoid any sort of wealth effects.'
            # 'QuizBonus': player.Bonus_Quiz + player.Bonus_Quiz_2,
            # 'EmotionBonus': player.Bonus_Emotion + player.Bonus_Emotion_2,
            # 'MathBonus': player.Bonus_Math+ player.Bonus_Math_2,
            # 'SpotBonus': player.Bonus_Spot+ player.Bonus_Spot_2,
            # 'Bonus_1': player.participant.Bonus_1
        }

        return variables
    


# Page sequence

# page_sequence = [Spot_instructions, Spot,
#                  Spot_instructions_2, Spot_2,
#                  Practice_Results] 
#TODO: uncomment below
page_sequence = [Quiz_instructions, Quiz, Emotion_instructions, Emotion, Math_instructions, Math, Spot_instructions, Spot,
                Quiz_instructions_2, Quiz_2, Emotion_instructions_2, Emotion_2, Math_instructions_2, Math_2, Spot_instructions_2, Spot_2,
                Practice_Results] 

