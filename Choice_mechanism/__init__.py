from otree.api import *
import random

doc = '''
This is the main survey app. It contains
1. Main survey 
2. One attention check.
- You can additionally calculate payoffs and save them at a participant field.
'''

class C(BaseConstants):
    NAME_IN_URL = 'Mechanism'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    Round_length = 180 #TODO: adjust round length
    Timer_text = "Time left to complete this round:" 
    
    Instructions_path = "_templates/global/Instructions.html"

    Return_redirect = "https://www.wikipedia.org/" #TODO: adjust redirect
    
    # Task instruction paths
    Math_instructions = "_templates/global/Task_instructions/Math.html"
    Emotion_instructions = "_templates/global/Task_instructions/Emotion.html"
    Quiz_instructions = "_templates/global/Task_instructions/Quiz.html"
    Spot_instructions = "_templates/global/Task_instructions/Spot.html"

    Bonus_max = 'XXX'
    
    
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):   
    # Attention check 2, 1 was in introduction 
    Attention_2 = models.BooleanField(choices=[
            [True, 'I disagree.'],
            [False, 'This is correct.'],
            [False, 'I agree.'],
            [False, 'I agree strongly.'],],
        label= 'A 20 year old man can eat 500kg meat and 2 tons of vegetables in one meal.', widget=widgets.RadioSelect)
            
    # Player answers
    ## Survey
    Favorite_task = models.StringField(choices=['Math','Spot','Quiz','Emotion'],
                                       label="Which task should be offered to you after the mechanism?",
                                   widget=widgets.RadioSelectHorizontal)
    Mechanism_outcome = models.StringField(choices=['Math','Spot','Quiz','Emotion'],
                                       label="What should be the mechanism outcome?",
                                   widget=widgets.RadioSelectHorizontal)
    Switch = models.IntegerField(choices=[[1, 'Yes, I take the offered bundle instead'], [0, 'No, I stick to the bundle decided by the mechanism']],
                                       label="Would you like to switch to the offered bundle?",
                                   widget=widgets.RadioSelect)
    
    Performance_final_task = models.IntegerField(min=0, max=100)
    Performance_final_task_Attempts = models.IntegerField(blank=True, min=0, max=100)
    

 
 #%% Base Pages
class MyBasePage(Page):
    'MyBasePage contains the functions that are common to all pages'
    form_model = 'player'
    form_fields = []
    
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.Allowed 
    
    @staticmethod
    def vars_for_template(player: Player):
        return {'hidden_fields': [], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path} 
  
# Pages
class Attributes(MyBasePage):
    extra_fields = ['Favorite_task'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        variables['Treatment'] = player.participant.Treatment
        return variables




class Mechanism(MyBasePage):
    extra_fields = ['Mechanism_outcome'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        variables['Treatment'] = player.participant.Treatment
        return variables
    
    
class ChosenBundleExplanation_offer(MyBasePage):
    extra_fields = ['Switch'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        variables['MechanismOutcome'] = player.Mechanism_outcome
        variables['Game_Instructions_path'] = f'_templates/global/Task_instructions/{player.Mechanism_outcome}.html'
        variables['Favorite_bundle'] = f'_templates/global/Task_instructions/{player.Mechanism_outcome}.html'
        variables['Offered_bundle'] = f'{player.Favorite_task}'
        return variables
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.Switch == 1:
            player.participant.Final_bundle = player.Favorite_task
        elif player.Switch == 0:
            player.participant.Final_bundle = player.Mechanism_outcome
            
        print(player.participant.Final_bundle)
    
    
    
class ChosenBundleExplanation(MyBasePage):
    extra_fields = [] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        variables['Final_bundle'] = player.participant.Final_bundle
        variables['Game_Instructions_path'] = f'_templates/global/Task_instructions/{player.participant.Final_bundle}.html'
        return variables
    
class ChosenBundlePlay(MyBasePage):
    extra_fields = ['Performance_final_task', 'Performance_final_task_Attempts'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    timeout_seconds = C.Round_length
    timer_text = C.Timer_text
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        variables['MechanismOutcome'] = player.participant.Final_bundle
        
        variables['MechanismOutcome_Template'] = f'_templates/global/Task_templates/{player.participant.Final_bundle}.html'
        return variables
    
    @staticmethod
    def js_vars(player):
        return dict(
            field_name = 'Performance_final_task',
            
        )
        
class Results(MyBasePage):
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Result'] = player.Performance_final_task
        
        return variables


class Attention_check_2(MyBasePage):         
    extra_fields = ['Attention_2']
    form_fields = MyBasePage.form_fields + extra_fields
    
    def before_next_page(player: Player, timeout_happened=False):
        if (not player.Attention_2 and not player.participant.vars['Attention_1']):
            player.participant.vars['Allowed'] = False
            player.participant.vars['Attention_passed'] = False
  
page_sequence = [
    Attributes,
    Mechanism,
    ChosenBundleExplanation_offer,
    ChosenBundleExplanation,
    ChosenBundlePlay,
    Results,
    Attention_check_2,
    ]
