from otree.api import *
import random
doc = '''
n check
- Treatment: which treatment they are assigned to
'''

#%% Functions



class C(BaseConstants):
    NAME_IN_URL = 'Introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    
    Instructions_general_path = "_templates/global/Instructions.html"
    

    Completion_fee = 5 
    Bonus_max_practice = 4.5
    Bonus_max = 20

    
class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    players = subsession.get_players()
    
    #remove this code below. FOr now this is there to allow me to bypass comprehension
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

            
    
    #remove this code below. FOr now this is there to allow me to bypass comprehension
    # for debugging purposes, remove this code below
    # for p in players:
    #     p.participant.Treatment = 'Sequential'
    
    
    
    # GROUP ASSIGNMENT
    treatment1_players = [p for p in players if p.participant.Treatment == 'Binary']
    treatment2_players = [p for p in players if p.participant.Treatment == 'Sequential']
    
               
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
    prolific_id = models.StringField(default=str("None")) #prolific id, will be fetched automatically.

    # Data quality. 
    #browser used by the participant This variable is saved in the demographics page.
    browser = models.StringField(blank=True) 
    blur_event_counts = models.StringField(initial=0, blank=True) 
    
    
    
    

    
    
    

            
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
        player.prolific_id = player.participant.label #save prolific id


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
                ]