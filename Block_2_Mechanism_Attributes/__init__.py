from otree.api import *
import random
import json

doc = '''

'''
# Functions
def return_available_bundles(player, howmany, difficulty):
    """
    Returns a list of unavailable bundles for a player based on the specified difficulty and number of bundles.
    Args:
        player (object): The player object containing participant information.
        howmany (int): The number of unavailable bundles to return. Must be one of [1, 2, 3, 4].
        difficulty (str): The difficulty level of the bundles. Must be one of ['Easy', 'Medium', 'Difficult'].
    Returns:
        list: A list of unavailable bundles based on the specified difficulty and number.
    """
    
    assert difficulty in ['Easy', 'Medium', 'Difficult']
    assert howmany in [1, 2, 3, 4]
    
    group_ids = player.participant.Group  # This contains IDs, not objects
    players_dict = {p.participant.id_in_session: p for p in player.subsession.get_players()}  # Create a lookup dict
        
    unavailable_bundles = []

    # Mapping difficulty to attribute names dynamically
    rank_attributes = {
        'Easy': ['Easy_rank1_choice', 'Easy_rank2_choice', 'Easy_rank3_choice', 'Easy_rank4_choice'],
        'Medium': ['Medium_rank1_choice', 'Medium_rank2_choice', 'Medium_rank3_choice', 'Medium_rank4_choice'],
        'Difficult': ['Difficult_rank1_choice', 'Difficult_rank2_choice', 'Difficult_rank3_choice', 'Difficult_rank4_choice']
    }

    # Get the correct list of attributes based on difficulty
    chosen_ranks = rank_attributes[difficulty]

    # Loop over the range of `howmany` and extract values dynamically
    for x in range(howmany):
        player_obj = players_dict[group_ids[x]]
        unavailable_bundles.append(getattr(player_obj, chosen_ranks[x]))

    if difficulty == 'Easy':
        available = list(C.BUNDLES_EASY.keys())
    elif difficulty == 'Medium':
        available = list(C.BUNDLES_MEDIUM.keys())
    else:
        available = list(C.BUNDLES_DIFFICULT.keys())     
        
    return [x for x in available if x not in unavailable_bundles]

    
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
    
    

    #TODO: have MICHI double check these
    BUNDLES_EASY = {
        "1": {
            "Math_3": "🔢<sub>3</sub>",  # Calculator with 3
            "Spot_1": "🔍<sub>1</sub>",  # Magnifying glass with 1
            "Quiz_1": "📚<sub>1</sub>",  # Books with 1
            "Emotion_1": "😃<sub>1</sub>",  # Smiley face with 1
            "Math_1": "🔢<sub>1</sub>",  # Calculator with 1
            "Emotion_2": "😃<sub>2</sub>",  # Smiley face with 2
            "Quiz_3": "🔍<sub>3</sub>"  # Magnifying glass with 3
        },
        "2": {
            "Math_3": "🔢<sub>3</sub>",
            "Spot_2": "🔍<sub>2</sub>",
            "Quiz_2": "📚<sub>2</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Math_2": "🔢<sub>2</sub>",
            "Emotion_3": "😃<sub>3</sub>",
            "Quiz_1": "🔍<sub>1</sub>"
        },
        "3": {
            "Math_3": "🔢<sub>3</sub>",
            "Spot_3": "🔍<sub>3</sub>",
            "Quiz_3": "📚<sub>3</sub>",
            "Emotion_3": "😃<sub>3</sub>",
            "Quiz_2": "📚<sub>2</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Spot_1": "🔍<sub>1</sub>"
        },
        "4": {
            "Math_3": "🔢<sub>3</sub>",
            "Spot_2": "🔍<sub>2</sub>",
            "Quiz_2": "📚<sub>2</sub>",
            "Emotion_3": "😃<sub>3</sub>",
            "Math_2": "🔢<sub>2</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Spot_3": "📚<sub>3</sub>"
        },
        "5": {
            "Math_3": "🔢<sub>3</sub>",
            "Spot_3": "🔍<sub>3</sub>",
            "Quiz_3": "📚<sub>3</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Math_1": "🔢<sub>1</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Quiz_2": "📚<sub>2</sub>"
        }
    }
        
    BUNDLES_MEDIUM = {
        "1": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_2_Emotion_3": "🔍<sub>2</sub> + 😃<sub>3</sub>",
            "Quiz_2_Emotion_3": "📚<sub>2</sub> + 😃<sub>3</sub>",
            "Emotion_2_Emotion_3": "😃<sub>2</sub> + 😃<sub>3</sub>",
            "Math_2_Emotion_3": "🔢<sub>2</sub> + 😃<sub>3</sub>",
            "Quiz_3_Emotion_3": "📚<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_1_Emotion_3": "🔍<sub>1</sub> + 😃<sub>3</sub>"
        },
        "2": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_3_Emotion_3": "🔍<sub>3</sub> + 😃<sub>3</sub>",
            "Quiz_3_Emotion_3": "📚<sub>3</sub> + 😃<sub>3</sub>",
            "Emotion_3_Quiz_3": "😃<sub>3</sub> + 📚<sub>3</sub>",
            "Math_3_Quiz_3": "🔢<sub>3</sub> + 📚<sub>3</sub>",
            "Emotion_2_Spot_3": "😃<sub>2</sub> + 🔍<sub>3</sub>",
            "Spot_1_Emotion_2": "🔍<sub>1</sub> + 😃<sub>2</sub>"
        },
        "3": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_3_Emotion_3": "🔍<sub>3</sub> + 😃<sub>3</sub>",
            "Quiz_3_Emotion_3": "📚<sub>3</sub> + 😃<sub>3</sub>",
            "Emotion_3_Quiz_3": "😃<sub>3</sub> + 📚<sub>3</sub>",
            "Math_3_Quiz_3": "🔢<sub>3</sub> + 📚<sub>3</sub>",
            "Emotion_2_Spot_3": "😃<sub>2</sub> + 🔍<sub>3</sub>",
            "Spot_1_Emotion_2": "🔍<sub>1</sub> + 😃<sub>2</sub>"
        },
        "4": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_3_Emotion_3": "🔍<sub>3</sub> + 😃<sub>3</sub>",
            "Quiz_3_Emotion_3": "📚<sub>3</sub> + 😃<sub>3</sub>",
            "Emotion_3_Quiz_3": "😃<sub>3</sub> + 📚<sub>3</sub>",
            "Math_3_Quiz_3": "🔢<sub>3</sub> + 📚<sub>3</sub>",
            "Emotion_2_Spot_3": "😃<sub>2</sub> + 🔍<sub>3</sub>",
            "Spot_1_Emotion_2": "🔍<sub>1</sub> + 😃<sub>2</sub>"
        },
        "5": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_3_Emotion_3": "🔍<sub>3</sub> + 😃<sub>3</sub>",
            "Quiz_3_Emotion_3": "📚<sub>3</sub> + 😃<sub>3</sub>",
            "Emotion_3_Quiz_3": "😃<sub>3</sub> + 📚<sub>3</sub>",
            "Math_3_Quiz_3": "🔢<sub>3</sub> + 📚<sub>3</sub>",
            "Emotion_2_Spot_3": "😃<sub>2</sub> + 🔍<sub>3</sub>",
            "Spot_1_Emotion_2": "🔍<sub>1</sub> + 😃<sub>2</sub>"
        }
    }


    
    BUNDLES_HIGH = {
        "1": {
            "Emotion_2_Math_2": "😃<sub>2</sub> + 🔢<sub>2</sub>",
            "Spot_2_Emotion_2": "🔍<sub>2</sub> + 😃<sub>2</sub>",
            "Quiz_1_Emotion_2": "📚<sub>1</sub> + 😃<sub>2</sub>",
            "Emotion_1_Quiz_2": "😃<sub>1</sub> + 📚<sub>2</sub>",
            "Math_1_Emotion_3": "🔢<sub>1</sub> + 😃<sub>3</sub>",
            "Quiz_2_Emotion_3": "📚<sub>2</sub> + 😃<sub>3</sub>",
            "Spot_1_Emotion_2": "🔍<sub>1</sub> + 😃<sub>2</sub>"
        },
        "2": {
            "Math_2_Emotion_2": "🔢<sub>2</sub> + 😃<sub>2</sub>",
            "Spot_2_Emotion_2": "🔍<sub>2</sub> + 😃<sub>2</sub>",
            "Quiz_1_Emotion_2": "📚<sub>1</sub> + 😃<sub>2</sub>",
            "Emotion_1_Quiz_2": "😃<sub>1</sub> + 📚<sub>2</sub>",
            "Math_1_Emotion_3": "🔢<sub>1</sub> + 😃<sub>3</sub>",
            "Quiz_2_Emotion_3": "📚<sub>2</sub> + 😃<sub>3</sub>",
            "Spot_1_Emotion_2": "🔍<sub>1</sub> + 😃<sub>2</sub>"
        },
        "3": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_2_Emotion_3": "🔍<sub>2</sub> + 😃<sub>3</sub>",
            "Quiz_1_Emotion_3": "📚<sub>1</sub> + 😃<sub>3</sub>",
            "Emotion_1_Quiz_3": "😃<sub>1</sub> + 📚<sub>3</sub>",
            "Math_1_Emotion_2": "🔢<sub>1</sub> + 😃<sub>2</sub>",
            "Quiz_2_Emotion_2": "📚<sub>2</sub> + 😃<sub>2</sub>",
            "Spot_1_Emotion_3": "🔍<sub>1</sub> + 😃<sub>3</sub>"
        },
        "4": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_2_Emotion_3": "🔍<sub>2</sub> + 😃<sub>3</sub>",
            "Quiz_1_Emotion_3": "📚<sub>1</sub> + 😃<sub>3</sub>",
            "Emotion_1_Quiz_3": "😃<sub>1</sub> + 📚<sub>3</sub>",
            "Math_1_Emotion_2": "🔢<sub>1</sub> + 😃<sub>2</sub>",
            "Quiz_2_Emotion_2": "📚<sub>2</sub> + 😃<sub>2</sub>",
            "Spot_1_Emotion_3": "🔍<sub>1</sub> + 😃<sub>3</sub>"
        },
        "5": {
            "Math_3_Emotion_3": "🔢<sub>3</sub> + 😃<sub>3</sub>",
            "Spot_2_Emotion_3": "🔍<sub>2</sub> + 😃<sub>3</sub>",
            "Quiz_1_Emotion_3": "📚<sub>1</sub> + 😃<sub>3</sub>",
            "Emotion_1_Quiz_3": "😃<sub>1</sub> + 📚<sub>3</sub>",
            "Math_1_Emotion_2": "🔢<sub>1</sub> + 😃<sub>2</sub>",
            "Quiz_2_Emotion_2": "📚<sub>2</sub> + 😃<sub>2</sub>",
            "Spot_1_Emotion_3": "🔍<sub>1</sub> + 😃<sub>3</sub>"
        }
    }

    
    


    
    
    # texts
    CognitiveLoad_text = "<strong>Place the task that is least mentally exhausting at the top. </strong>"
    Engagement_text = "<strong>Place the task that you find most engaging at the top.</strong>"
    ProbSuccess_text = "<strong>Place the task that you find yourself most confident with at the top.</strong>"
    TimeEfficiency_text = "<strong>Place the task that you think takes fewest amount of mouse-clicks at the top.</strong>"
    
    CognitiveLoad_text_2 = "<strong>If a task is mentally exhausting, assign it a lower score. </strong>"
    Engagement_text_2 = "<strong>If a task is engaging, assign it a higher score.</strong>"
    ProbSuccess_text_2 = "<strong>If you feel confident in your ability in the task, assign it a higher score.</strong>"
    TimeEfficiency_text_2 = "<strong>If a task takes few amount of mouse-clicks, assign it a higher score.</strong>"
    
    Rank_sentence ={
        1: "You are now rank 1. This means that for this round, you get to choose from the set of all available bundles.",
        2: "You are now rank 2. This means that for this round, the set of bundles available in this round is all the bundles minus the bundle the rank 1 player chose.",
        3: "You are now rank 3. This means that for this round, the set of bundles available in this round is all the bundles minus the bundles the rank 1 and rank 2 players chose.",
        4: "You are now rank 4.  This means that for this round, the set of bundles available in this round is all the bundles minus the bundles the ranks 1, 2 and 3 players chose.",
        5: "You are now rank 5.  This means that for this round, the set of bundles available in this round is all the bundles minus the bundles the ranks 1, 2, 3, and 3 players chose.",
    }
    
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
    
    ## Mechanism
    Easy_rank1_choice = models.StringField()
    Easy_rank2_choice = models.StringField()
    Easy_rank3_choice = models.StringField()
    Easy_rank4_choice = models.StringField()
    Easy_rank5_choice = models.StringField()
    
    Medium_rank1_choice = models.StringField()
    Medium_rank2_choice = models.StringField()
    Medium_rank3_choice = models.StringField()
    Medium_rank4_choice = models.StringField()
    Medium_rank5_choice = models.StringField()
    
    Difficult_rank1_choice = models.StringField()
    Difficult_rank2_choice = models.StringField()
    Difficult_rank3_choice = models.StringField()
    Difficult_rank4_choice = models.StringField()
    Difficult_rank5_choice = models.StringField()
    
    
 
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
                'Instructions': C.Instructions_path,
                'MechanismPage': "_templates/global/Mechanism.html",} 
  
#%% Pages
class TreatmentWaitPage(WaitPage):
    pass



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

#TODO: clarify. The order of ranks is not random
#TODO: clarify. The order of difficulty levels is not random first easy then medium then hard.
class Mechanism_Easy_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank1_choice'] 
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = list(C.BUNDLES_EASY["1"].values())
        variables['rank_sentence'] = C.Rank_sentence[1]       
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism = player.participant.Treatment,
            Field_name = 'Easy_rank1_choice',
            AvailableBundles = list(C.BUNDLES_EASY["1"].keys()),
            BundleIcons = C.BUNDLES_EASY
        )
    
    
class Mechanism_Easy_rank2_WaitPage(WaitPage):
    pass                    
    
class Mechanism_Easy_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank2_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        
        variables['AvailableBundles'] = return_available_bundles(player, 1, 'Easy')
        
        variables['Group'] = player.participant.Group
        variables['rank_sentence'] = C.Rank_sentence[2]
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism = player.participant.Treatment,
            Field_name = 'Easy_rank2_choice',
            AvailableBundles = return_available_bundles(player, 1, 'Easy')
        )
        
class Mechanism_Easy_rank3_WaitPage(WaitPage):
    pass

class Mechanism_Easy_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank3_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 2, 'Easy')
        variables['rank_sentence'] = C.Rank_sentence[3]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Easy_rank3_choice',
            AvailableBundles=return_available_bundles(player, 2, 'Easy')
        )

class Mechanism_Easy_rank4_WaitPage(WaitPage):
    pass

class Mechanism_Easy_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank4_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 3, 'Easy')
        variables['rank_sentence'] = C.Rank_sentence[4]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Easy_rank4_choice',
            AvailableBundles=return_available_bundles(player, 3, 'Easy')
        )

class Mechanism_Easy_rank5_WaitPage(WaitPage):
    pass

class Mechanism_Easy_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank5_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 4, 'Easy')
        variables['rank_sentence'] = C.Rank_sentence[5]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Easy_rank5_choice',
            AvailableBundles=return_available_bundles(player, 4, 'Easy')
        )

class Mechanism_Medium_rank1_WaitPage(WaitPage):
    pass

class Mechanism_Medium_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank1_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = C.BUNDLES_MEDIUM
        variables['rank_sentence'] = C.Rank_sentence[1]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Medium_rank1_choice',
            AvailableBundles=C.BUNDLES_MEDIUM
        )

class Mechanism_Medium_rank2_WaitPage(WaitPage):
    pass

class Mechanism_Medium_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank2_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 1, 'Medium')
        variables['rank_sentence'] = C.Rank_sentence[2]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Medium_rank2_choice',
            AvailableBundles=return_available_bundles(player, 1, 'Medium')
        )

class Mechanism_Medium_rank3_WaitPage(WaitPage):
    pass

class Mechanism_Medium_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank3_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 2, 'Medium')
        variables['rank_sentence'] = C.Rank_sentence[3]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Medium_rank3_choice',
            AvailableBundles=return_available_bundles(player, 2, 'Medium')
        )

class Mechanism_Medium_rank4_WaitPage(WaitPage):
    pass

class Mechanism_Medium_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank4_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 3, 'Medium')
        variables['rank_sentence'] = C.Rank_sentence[4]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Medium_rank4_choice',
            AvailableBundles=return_available_bundles(player, 3, 'Medium')
        )

class Mechanism_Medium_rank5_WaitPage(WaitPage):
    pass

class Mechanism_Medium_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank5_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 4, 'Medium')
        variables['rank_sentence'] = C.Rank_sentence[5]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Medium_rank5_choice',
            AvailableBundles=return_available_bundles(player, 4, 'Medium')
        )

class Mechanism_Difficult_rank1_WaitPage(WaitPage):
    pass

class Mechanism_Difficult_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank1_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = C.BUNDLES_DIFFICULT
        variables['rank_sentence'] = C.Rank_sentence[1]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Difficult_rank1_choice',
            AvailableBundles=C.BUNDLES_DIFFICULT
        )

class Mechanism_Difficult_rank2_WaitPage(WaitPage):
    pass

class Mechanism_Difficult_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank2_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 1, 'Difficult')
        variables['rank_sentence'] = C.Rank_sentence[2]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Difficult_rank2_choice',
            AvailableBundles=return_available_bundles(player, 1, 'Difficult')
        )

class Mechanism_Difficult_rank3_WaitPage(WaitPage):
    pass

class Mechanism_Difficult_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank3_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 2, 'Difficult')
        variables['rank_sentence'] = C.Rank_sentence[3]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Difficult_rank3_choice',
            AvailableBundles=return_available_bundles(player, 2, 'Difficult')
        )

class Mechanism_Difficult_rank4_WaitPage(WaitPage):
    pass

class Mechanism_Difficult_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank4_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 3, 'Difficult')
        variables['rank_sentence'] = C.Rank_sentence[4]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Difficult_rank4_choice',
            AvailableBundles=return_available_bundles(player, 3, 'Difficult')
        )

class Mechanism_Difficult_rank5_WaitPage(WaitPage):
    pass

class Mechanism_Difficult_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank5_choice']

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)
        variables['Mechanism'] = player.participant.Treatment
        variables['AvailableBundles'] = return_available_bundles(player, 4, 'Difficult')
        variables['rank_sentence'] = C.Rank_sentence[5]
        return variables

    @staticmethod
    def js_vars(player: Player):
        return dict(
            Mechanism=player.participant.Treatment,
            Field_name='Difficult_rank5_choice',
            AvailableBundles=return_available_bundles(player, 4, 'Difficult')
        )
    
    
    
#%%    
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
#TODO: discuss. I really dont like the ordinality pages. I think they are unnecessary and unintuitive. 
pages_Attributes = [Attributes_rank, Attributes_rank_cardinality, 
                    Attributes_tasks_Dimension_1, Attributes_tasks_Dimension_1_cardinality,
                    Attributes_tasks_Dimension_2, Attributes_tasks_Dimension_2_cardinality,
                    Attributes_tasks_Dimension_3, Attributes_tasks_Dimension_3_cardinality,
                    Attributes_tasks_Dimension_4, Attributes_tasks_Dimension_4_cardinality,]

pages_mechanism = [
    Mechanism_Easy_rank1, 
    Mechanism_Easy_rank2_WaitPage, Mechanism_Easy_rank2, 
    Mechanism_Easy_rank3_WaitPage, Mechanism_Easy_rank3,
    Mechanism_Easy_rank4_WaitPage, Mechanism_Easy_rank4,
    Mechanism_Easy_rank5_WaitPage, Mechanism_Easy_rank5,
    Mechanism_Medium_rank1_WaitPage, Mechanism_Medium_rank1,
    Mechanism_Medium_rank2_WaitPage, Mechanism_Medium_rank2,
    Mechanism_Medium_rank3_WaitPage, Mechanism_Medium_rank3,
    Mechanism_Medium_rank4_WaitPage, Mechanism_Medium_rank4,
    Mechanism_Medium_rank5_WaitPage, Mechanism_Medium_rank5,
    Mechanism_Difficult_rank1_WaitPage, Mechanism_Difficult_rank1,
    Mechanism_Difficult_rank2_WaitPage, Mechanism_Difficult_rank2,
    Mechanism_Difficult_rank3_WaitPage, Mechanism_Difficult_rank3,
    Mechanism_Difficult_rank4_WaitPage, Mechanism_Difficult_rank4,
    Mechanism_Difficult_rank5_WaitPage, Mechanism_Difficult_rank5
    ]

pages_rest = [ChosenBundleExplanation_offer,
                 ChosenBundleExplanation,
                 ChosenBundlePlay,
                 Results,
                 Attention_check_2,]
#TODO: make sure to add the TreatmentWaitPage to the page_sequence
#TODO: make sure to add Attributes and randomize order with pages_mechanism
page_sequence = pages_mechanism + pages_rest

                
