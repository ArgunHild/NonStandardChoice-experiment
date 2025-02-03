from otree.api import *


doc = '''
Third app - Exit survey.
'''

class C(BaseConstants):
    NAME_IN_URL = 'Exit_Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    Instructions_path = "_templates/global/Instructions.html"

    Return_redirect = "https://www.wikipedia.org/" #TODO: adjust return redirect


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Exit survey
    Exit_1 = models.StringField(initial='')
    Exit_2 = models.StringField(initial='')
    Exit_3 = models.StringField(initial='')
    
    #Pilot questions
    Pilot_1 = models.StringField(initial='')
    Pilot_2 = models.StringField(initial='')
    Pilot_3 = models.StringField(initial='')
    Pilot_4 = models.StringField(initial='')
    Pilot_5 = models.StringField(initial='')
    Pilot_6 = models.StringField(initial='')
    


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
        return {'hidden_fields': ['bullshit'], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path} 

#%% Pages
class MyBasePage(MyBasePage):
    'MyBasePage contains the functions that are common to all pages'
    extra_fields = []
    form_fields = MyBasePage.form_fields + extra_fields

    
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.Allowed 
    
    @staticmethod
    def vars_for_template(player: Player):
        return {'hidden_fields': ['bullshit'], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path} 

class Exit_survey(MyBasePage):
    extra_fields = ['Exit_1','Exit_2','Exit_3']
    form_fields = MyBasePage.form_fields + extra_fields
    
# Only for pilot
class Pilot(MyBasePage):
    extra_fields = ['Pilot_1','Pilot_2','Pilot_3','Pilot_4','Pilot_5','Pilot_6']
    form_fields = MyBasePage.form_fields + extra_fields
    
        
page_sequence = [Exit_survey, Pilot]
