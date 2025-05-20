from otree.api import *
import random


doc = """
Your app description
"""

#TODO: create two rounds of trial stages each 180 seconds
#TODO: create more games for the emotion recognition

def get_icon(task, level):
    """
    Returns the icon for a given task and difficulty level.
    
    Args:
        task (str): The task type. Must be one of ['Math', 'Spot', 'Quiz', 'Emotion'].
        level (int): The difficulty level of the task. Must be one of [1, 2, 3].
    
    Returns:
        str: The corresponding icon.
    """
    icons = {
        "Math": "🔢",
        "Spot": "🔍",
        "Quiz": "📚",
        "Emotion": "😃"
    }
    return f"{icons[task]}<sub>{level}</sub>"


class C(BaseConstants):
    NAME_IN_URL = 'Play'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    Round_length = 18000 #TODO: adjust round length to 180?
    Timer_text = "Time left to complete this round:" 
    
    Instructions_path = "_templates/global/Instructions.html"

    Return_redirect = "https://www.wikipedia.org/" #TODO: adjust redirect
    
    # Task instruction paths
    Emotion_template = "_templates/global/Task_templates/Emotion.html"
    Quiz_temlpate = "_templates/global/Task_templates/Quiz.html"
    Math_template = "_templates/global/Task_templates/Math.html"
    Spot_template = "_templates/global/Task_templates/Spot_2.html" 
    # Task instruction paths
    Math_instructions = "_templates/global/Task_instructions/Math.html"
    Emotion_instructions = "_templates/global/Task_instructions/Emotion.html"
    Quiz_instructions = "_templates/global/Task_instructions/Quiz.html"
    Spot_instructions = "_templates/global/Task_instructions/Spot.html"

    Bonus_max = 7.5 #TODO: adjust bonus
    
    # TODO: minimum scores need to be adjusted
    Minimum_scores = {
        "Quiz": {
            1: 5,
            2: 5,
            3: 5
        },
        "Math": {
            1: 5,
            2: 5,
            3: 5,
        },
        "Spot": {
            1: 5,
            2: 5,
            3: 5
        },
        "Emotion": {
            1: 5,
            2: 5,
            3: 5
        }        
    }
    
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Attention_2 = models.IntegerField(min=0, max=100, initial=0)
    
    Game_1_performance = models.IntegerField(min=0, max=100, initial=0)
    Game_2_performance = models.IntegerField(min=0, max=100, initial=0)
    Game_3_performance = models.IntegerField(min=0, max=100, initial=0)
    
    Bonus_2_1 = models.FloatField(min=0, max=100, initial=0)
    Bonus_2_2 = models.FloatField(min=0, max=100, initial=0)
    Bonus_2_3 = models.FloatField(min=0, max=100, initial=0)
    
    Final_bundle = models.StringField(initial='')


# Pages
class MyBasePage(Page):
    'MyBasePage contains the functions that are common to all pages'
    form_model = 'player'
    form_fields = []
    
    @staticmethod
    def vars_for_template(player: Player):
        return {'hidden_fields': [], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path,
                } 
  


class ChosenBundleExplanation(MyBasePage):
    extra_fields = [] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        Final_bundle = player.participant.Final_bundle.strip('"')
        bundle = Final_bundle.split('_')
        
        bundle_1 = get_icon(bundle[0], int(bundle[1]))  
        final_bundle = f'{bundle_1}'
        try: 
            bundle_2 = get_icon(bundle[2], int(bundle[3]))
            final_bundle += f'+{bundle_2}'
        except:
            bundle_2 = False
        try:
            bundle_3 = get_icon(bundle[4], int(bundle[5]))
            final_bundle += f'+{bundle_3}'
        except:
            bundle_3 = False
            
            
        Bundle_text = f'''
            You have been assigned the following bundle: {final_bundle}.
            
            <br><br>
            To earn the bonus of <strong>{C.Bonus_max}€</strong>, you must reach the required minimum score in <strong>each</strong> of the tasks in this bundle. Failing to meet the cutoff in any one task means no bonus will be paid.
            
            <br><br>
            On the next page, you will begin working on your assigned bundle.
        '''

        
        variables['Bundle_text'] = Bundle_text
        def format_bundle_icon(bundle_str):
            clean = bundle_str.strip('"')
            parts = clean.split('_')
            return ' + '.join([get_icon(parts[i], int(parts[i+1])) for i in range(0, len(parts), 2)])

        variables['Final_bundle'] = format_bundle_icon(Final_bundle)
    
        return variables
    

def calculate_bonus(player, field_num):
    assert field_num in [0, 2, 4], "Field number must be 0, 2 or 4"
    
    game_num = field_num // 2 + 1
    
    Final_bundle = player.participant.Final_bundle
    
    task = Final_bundle.split('_')[field_num]
    difficulty = int(Final_bundle.split('_')[field_num+1])
    performance = getattr(player, f'Game_{game_num}_performance')
    
    bonus = 0
    if performance > C.Minimum_scores[task][difficulty]:
        bonus = C.Bonus_max
    
    setattr(player, f'Bonus_2_{game_num}', bonus)
    print(f'Player {player.id_in_group} earned {bonus} for {task} {difficulty}. He scored {performance} and cutoff is {C.Minimum_scores[task][difficulty]}')
    

class Game_1(MyBasePage):
    extra_fields = ['Game_1_performance'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    timeout_seconds, timer_text = C.Round_length, C.Timer_text

    @staticmethod
    def js_vars(player):
        return dict(field_name = 'Game_1_performance',)
        
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        
        num = 0
        
        variables['Task'] = bundle[num]
        variables['Difficulty'] = num+1
        task = bundle[num].strip('"')
        variables['Task_instructions'] = getattr(C, f"{task}_instructions")
        variables['GameTemplate'] = getattr(C, f"{task}_template")
        
        return variables
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_bonus(player, 0)

class Game_2(MyBasePage):
    #TODO: make sure player doesnt see this page if there are only 1 task in his bundle
    extra_fields = ['Game_2_performance'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def is_displayed(player: Player):
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        return len(bundle) > 2
    
    timeout_seconds, timer_text = C.Round_length, C.Timer_text

    @staticmethod
    def js_vars(player):
        return dict(field_name = 'Game_2_performance',)
        
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        
        num = 2
        
        variables['Task'] = bundle[num]
        variables['Difficulty'] = num+1
        task = bundle[num].strip('"')
        variables['Task_instructions'] = getattr(C, f"{task}_instructions")
        variables['GameTemplate'] = getattr(C, f"{task}_template")

        return variables
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_bonus(player, 2)

class Game_3(MyBasePage):
    #TODO: make sure player doesnt see this page if there are only 2 tasks in his bundle
    extra_fields = ['Game_3_performance'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def is_displayed(player: Player):
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        return len(bundle) > 4
    
    timeout_seconds, timer_text = C.Round_length, C.Timer_text

    @staticmethod
    def js_vars(player):
        return dict(field_name = 'Game_3_performance',)
        
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        
        num = 4
        
        variables['Task'] = bundle[num]
        variables['Difficulty'] = num+1
        task = bundle[num].strip('"')
        variables['Task_instructions'] = getattr(C, f"{task}_instructions")
        variables['GameTemplate'] = getattr(C, f"{task}_template")
        return variables
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_bonus(player, 4)


        
class Results(MyBasePage):
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        
        bundle_1 = get_icon(bundle[0], int(bundle[1]))  
        try: 
            bundle_2 = get_icon(bundle[2], int(bundle[3]))
        except:
            bundle_2 = False
        try:
            bundle_3 = get_icon(bundle[4], int(bundle[5]))
        except:
            bundle_3 = False
            
        final_bundle = f'{bundle_1}+{bundle_2}+{bundle_3}'
        
        variables['Final_bundle'] = final_bundle
        #TODO: test this for multiple different bundle sizes i.e. if there are 2 or 1 bundle only
        if bundle_2 and bundle_3:
            bonuses = f'''
            <ol>
            <li> {bundle_1}: {player.Bonus_2_1}€ </li>
            <li> {bundle_2}: {player.Bonus_2_2}€ </li>
            <li> {bundle_3}: {player.Bonus_2_1}€ </li>
            </ol>
            '''
        elif bundle_2:
            bonuses = f'''
            <ol>
            <li> {bundle_1}: {player.Bonus_2_1}€ </li>
            <li> {bundle_2}: {player.Bonus_2_2}€ </li>
            </ol>
            '''
        else:
            bonuses = f'''
            <ol>
            <li> {bundle_1}: {player.Bonus_2_1}€ </li>
            </ol>
            '''
        
        variables['ResultsText'] = f'''
        You have earned the following bonus:
        {bonuses}
        '''
        
        return variables
        
    
        

page_sequence = [ChosenBundleExplanation, Game_1, Game_2, Game_3,
                 Results]
