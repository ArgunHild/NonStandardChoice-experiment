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
    NAME_IN_URL = 'Learning_stage'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 8
    
    Round_length = 60 #TODO: adjust time 
    Timer_text = "Time left to complete this round:" 
    
    # Game instruction path
    Instructions_path = "_templates/global/Instructions.html"
    
    # Games paths
    Emotion_recognition_template = "_templates/global/Task_templates/Emotion.html"
    Quiz_temlpate_path = "_templates/global/Task_templates/Quiz.html"
    Math_template_path = "_templates/global/Task_templates/Math.html"
    Spot_the_difference_template_path = "_templates/global/Task_templates/Spot.html"
    Spot_the_difference_template_path_2 = "_templates/global/Task_templates/Spot_2.html"
    
    
    # Task instruction paths
    Math_instructions = "_templates/global/Task_instructions/Math.html"
    Emotion_instructions = "_templates/global/Task_instructions/Emotion.html"
    Quiz_instructions = "_templates/global/Task_instructions/Quiz.html"
    Spot_the_difference_instructions = "_templates/global/Task_instructions/Spot.html"
        
    Bonus_1 = 0.5 #TODO: adjust the bonus for practice stage. Make sure participant knows about the bonus in the instructions.
    
    Bonus_cutoffs = {
        'Quiz': 1, #TODO: adjust these
        'Emotion': 1,
        'Math': 1,
        'Spot': 1,
    }

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    task_names = ['Quiz', 'Emotion', 'Math', 'Spot']
    for p in subsession.get_players():
        task_order = random.sample(task_names, len(task_names))
        task_order += random.sample(task_names, len(task_names))  # repeat for round 5–8
        p.participant.vars['task_order'] = task_order



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
    
    def current_task(self):
        return self.participant.vars['task_order'][self.round_number - 1]

# PAGES
class Instruction_Page(Page):
    pass

class TaskPage(Page):
    
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        task = player.current_task()
        suffix = '' if player.round_number <= 4 else '_2'
        return [task + suffix]


    @staticmethod
    def vars_for_template(player: Player):
        return {
            'task_name': player.current_task(),
            'round_type': 'trial' if player.round_number <= 4 else 'main'
        }

    @staticmethod
    def js_vars(player: Player):
        task = player.current_task()
        suffix = '' if player.round_number <= 4 else '_2'
        return {'field_name': task + suffix, 'trial': 'trial' if suffix == '' else 'trial2'}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        task = player.current_task()
        suffix = '' if player.round_number <= 4 else '_2'
        field = task + suffix
        setattr(player, field, getattr(player, field))  # Value already stored by the form

    @staticmethod
    def vars_for_template(player: Player):
        task = player.current_task()
        suffix = '' if player.round_number <= 4 else '_2'
        return {
            'task_template': f"Task_templates/{task}.html",
            'instructions_template': f"Task_instructions/{task}.html",
            'task_name': task + suffix
        }


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
            'Spot_2': player.Spot_2
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

page_sequence = [Instruction_Page, TaskPage]

