from otree.api import *
import random
#TODO: where to put the wait pages?
doc = '''
n check
- Treatment: which treatment they are assigned to
'''

#%% Functions



class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    
    # Prolific links:
    Completion_redirect = "https://www.wikipedia.org/" #TODO: adjust completion redirect
    Reject_redirect = "https://www.wikipedia.org/" #TODO: adjust reject redirect
    Return_redirect = "https://www.wikipedia.org/" #TODO: adjust return redirect
    
    Instructions_general_path = "_templates/global/Instructions.html"
    
    Comprehension_password = 'MARGUN'

    
class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    players = subsession.get_players()
    
    #TODO: remove this code below. FOr now this is there to allow me to bypass comprehension
    # for p in players:
        
    #     # randomly select one of the 15 bundles to be relevant
    #     selected_rank = random.randint(1, 5) 
    #     selected_difficulty = random.choice(['Easy', 'Medium', 'Difficult']) 
    #     p.participant.Random_bundle = f'{selected_difficulty}_{selected_rank}'  
        
    #     p.participant.vars['Comprehension_passed'] = True
    #     p.participant.vars['Allowed'] = True   
    
    
    
    # Treatment assignment.
    # Randomly decide which treatment will go to the first half
    first_half_treatment = random.choice(['Binary', 'Sequential'])
    second_half_treatment = 'Sequential' if first_half_treatment == 'Binary' else 'Binary'

    # Sort players by ID_in_subsession for consistency
    players_sorted = sorted(players, key=lambda p: p.participant.id_in_session)
    half = len(players_sorted) // 2

    Tr1_counter = 1
    Tr2_counter = 1
    
    for i, p in enumerate(players_sorted):
        if i < half:
            p.participant.Treatment = first_half_treatment
            p.participant.ID_in_Treatment = Tr1_counter # Assign ID in treatment group
            Tr1_counter += 1
        else:
            p.participant.Treatment = second_half_treatment
            p.participant.ID_in_Treatment = Tr2_counter # Assign ID in treatment group
            Tr2_counter += 1

            
    
    #TODO: remove this code below. FOr now this is there to allow me to bypass comprehension
    # for debugging purposes, remove this code below
    # for p in players:
    #     p.participant.Treatment = 'Sequential'
    
    
    
    # GROUP ASSIGNMENT
    treatment1_players = [p for p in players if p.participant.Treatment == 'Binary']
    treatment2_players = [p for p in players if p.participant.Treatment == 'Sequential']
    
    
    def assign_groups(player_list):
        #TODO: check that treatment assignment works well
        
        '''
	    1. Each player is assigned randomly an id from 1 till N (session size//2 - given 2 mechanisms). 
	    2. For the first 5 participants, each player is in a group with the other 4 participants. for the remaining players, their choices have no bearing on the first 5 players, but the first 5 players choies affect the available bundles of these players. (Remember that group id assignment is random.)
        '''
               
    def assign_groups(player_list):
        group_ids = [p.participant.id_in_session for p in player_list]  # session-wide IDs

        for player in player_list:
            player_id = player.participant.ID_in_Treatment
            player_id = ((player_id - 1) % 5) + 1
            player.participant.ID_in_Group = player_id

            # Group is everyone else’s id_in_session
            player.participant.Group = [p.participant.id_in_session for p in player_list if p != player]

            
    # Assign groups within each treatment
    assign_groups(treatment1_players)
    assign_groups(treatment2_players)
    
    # Initializing statuses
    for player in subsession.get_players():
        player.participant.Allowed = True
        player.participant.Comprehension_passed = False 
        
    
    

    

class Group(BaseGroup):
    pass

class Player(BasePlayer):      
    # Demographics
    prolific_id = models.StringField(default=str("None")) #prolific id, will be fetched automatically.
    age = models.IntegerField(blank=True, #TODO: remove blank=True
                                label="Age", min=18, max=100)
    gender = models.StringField(blank=True, #TODO: remove blank=True
                                label='Gender at birth',
                                choices=['Male', 'Female', 'Other/Prefer not to say'], widget=widgets.RadioSelect)
    education = models.StringField(blank=True, #TODO: remove blank=True
                                label = 'Education level',
                                   choices=['Haven’t graduated high school','GED','High school graduate','Bachelors','Masters','Professional degree (JD, MD, MBA)','Doctorate', 'Other'], widget=widgets.RadioSelect) 
    # education = models.StringField(label = 'Education level',
    #                                choices=['High school or lower','Bachelors degree','Masters degree','PhD','Other'], widget=widgets.RadioSelect) 
    
    employment = models.StringField(blank=True, #TODO: remove blank=True
                                label='Employment status',
                                    choices=['Employed full-time', 'Employed part-time', 'Self-employed', 'Out of work, or seeking work',
                                             'Student', 'Out of labor force (e.g. retired or parent raising one or more children)'], widget=widgets.RadioSelect)
    
    income = models.StringField(blank=True, #TODO: remove blank=True
                                label='Approximately, what was your <strong>total household income</strong> in the last year, before taxes?',
                            choices=['$0-$10.000', '$10.000-$20.000','$20.000-$30.000','$30.000-$40.000','$40.000-$50.000','$50.000-$60.000',
                                     '$50.000-$75.000', '$75.000-$100.000', '$100.000-$150.000', '$150.000-$200.000', '$200.000+', 'Prefer not to answer',
                                     ],)
    # Data quality. 
    #browser used by the participant This variable is saved in the demographics page.
    browser = models.StringField(blank=True) 
    # logs how often user clicked out of the page #TODO: ensure that this is added to all the pages
    blur_event_counts = models.StringField(initial=0, blank=True) 
    
    
    
    # 'Comprehension and attention checks'
    # Comprehension_password = models.StringField(blank=False,
    #                                     label='Password')
    # #whether the player got the comprehension questions rigt at the first try
    # Comprehension_1 = models.BooleanField(initial=True) 
    # #In the first comprehension check, the questions the player has answered wrong are stored as a string below.
    # Comprehension_wrong_answers = models.StringField(initial='') 
    # Comprehension_wrong_answers_2 = models.StringField(initial='') 
    # Comprehension_2 = models.BooleanField(initial=True) 
    
    # Comprehension_question_1 = models.BooleanField(choices=[
    #         [True,'Twice'], # Correct answer here
    #         [False, 'Once'],
    #         [False, 'Three times'],],
    #     initial=True,
    #     label = 'How many times will you practice each task during the learning stage?',
    #     widget=widgets.RadioSelect)
    # Comprehension_question_2 = models.BooleanField(choices=[
    #     [True, 'Performance in the learning stage'],  
    #     [False, 'Number of tasks shown'],
    #     [False, 'Number of times you click'],],
    #     initial=True,
    #     label = 'What contributes to your final bonus payment?',
    #     widget=widgets.RadioSelect)
    # Comprehension_question_3 = models.BooleanField(choices=[
    #     [True, 'Right before the main stage begins'],
    #     [False, 'At the very end of the experiment'],
    #     [False, 'During the first practice task'],],
    #     initial=True,
    #     label = 'When will you receive more detailed information about the main stage choices?',
    #     widget=widgets.RadioSelect)
    
    # Attention_1 = models.BooleanField(
    # choices=[
    #     [False, 'Lion'],
    #     [False, 'Elephant'],
    #     [True, 'Unicorn'],
    #     [False, 'Giraffe']
    # ],
    #     initial=True,
    #     label='Please select the animal described in the text.',
    #     widget=widgets.RadioSelect
    # )
    
    
    

            
# PAGES
#%% Base Pages
class MyBasePage(Page):
    'MyBasePage contains the functions that are common to all pages'
    form_model = 'player'
    form_fields = ['blur_event_counts']
    
    

    
    @staticmethod
    def vars_for_template(player: Player):
        return {'hidden_fields': ['blur_event_counts'], #fields to be hidden from the participant e.g. browser, blur_event_counts, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_general_path} 

#%% Pages

#Consent, Demographics, Introduction, Comprehension checks and attention check 1
class Consent(Page):   
    @staticmethod
    def before_next_page(player: Player, timeout_happened=False):
        # TODO: in prolific use https://.../room/your_prolific_study?participant_label={{%PROLIFIC_PID%}}
        player.prolific_id = player.participant.label #save prolific id

class Demographics(MyBasePage):
    # TODO: move demographics to the end of the experiment
    extra_fields = ['age', 'gender', 'education', 'employment', 'income','browser'] 
    form_fields = MyBasePage.form_fields + extra_fields

        
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        variables['hidden_fields'].append('browser') 
        return variables
    
class Instructions(MyBasePage):
    pass        




# class Attention_check_1(MyBasePage):
#     extra_fields = ['Attention_1']
#     form_fields = MyBasePage.form_fields + extra_fields    
#     #save at  the participant level
#     @staticmethod   
#     def before_next_page(player: Player, timeout_happened=False):
#         player.participant.vars['Attention_1'] = player.Attention_1


page_sequence = [Consent, Instructions,
                #  Comprehension_check_1, Comprehension_check_2, Comprehension_check_3,
                #  Attention_check_1
                ]