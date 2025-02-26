from otree.api import *
import random
import json

doc = '''

'''

class C(BaseConstants):
    NAME_IN_URL = 'Mechanism'
    PLAYERS_PER_GROUP = 5
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
    
    BUNDLES_EASY = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    BUNDLES_MEDIUM = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    BUNDLES_DIFFICULT = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    
    
    # texts
    CognitiveLoad_text = "<strong>Place the task that is least mentally exhausting at the top. </strong>"
    Engagement_text = "<strong>Place the task that you find most engaging at the top.</strong>"
    ProbSuccess_text = "<strong>Place the task that you find yourself most confident with at the top.</strong>"
    TimeEfficiency_text = "<strong>Place the task that you think takes fewest amount of mouse-clicks at the top.</strong>"
    
    CognitiveLoad_text_2 = "<strong>If a task is mentally exhausting, assign it a lower score. </strong>"
    Engagement_text_2 = "<strong>If a task is engaging, assign it a higher score.</strong>"
    ProbSuccess_text_2 = "<strong>If you feel confident in your ability in the task, assign it a higher score.</strong>"
    TimeEfficiency_text_2 = "<strong>If a task takes few amount of mouse-clicks, assign it a higher score.</strong>"
    
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    #TODO: how do i make sure that grouping happens within treatment level?
    remaining_bundles_easy = models.StringField()
    remaining_bundles_medium = models.StringField()
    remaining_bundles_difficult = models.StringField()

    def initialize_bundles(self):
        """Called at the start of the game to initialize all bundles."""
        self.remaining_bundles_easy = ",".join(C.BUNDLES_EASY)  # Store as a comma-separated string
        self.remaining_bundles_medium = ",".join(C.BUNDLES_MEDIUM)  # Store as a comma-separated string
        self.remaining_bundles_difficult = ",".join(C.BUNDLES_DIFFICULT)  # Store as a comma-separated string

    def update_remaining_bundles(self, chosen_bundle, which_complexity):
        """Removes the chosen bundle from the list."""
        if which_complexity == 'easy':
            bundles = self.remaining_bundles_easy.split(",")
            bundles.remove(chosen_bundle)
            self.remaining_bundles_easy = ",".join(bundles)
        elif which_complexity == 'medium':
            bundles = self.remaining_bundles_medium.split(",")
            bundles.remove(chosen_bundle)
            self.remaining_bundles_medium = ",".join(bundles)
        elif which_complexity == 'difficult':
            bundles = self.remaining_bundles_difficult.split(",")
            bundles.remove(chosen_bundle)
            self.remaining_bundles_difficult = ",".join(bundles)


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
    
    
    ranking_order = models.StringField() 
    cardinality_Dimension_1 = models.IntegerField()
    cardinality_Dimension_2 = models.IntegerField()
    cardinality_Dimension_3 = models.IntegerField()
    cardinality_Dimension_4 = models.IntegerField()
    cardinality_Dimension_5 = models.IntegerField()
    
    
    ranking_order_CognitiveLoad = models.StringField()
    ranking_order_Engagement = models.StringField()
    ranking_order_ProbSuccess = models.StringField()
    ranking_order_TimeEfficiency = models.StringField()
    
    cardinality_Dimension_CognitiveLoad_SpotTheDifference =  models.IntegerField()
    cardinality_Dimension_Engagement_SpotTheDifference =      models.IntegerField()
    cardinality_Dimension_ProbSuccess_SpotTheDifference =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_SpotTheDifference = models.IntegerField()
    
    cardinality_Dimension_CognitiveLoad_Quiz =  models.IntegerField()
    cardinality_Dimension_Engagement_Quiz =      models.IntegerField()
    cardinality_Dimension_ProbSuccess_Quiz =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_Quiz = models.IntegerField()
    
    cardinality_Dimension_CognitiveLoad_MathMemory =  models.IntegerField()
    cardinality_Dimension_Engagement_MathMemory =      models.IntegerField()
    cardinality_Dimension_ProbSuccess_MathMemory =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_MathMemory = models.IntegerField()
    
    cardinality_Dimension_CognitiveLoad_EmotionRecognition =  models.IntegerField()
    cardinality_Dimension_Engagement_EmotionRecognition =      models.IntegerField()
    cardinality_Dimension_ProbSuccess_EmotionRecognition =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_EmotionRecognition = models.IntegerField()
    

 
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
  
#%% Pages
class Attributes_rank(MyBasePage):
    extra_fields = ['ranking_order'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        
        variables['items'] = ["Dimension 1", "Dimension 2", "Dimension 3", "Dimension 4", "Dimension 5"]
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            field_name = 'ranking_order',
        )
    
class Attributes_rank_cardinality(MyBasePage):
    extra_fields = ['cardinality_Dimension_1', 'cardinality_Dimension_2', 'cardinality_Dimension_3',
                    'cardinality_Dimension_4', 'cardinality_Dimension_5'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        
        variables['ranked_items'] = json.loads(player.ranking_order)
        return variables

# Attributes and tasks
## Cognitive load
class Attributes_tasks_Dimension_1(MyBasePage):
    extra_fields = ['ranking_order_CognitiveLoad'] 
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        
        variables['items'] = ["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"]
        variables['DimensionAtHand'] = "CognitiveLoad"
        variables['DimensionText'] = C.CognitiveLoad_text
        
        variables['field_name'] = "ranking_order_CognitiveLoad"
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            field_name = 'ranking_order_CognitiveLoad',
        )
    
class Attributes_tasks_Dimension_1_cardinality(MyBasePage):
    extra_fields = [
        'cardinality_Dimension_CognitiveLoad_SpotTheDifference', 
        'cardinality_Dimension_CognitiveLoad_Quiz',
        'cardinality_Dimension_CognitiveLoad_MathMemory',
        'cardinality_Dimension_CognitiveLoad_EmotionRecognition',
    ] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        ranking_order = player.ranking_order_CognitiveLoad #TODO: make this dynamic for randomizing pages
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "CognitiveLoad"
        variables['DimensionText'] = C.CognitiveLoad_text_2
        
        variables['ranked_items'] = json.loads(ranking_order)
        return variables
    
## Enjoyment
class Attributes_tasks_Dimension_2(MyBasePage):
    extra_fields = ['ranking_order_Engagement'] 
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        
        variables['items'] = ["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"]
        variables['DimensionAtHand'] = "Engagement"
        variables['DimensionText'] = C.Engagement_text
        
        variables['field_name'] = "ranking_order_Engagement"
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            field_name = 'ranking_order_Engagement',
        )
    
class Attributes_tasks_Dimension_2_cardinality(MyBasePage):
    extra_fields = [
        'cardinality_Dimension_Engagement_SpotTheDifference', 
        'cardinality_Dimension_Engagement_Quiz',
        'cardinality_Dimension_Engagement_MathMemory',
        'cardinality_Dimension_Engagement_EmotionRecognition',
    ] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        ranking_order = player.ranking_order_Engagement #TODO: make this dynamic for randomizing pages
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "Engagement"
        variables['DimensionText'] = C.Engagement_text_2
        
        variables['ranked_items'] = json.loads(ranking_order)
        return variables
    
## Probability of success
class Attributes_tasks_Dimension_3(MyBasePage):
    extra_fields = ['ranking_order_ProbSuccess'] 
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        
        variables['items'] = ["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"]
        variables['DimensionAtHand'] = "ProbSuccess"
        variables['DimensionText'] = C.ProbSuccess_text
        
        variables['field_name'] = "ranking_order_ProbSuccess"
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            field_name = 'ranking_order_ProbSuccess',
        )
    
class Attributes_tasks_Dimension_3_cardinality(MyBasePage):
    extra_fields = [
        'cardinality_Dimension_ProbSuccess_SpotTheDifference', 
        'cardinality_Dimension_ProbSuccess_Quiz',
        'cardinality_Dimension_ProbSuccess_MathMemory',
        'cardinality_Dimension_ProbSuccess_EmotionRecognition',
    ] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        ranking_order = player.ranking_order_ProbSuccess #TODO: make this dynamic for randomizing pages
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "TimeFfiency"
        variables['DimensionText'] = C.ProbSuccess_text
        
        variables['ranked_items'] = json.loads(ranking_order)
        return variables
    
## Time efficiency
class Attributes_tasks_Dimension_4(MyBasePage):
    extra_fields = ['ranking_order_TimeEfficiency'] 
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        
        variables['items'] = ["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"]
        variables['DimensionAtHand'] = "TimeEfficiency"
        variables['DimensionText'] = C.TimeEfficiency_text
        
        variables['field_name'] = "ranking_order_TimeEfficiency"
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            field_name = 'ranking_order_TimeEfficiency',
        )
    
class Attributes_tasks_Dimension_4_cardinality(MyBasePage):
    extra_fields = [
        'cardinality_Dimension_TimeEfficiency_SpotTheDifference', 
        'cardinality_Dimension_TimeEfficiency_Quiz',
        'cardinality_Dimension_TimeEfficiency_MathMemory',
        'cardinality_Dimension_TimeEfficiency_EmotionRecognition',
    ] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        ranking_order = player.ranking_order_TimeEfficiency #TODO: make this dynamic for randomizing pages
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "TimeEfficiency"
        variables['DimensionText'] = C.TimeEfficiency_text_2
        
        variables['ranked_items'] = json.loads(ranking_order)
        return variables


#%% # Mechanism pages
'''
Pseudo code:
- There are 7 bundles. 
- each person is in group with gs others.
- each person starts with group_n_rank_X_available_bundles and has rank_X_chosen_bundle.
- Withing each complexity level
    -  For each rank 
        - Mechanism page:
            1. Determine mechanism from the Treatment.
            2. pass to the page: available bundles.
            3. js and css handle how mechanism works
            4. Pass the outcome to the player page and update remaining bundles.
        - WaitPage

'''
class Mechanism(MyBasePage):
    extra_fields = ['Mechanism_outcome'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        if player.participant.Treatment == 'Binary':
            Mechanism = 'Binary'
        elif player.participant.Treatment == 'Sequential':
            Mechanism = 'Sequential'

        # Add or modify variables specific to ExtendedPage
        
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


# TODO: randomize whether mechanism or attributes comes first  
pages_Attributes = [Attributes_rank, Attributes_rank_cardinality, 
                    Attributes_tasks_Dimension_1, Attributes_tasks_Dimension_1_cardinality,
                    Attributes_tasks_Dimension_2, Attributes_tasks_Dimension_2_cardinality,
                    Attributes_tasks_Dimension_3, Attributes_tasks_Dimension_3_cardinality,
                    Attributes_tasks_Dimension_4, Attributes_tasks_Dimension_4_cardinality,
                    ]
pages_mechanism = [Mechanism]
pages_rest = [ChosenBundleExplanation_offer,
                 ChosenBundleExplanation,
                 ChosenBundlePlay,
                 Results,
                 Attention_check_2,
                 ]
#TODO: uncomment the first line to include the attributes pages
page_sequence = pages_Attributes + pages_mechanism + pages_rest
# page_sequence =  pages_mechanism + pages_rest
                
