from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Learning_stage'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    Round_length = 60 
    Timer_text = "Time left to complete this round:" 
    
    # Game instruction path
    Instructions_general_path = "_templates/global/Instructions.html"
    
    # Games paths
    Emotion_recognition_template = "_templates/global/Game_templates/Emotion.html"
    Quiz_template_path = "_templates/global/Game_templates/Quiz.html"
    Math_template_path = "_templates/global/Game_templates/Math.html"
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

    #TODO: no more cutoffs for practice.
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
        task_order += task_order  # repeat for round 5–8
        p.participant.vars['task_order'] = task_order
        # print(f"Task order for participant {p.participant.id_in_session}: {task_order}")



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
    

# Function to get task
def get_task(player: Player, round_number: int):
    task_order = player.participant.vars['task_order']
    task_name = task_order[round_number]
    
    if round_number > 4:
        task_name = task_name + '_2'
    
    return task_name

def get_task_Template(task, round_number):
    if round_number > 4:
        ending = '_2'
    else:
        ending = ''

    template = f"_templates/global/Task_templates/pages/{task}{ending}.html"
    instructions = f"_templates/global/Task_templates/pages/{task}_instructions{ending}.html"
    return template, instructions




# PAGES
class Instruction_1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        task = get_task(player, 1)
        instructions = get_task_Template(task, 1)[1]
        player.participant.vars['task'] = task
        # print(instructions)
        return {
            'Instructions_general_path': instructions,
            'task': task,
        }
        
        
class Instruction_2(Page):
    pass
class Instruction_3(Page):
    pass
class Instruction_4(Page):
    pass

class Instruction_5(Page):
    pass

class Instruction_6(Page):
    pass

class Instruction_7(Page):
    pass

class Instruction_8(Page):
    pass

class Game_1(Page):
    
    
    @staticmethod
    def vars_for_template(player: Player):
        task = get_task(player, 1)
        template, instructions = get_task_Template(task, 1)
        
        return {
            'Instructions_general_path': instructions,
            'task': task,
            'template_path': template,
        }

class Game_2(Page):
    pass
class Game_3(Page):
    pass
class Game_4(Page):
    pass

class Game_5(Page):
    pass

class Game_6(Page):
    pass

class Game_7(Page):
    pass

class Game_8(Page):
    pass

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
            'Quiz': player.Quiz,
            'Emotion': player.Emotion,
            'Math': player.Math,
            'Spot': player.Spot,
            'QuizBonus': player.Bonus_Quiz,
            'EmotionBonus': player.Bonus_Emotion,
            'MathBonus': player.Bonus_Math,
            'SpotBonus': player.Bonus_Spot,
            'Bonus_1': player.participant.Bonus_1
        }

        return variables
    


# Page sequence

page_sequence = [Instruction_1, Game_1, Instruction_2, Game_2, Instruction_3, Game_3, Instruction_4, Game_4,
                 Instruction_5, Game_5, Instruction_6, Game_6, Instruction_7, Game_7, Instruction_8, Practice_Results]

