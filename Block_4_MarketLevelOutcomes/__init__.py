from otree.api import *


doc = '''
Third app - Exit survey.
'''

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
    NAME_IN_URL = 'Market_Level_Outcomes'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    Instructions_path = "_templates/global/Instructions.html"

    Return_redirect = "https://www.wikipedia.org/" #TODO: adjust return redirect
    
    


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    MarketLevel_1 = models.StringField(initial='', blank=True)
    MarketLevel_2 = models.StringField(initial='', blank=True)
    



#%% Base Pages
class MyBasePage(Page):
    'MyBasePage contains the functions that are common to all pages'
    form_model = 'player'
    form_fields = []
    
    @staticmethod
    def vars_for_template(player: Player):
        return {'hidden_fields': ['bullshit'], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path} 

#%% Pages

class Exit_survey(MyBasePage):
    extra_fields = ['Exit_1','Exit_2','Exit_3']
    form_fields = MyBasePage.form_fields + extra_fields
    
# Only for pilot
class MarketLevel_1(MyBasePage):
    extra_fields = ['MarketLevel_1']
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        
        Final_bundle = player.participant.Final_bundle
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
            
        variables['Final_bundle'] = final_bundle
        
        Random_bundle = player.participant.vars['Random_bundle'].split('_')
        
        round_number = Random_bundle
        
        variables['round_number'] = int(round_number[1])
        
        if round_number[0] == 'Difficult':
            variables['round_number'] += 10
        elif round_number[0] == 'Medium':
            variables['round_number'] += 5
        
        return variables
        
page_sequence = [MarketLevel_1,  ]
