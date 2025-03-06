from otree.api import *
import random
import json
# TODO: at the end. Currently the choices are saved as emojis, write a function to turn these emojis back into strings in Easy_rank_1_choice, etc.
doc = '''

'''
# Functions
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

def get_bundle_icons(player, rank, difficulty):
    
    bundles = list(return_available_bundles(player, rank, difficulty).keys())
    
    bundle_icons = C.Bundle_icons
    result = {}
    
    for bundle in bundles:
        parts = bundle.split('_')
        if '+' in bundle:
            sub_bundles = bundle.split('+')
            icons = []
            for sub_bundle in sub_bundles:
                task, difficulty = sub_bundle.split('_')
                icons.append(f"{bundle_icons[task]}<sub>{difficulty}</sub>")
            result[bundle] = ' + '.join(icons)
        else:
            task, difficulty = parts[0], parts[1]
            result[bundle] = f"{bundle_icons[task]}<sub>{difficulty}</sub>"
    return result

def return_available_bundles(player, rank, difficulty, save_to_player=False):
    """
    Returns a dictionary of available bundles for a player based on the specified difficulty and rank.
    
    Args:
        player (object): The player object containing participant information.
        rank (int): The rank of the bundle selection. Must be one of [1, 2, 3, 4, 5].
        difficulty (str): The difficulty level of the bundles. Must be one of ['Easy', 'Medium', 'Difficult'].
    
    Returns:
        dict: A dictionary of available bundles (keys & values), excluding those in unavailable_bundles.
    """
    
    assert difficulty in ['Easy', 'Medium', 'Difficult'], "Invalid difficulty level."
    assert rank in [1, 2, 3, 4, 5], "Rank must be between 1 and 5."

    player_id_group = player.participant.Group_id_counter
    Group = player.participant.Group
    # Selecting the correct bundle dictionary
    bundle_dict = {
        'Easy': C.BUNDLES_EASY,
        'Medium': C.BUNDLES_MEDIUM,
        'Difficult': C.BUNDLES_HIGH
    }[difficulty]

    # If rank is 1, return initial bundles instead of filtering
    if rank == 1:
        'if player is rank 1 he gets menu#Group_id_counter e.g. if hes the second player he gets the second menu'
        returnable = bundle_dict.get(f"{player_id_group}", {})
        if save_to_player:
            setattr(player, f"Available_bundles_{difficulty}_rank{rank}", json.dumps(list(returnable.keys())))
                
        return returnable  # Return full dictionary for rank 1

    
    players_dict = {p.participant.Group_id_counter: p for p in player.subsession.get_players()
                    if p.participant.id_in_session in player.participant.Group}  # Lookup dict for players
        
    unavailable_bundles = []

    # Mapping difficulty to attribute names dynamically
    rank_attributes = {
        'Easy': ['Easy_rank1_choice', 'Easy_rank2_choice', 'Easy_rank3_choice', 'Easy_rank4_choice'],
        'Medium': ['Medium_rank1_choice', 'Medium_rank2_choice', 'Medium_rank3_choice', 'Medium_rank4_choice'],
        'Difficult': ['Difficult_rank1_choice', 'Difficult_rank2_choice', 'Difficult_rank3_choice', 'Difficult_rank4_choice']
    }

    # Get the correct list of attributes based on difficulty
    chosen_ranks = rank_attributes[difficulty]

    '''
    for player 1 (group_id_counter = 1) 
        - rank 1, no unavailable bundles; menu #1
        - rank 2, unavailable bundles: what player 2 chose in rank 1 from menu 2; menu #2
        - .. 
        - rank 5, unavailable bundles: what player 5 chose in rank1, what player 4 chose in rank 4, .. ; menu #5
        
    for player i, (for Group_id_counter i in 1, 2, 3, 4, 5)
        - rank 1, no unavailable bundles; menu #Group_id_counter
        - rank i, unavailable bundles: what player i+1 chose in rank i-1 from menu i+1; menu #Group_id_counter + i
            - if i+1 > 5, then we start from 1 again (next guy)
            
    for player i > 5
        - algorithm treats him as player 1.
    '''
    # Extract unavailable bundles dynamically
    next_guy = player_id_group  
    opponent_rank = 0
    for x in range(1, rank): #range (0,rank): 1, 2, ... rank-1
        opponent_rank += 1
        next_guy += 1 #initially the next guy is the participant himself but then we increment it by one
        if next_guy >min(5, len(players_dict)+1): #if next guy is greater than 5, then we start from 1 again
            next_guy = 1 
        # print('players in this group',   players_dict.keys())
        # print('current guys id:', player_id_group,'next guy is:', next_guy)
        # get the player whose Group_id_counter == x - 1, this person has picked, in the previous round, from the relevant bundle.
        # print('playersdict' ,players_dict)
        player_object = players_dict[next_guy]
        
        # remove what player x-opponent_rank (group_id) what he picked in his choice x-opponent_rank 
        # (e.g. if group_id = 3 and rank 4,
        #   then we remove what player 4 picked in his choice 3, 
        #   + what player 5 picked in his choice 4, etc. 
        #TODO: ask guys to check if this works as intended.
        unavailable_bundles.append(getattr(player_object, chosen_ranks[x-opponent_rank]))
        # print(f'Rank: {rank}, player with group id {next_guy} had picked {getattr(player_object, chosen_ranks[x-opponent_rank])}')
    # Return dictionary without unavailable bundles
    menu_current = player_id_group + rank - 1 # e.g. if player is 2nd in group and rank 3, then he gets menu 4
    if player_id_group + rank - 1 > min(5, len(players_dict)+1): #but if there is no player 4 or he is 5th player then he gets menu 4
        menu_current = 1
    
    # returnable = {k: v for k, v in bundle_dict.get(f"{player_id_group + rank - 1}", {}).items() if k not in unavailable_bundles}
    returnable = {k: v for k, v in bundle_dict.get(f"{menu_current}", {}).items() if k not in unavailable_bundles}
    # print('returnable', returnable, 'unavailable', unavailable_bundles)
    # print('\n\n')
    
    if save_to_player:
        setattr(player, f"Available_bundles_{difficulty}_rank{rank}", json.dumps(list(returnable.keys())))
    
    return returnable

def calculate_task_scores(player):
    '''
    The calculate_task_scores function takes a player object and calculates their scores for different tasks based on various dimensions like cognitive load, engagement, confidence, and time efficiency. 
    It then updates the player's scores for each task by considering these dimensions.
    '''
    
    score_CognitiveLoad = player.cardinality_Dimension_1
    score_Engagement = player.cardinality_Dimension_2
    score_Confidence = player.cardinality_Dimension_3
    score_TimeEfficiency = player.cardinality_Dimension_4
    
    # weight scores
    total_score = score_CognitiveLoad + score_Engagement + score_Confidence + score_TimeEfficiency
    score_CognitiveLoad /= total_score
    score_Engagement /= total_score
    score_Confidence /= total_score
    score_TimeEfficiency /= total_score
    
    Quiz_scores = [player.cardinality_Dimension_CognitiveLoad_Quiz, player.cardinality_Dimension_Engagement_Quiz,
                   player.cardinality_Dimension_Confidence_Quiz, player.cardinality_Dimension_TimeEfficiency_Quiz]
    MathMemory_scores = [player.cardinality_Dimension_CognitiveLoad_MathMemory, player.cardinality_Dimension_Engagement_MathMemory,
                            player.cardinality_Dimension_Confidence_MathMemory, player.cardinality_Dimension_TimeEfficiency_MathMemory]
    EmotionRecognition_scores = [player.cardinality_Dimension_CognitiveLoad_EmotionRecognition, player.cardinality_Dimension_Engagement_EmotionRecognition,
                            player.cardinality_Dimension_Confidence_EmotionRecognition, player.cardinality_Dimension_TimeEfficiency_EmotionRecognition]
    SpotTheDifference_scores = [player.cardinality_Dimension_CognitiveLoad_SpotTheDifference, player.cardinality_Dimension_Engagement_SpotTheDifference,
                            player.cardinality_Dimension_Confidence_SpotTheDifference, player.cardinality_Dimension_TimeEfficiency_SpotTheDifference]
    
    # calculate weighted scores
    Quiz_scores = [score_CognitiveLoad * Quiz_scores[0], score_Engagement * Quiz_scores[1], score_Confidence * Quiz_scores[2], score_TimeEfficiency * Quiz_scores[3]]
    MathMemory_scores = [score_CognitiveLoad * MathMemory_scores[0], score_Engagement * MathMemory_scores[1], score_Confidence * MathMemory_scores[2], score_TimeEfficiency * MathMemory_scores[3]]
    EmotionRecognition_scores = [score_CognitiveLoad * EmotionRecognition_scores[0], score_Engagement * EmotionRecognition_scores[1], score_Confidence * EmotionRecognition_scores[2], score_TimeEfficiency * EmotionRecognition_scores[3]]
    SpotTheDifference_scores = [score_CognitiveLoad * SpotTheDifference_scores[0], score_Engagement * SpotTheDifference_scores[1], score_Confidence * SpotTheDifference_scores[2], score_TimeEfficiency * SpotTheDifference_scores[3]]
    
    player.score_Quiz = sum(Quiz_scores)
    player.score_MathMemory = sum(MathMemory_scores)
    player.score_EmotionRecognition = sum(EmotionRecognition_scores)
    player.score_SpotTheDifference = sum(SpotTheDifference_scores)
    
    print('SCORES. Quiz:', player.score_Quiz, 'MathMemory:', player.score_MathMemory, 'EmotionRecognition:', player.score_EmotionRecognition, 'SpotTheDifference:', player.score_SpotTheDifference)
 
 
def calculate_bundle_scores(player, difficulty, rank):
    """
    Calculates scores for each bundle in each difficulty level and rank.
    
    The score is determined based on the tasks in the bundle:
    - If the tasks in the bundle are **different**, the score is multiplied by `score_variety`.
    - If the tasks in the bundle are **the same**, the score is multiplied by `1 - score_variety`.
    
    The function stores the scores in a nested dictionary `Available_bundles_Easy_scores`.
    """
    
    # Retrieve available bundles
    Available_bundles = getattr(player, f"Available_bundles_{difficulty}_rank{rank}")
    Available_bundles = json.loads(Available_bundles)
    # Retrieve individual task scores
    task_scores = {
        "Quiz": player.score_Quiz,
        "MathMemory": player.score_MathMemory,
        "EmotionRecognition": player.score_EmotionRecognition,
        "SpotTheDifference": player.score_SpotTheDifference
    }
    print(f"\n task_scores: {task_scores}")
    score_variety = player.taste_variety  # Player's preference for variety

    # Initialize nested dictionary
    Available_bundles_scores = {}

    # Loop through each bundle
    for bundle in Available_bundles:
        # Split bundle into tasks (assuming tasks are separated by " + ")
        tasks = bundle.split(" + ")
        
        # Compute bundle score
        total_score = 0
        task_types = set()  # To track unique task types
        # print('tasks', tasks)
        for task in tasks:
            base_task = task.split("_")[0]  # Extract task type (e.g., "Math" from "Math_3")
            task_types.add(base_task)

            # Get task score from the dictionary
            task_score = task_scores.get(base_task, 0)  # Default to 0 if task not found
            total_score += task_score
        # print('total score before variety', total_score)
        # print('variety', score_variety)
        # Apply variety modifier
        if len(tasks)>1:
            if len(task_types) > 1:  # Tasks are different
                total_score *= score_variety
            else:  # Tasks are the same
                total_score *= (1 - score_variety)
            # print('total score after variety', total_score)

        # Store score in rank dictionary
        Available_bundles_scores[bundle] = total_score


    # Store the computed scores in the player model
    setattr(player, f"Available_bundles_{difficulty}_rank{rank}_score", json.dumps(Available_bundles_scores))

    return Available_bundles_scores  # Optional return for debugging

        
    
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
    
    
    # bundle icons
    Bundle_icons = {
            "Math": "🔢",
            "Spot": "🔍",
            "Quiz": "📚",
            "Emotion": "😃",
    }
    
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
    Confidence_text = "<strong>Place the task that you find yourself most confident with at the top.</strong>"
    TimeEfficiency_text = "<strong>Place the task that you think takes fewest amount of mouse-clicks at the top.</strong>"
    
    CognitiveLoad_text_2 = "<strong>If a task is mentally exhausting, assign it a lower score. </strong>"
    Engagement_text_2 = "<strong>If a task is engaging, assign it a higher score.</strong>"
    Confidence_text_2 = "<strong>If you feel confident in your ability in the task, assign it a higher score.</strong>"
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
    ## Attributes Survey
    ### Holds chosen bundle in the revsitit stage
    Easy_rank_1_revisit_choice = models.StringField(label='')
    Easy_rank_2_revisit_choice = models.StringField(label='')
    Easy_rank_3_revisit_choice = models.StringField(label='')
    Easy_rank_4_revisit_choice = models.StringField(label='')
    Easy_rank_5_revisit_choice = models.StringField(label='')

    Medium_rank_1_revisit_choice = models.StringField(label='')
    Medium_rank_2_revisit_choice = models.StringField(label='')
    Medium_rank_3_revisit_choice = models.StringField(label='')
    Medium_rank_4_revisit_choice = models.StringField(label='')
    Medium_rank_5_revisit_choice = models.StringField(label='')

    Difficult_rank_1_revisit_choice = models.StringField(label='')
    Difficult_rank_2_revisit_choice = models.StringField(label='')
    Difficult_rank_3_revisit_choice = models.StringField(label='')
    Difficult_rank_4_revisit_choice = models.StringField(label='')
    Difficult_rank_5_revisit_choice = models.StringField(label='')
    
    ### switch dummies. these are dictionaries 
    Easy_rank_1_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Easy_rank_2_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Easy_rank_3_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Easy_rank_4_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Easy_rank_5_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    
    Medium_rank_1_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Medium_rank_2_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Medium_rank_3_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Medium_rank_4_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Medium_rank_5_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    
    Difficult_rank_1_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Difficult_rank_2_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Difficult_rank_3_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Difficult_rank_4_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    Difficult_rank_5_revisit_choice_switch = models.IntegerField(label='Would you like to take the offered bundle or stick to the mechanism outcome?', choices=[[1, 'Offered bundle'], [0, 'Mechanism outcome']], widget=widgets.RadioSelect)
    
    #TODO: do the same for medium and difficult
    
    ### Outcome of the random choice
    Outcome_bundle = models.StringField()
    Performance_final_task = models.IntegerField(min=0, max=100)
    Performance_final_task_Attempts = models.IntegerField(blank=True, min=0, max=100)
    Earnings_final_task = models.FloatField()
    
    ## Dimension scores
    ranking_order = models.StringField() 
    cardinality_Dimension_1 = models.IntegerField()  #cognitive load 
    cardinality_Dimension_2 = models.IntegerField() # engagement 
    cardinality_Dimension_3 = models.IntegerField() # confidence
    cardinality_Dimension_4 = models.IntegerField() # time efficiency
    
    taste_variety = models.FloatField(
        label = '',
        choices = [[1.2, 'I strongly prefer a bundle with different tasks'],
                   [1.1, 'I mildly prefer a bundle with different tasks'],  
                   [1, 'I am indifferent'],
                   [0.9, 'I mildly prefer a bundle with the same task'],  
                   [0.8, 'I strongly prefer a bundle with the same task'],
                     ],
        widget=widgets.RadioSelect
    )
    
    ## Task_dimension scores
    ranking_order_CognitiveLoad = models.StringField()
    ranking_order_Engagement = models.StringField()
    ranking_order_Confidence = models.StringField()
    ranking_order_TimeEfficiency = models.StringField()
    
    cardinality_Dimension_CognitiveLoad_SpotTheDifference =  models.IntegerField()
    cardinality_Dimension_Engagement_SpotTheDifference =      models.IntegerField()
    cardinality_Dimension_Confidence_SpotTheDifference =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_SpotTheDifference = models.IntegerField()
    
    cardinality_Dimension_CognitiveLoad_Quiz =  models.IntegerField()
    cardinality_Dimension_Engagement_Quiz =      models.IntegerField()
    cardinality_Dimension_Confidence_Quiz =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_Quiz = models.IntegerField()
    
    cardinality_Dimension_CognitiveLoad_MathMemory =  models.IntegerField()
    cardinality_Dimension_Engagement_MathMemory =      models.IntegerField()
    cardinality_Dimension_Confidence_MathMemory =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_MathMemory = models.IntegerField()
    
    cardinality_Dimension_CognitiveLoad_EmotionRecognition =  models.IntegerField()
    cardinality_Dimension_Engagement_EmotionRecognition =      models.IntegerField()
    cardinality_Dimension_Confidence_EmotionRecognition =    models.IntegerField()
    cardinality_Dimension_TimeEfficiency_EmotionRecognition = models.IntegerField()
    
    ## Task scores
    score_Quiz = models.FloatField()
    score_MathMemory = models.FloatField()
    score_EmotionRecognition = models.FloatField()
    score_SpotTheDifference = models.FloatField()
    
    
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
    
    # these are the bundles that are available to the player. it is a dictionary i.e. rank_1: bundles, etc
    Available_bundles_Easy_rank1 = models.StringField(initial='')
    Available_bundles_Easy_rank2 = models.StringField(initial='')
    Available_bundles_Easy_rank3 = models.StringField(initial='')
    Available_bundles_Easy_rank4 = models.StringField(initial='')
    Available_bundles_Easy_rank5 = models.StringField(initial='')
    
    Available_bundles_Medium_rank1 = models.StringField(initial='')
    Available_bundles_Medium_rank2 = models.StringField(initial='')
    Available_bundles_Medium_rank3 = models.StringField(initial='')
    Available_bundles_Medium_rank4 = models.StringField(initial='')
    Available_bundles_Medium_rank5 = models.StringField(initial='')
    
    Available_bundles_Difficult_rank1 = models.StringField(initial='')
    Available_bundles_Difficult_rank2 = models.StringField(initial='')
    Available_bundles_Difficult_rank3 = models.StringField(initial='')
    Available_bundles_Difficult_rank4 = models.StringField(initial='')
    Available_bundles_Difficult_rank5 = models.StringField(initial='')
    
    #scores for each of the available bundles. a nested dictionary i.e. rank_1: {bundle: score, bundle2: score2, etc}, etc
    Available_bundles_Easy_rank1_score = models.StringField(initial='')
    Available_bundles_Easy_rank2_score = models.StringField(initial='')
    Available_bundles_Easy_rank3_score = models.StringField(initial='')
    Available_bundles_Easy_rank4_score = models.StringField(initial='')
    Available_bundles_Easy_rank5_score = models.StringField(initial='')
    
    Available_bundles_Medium_rank1_score = models.StringField(initial='')
    Available_bundles_Medium_rank2_score = models.StringField(initial='')
    Available_bundles_Medium_rank3_score = models.StringField(initial='')
    Available_bundles_Medium_rank4_score = models.StringField(initial='')
    Available_bundles_Medium_rank5_score = models.StringField(initial='')
    
    Available_bundles_Difficult_rank1_score = models.StringField(initial='')
    Available_bundles_Difficult_rank2_score = models.StringField(initial='')
    Available_bundles_Difficult_rank3_score = models.StringField(initial='')
    Available_bundles_Difficult_rank4_score = models.StringField(initial='')
    Available_bundles_Difficult_rank5_score = models.StringField(initial='')
 
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
        
        # variables['items'] = ["Dimension 1", "Dimension 2", "Dimension 3", "Dimension 4", "Dimension 5"]
        variables['items'] = ["Cognitive Load", "Engagement", "Confidence", "Time Efficiency", ]
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            field_name = 'ranking_order',
        )
    
class Attributes_rank_cardinality(MyBasePage):
    extra_fields = ['cardinality_Dimension_1', 'cardinality_Dimension_2', 
                    'cardinality_Dimension_3', 'cardinality_Dimension_4', ] 
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
    extra_fields = ['ranking_order_Confidence'] 
    form_fields = MyBasePage.form_fields + extra_fields

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        # Add or modify variables specific to ExtendedPage
        
        variables['items'] = ["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"]
        variables['DimensionAtHand'] = "Confidence"
        variables['DimensionText'] = C.Confidence_text
        
        variables['field_name'] = "ranking_order_Confidence"
        return variables
    
    @staticmethod
    def js_vars(player: Player):
        return dict(
            field_name = 'ranking_order_Confidence',
        )
    
class Attributes_tasks_Dimension_3_cardinality(MyBasePage):
    extra_fields = [
        'cardinality_Dimension_Confidence_SpotTheDifference', 
        'cardinality_Dimension_Confidence_Quiz',
        'cardinality_Dimension_Confidence_MathMemory',
        'cardinality_Dimension_Confidence_EmotionRecognition',
    ] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        ranking_order = player.ranking_order_Confidence #TODO: make this dynamic for randomizing pages
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "TimeFfiency"
        variables['DimensionText'] = C.Confidence_text
        
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
    
    
class Attributes_variety(MyBasePage):
    extra_fields = ['taste_variety']
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        
        variables = MyBasePage.vars_for_template(player)
            
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

#TODO: clarify. The order of ranks is not random 1,2,3,4,5
#TODO: clarify. The order of difficulty levels is not random first easy then medium then hard.

def get_variables_for_template(player: Player, rank: int, difficulty: str):
    variables = MyBasePage.vars_for_template(player)
    variables['Mechanism'] = player.participant.Treatment
    variables['player_Group_id'] = player.participant.Group_id_counter
    variables['AvailableBundles'] = list(return_available_bundles(player, rank, difficulty).values())
    variables['rank_sentence'] = C.Rank_sentence[rank]
    return variables

def get_js_vars(player: Player, rank: int, difficulty: str):
    return dict(
        Mechanism = player.participant.Treatment,
        Field_name = f'{difficulty}_rank{rank}_choice',
        AvailableBundles = list(return_available_bundles(player, rank, difficulty).values()),
        BundleIcons = get_bundle_icons(player, rank, difficulty)
    )
  

class Mechanism_Easy_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank1_choice'] 
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 1, 'Easy')
            
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 1, 'Easy')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 1,  'Easy', save_to_player=True)
                
        
class Mechanism_Easy_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank2_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 2, 'Easy')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 2, 'Easy')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        return_available_bundles(player, 2,  'Easy', save_to_player=True)


class Mechanism_Easy_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank3_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 3, 'Easy')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 3, 'Easy')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        return_available_bundles(player, 3,  'Easy', save_to_player=True)


class Mechanism_Easy_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank4_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 4, 'Easy')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 4, 'Easy')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        return_available_bundles(player, 4,  'Easy', save_to_player=True)


class Mechanism_Easy_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank5_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 5, 'Easy')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 5, 'Easy')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        return_available_bundles(player, 5,  'Easy', save_to_player=True)

class Mechanism_Medium_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank1_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 1, 'Medium')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 1, 'Medium')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        return_available_bundles(player, 1,  'Medium', save_to_player=True)

class Mechanism_Difficult_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank1_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 1, 'Difficult')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 1, 'Difficult')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        return_available_bundles(player, 1,  'Difficult', save_to_player=True)

## Wait pages

class Mechanism_Easy_rank2_WaitPage(WaitPage):   
    pass    
class Mechanism_Easy_rank3_WaitPage(WaitPage):   
    pass    
class Mechanism_Easy_rank4_WaitPage(WaitPage):   
    pass    
class Mechanism_Easy_rank5_WaitPage(WaitPage):   
    pass   

class Mechanism_Medium_rank1_WaitPage(WaitPage):
    pass 
class Mechanism_Medium_rank2_WaitPage(WaitPage):
    pass 
class Mechanism_Medium_rank3_WaitPage(WaitPage):
    pass 
class Mechanism_Medium_rank4_WaitPage(WaitPage):
    pass 
class Mechanism_Medium_rank5_WaitPage(WaitPage):
    pass 

class Mechanism_Difficult_rank1_WaitPage(WaitPage):
    pass 
class Mechanism_Difficult_rank2_WaitPage(WaitPage):
    pass 
class Mechanism_Difficult_rank3_WaitPage(WaitPage):
    pass 
class Mechanism_Difficult_rank4_WaitPage(WaitPage):
    pass 
class Mechanism_Difficult_rank5_WaitPage(WaitPage):
    pass 

#TODO: do the pages for medium and difficult
    
#%% Revisit pages
class Revisit_WaitPage(WaitPage):
    pass

class Revisit_explanation(MyBasePage):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_task_scores(player)
        for rank in range(1, 2): #TODO: change range to 1,6
            for difficulty in ['Easy',]: #TODO: add back#  'Medium', 'Difficult']
                calculate_bundle_scores(player, difficulty, rank)

def get_variables_for_template_revisit(player: Player, rank: int, difficulty: str):
    variables = MyBasePage.vars_for_template(player)
    # calculate_bundle_scores(player, difficulty, rank)    
    variables['rank'] = rank
    variables['difficulty'] = difficulty
    
    available_bundles_scores =getattr(player, f"Available_bundles_{difficulty}_rank{rank}_score")
    available_bundles_scores = json.loads(available_bundles_scores)
    variables['Scores_bundles'] = available_bundles_scores
    
    mechanism_outcome = getattr(player, f'{difficulty}_rank{rank}_choice')
    available_bundles_scores.pop(mechanism_outcome, None)  # Remove the mechanism outcome bundle
    offered_bundle = max(available_bundles_scores, key=available_bundles_scores.get)
    
    MechanismOutcome = getattr(player, f'{difficulty}_rank{rank}_choice')
    variables['MechanismOutcome'] = get_icon(MechanismOutcome.split('_')[0], MechanismOutcome.split('_')[1])
    variables['OfferedBundle'] = get_icon(offered_bundle.split('_')[0], offered_bundle.split('_')[1])
    
    return variables
       

class Revisit_Easy_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank_1_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 1, 'Easy')
    
class Revisit_Easy_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank_2_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 2, 'Easy')
    
class Revisit_Easy_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank_3_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 3, 'Easy')
    
class Revisit_Easy_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank_4_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 4, 'Easy')
    
class Revisit_Easy_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Easy_rank_5_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 5, 'Easy')

class Revisit_Medium_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank_1_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 1, 'Medium')
    
class Revisit_Medium_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank_2_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 2, 'Medium')
    
class Revisit_Medium_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank_3_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 3, 'Medium')
    
class Revisit_Medium_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank_4_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 4, 'Medium')
    
class Revisit_Medium_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank_5_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 5, 'Medium')

class Revisit_Difficult_rank1(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank_1_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 1, 'Difficult')
    
class Revisit_Difficult_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank_2_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 2, 'Difficult')
    
class Revisit_Difficult_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank_3_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 3, 'Difficult')
    
class Revisit_Difficult_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank_4_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 4, 'Difficult')
    
class Revisit_Difficult_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank_5_revisit_choice_switch']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template_revisit(player, 5, 'Difficult')



class Revisit_complete(MyBasePage):
    @staticmethod
    def vars_for_template(player: Player, timeout_happened=False):
        variables = MyBasePage.vars_for_template(player)
        
        random_bundle = player.participant.Random_bundle
        
        MechanismOutcome = getattr(player, f'{selected_difficulty}_rank{selected_rank}_choice')
        # check if player switched in Random_bundle[0] difficulty, Random_bundle[1] rank
        selected_difficulty = random_bundle.split('_')[0]
        selected_rank = int(random_bundle.split('_')[1])
        
        switched = getattr(player, f'{selected_difficulty}_rank_{selected_rank}_revisit_choice_switch')
        available_bundles_scores = getattr(player, f"Available_bundles_{selected_difficulty}_rank{selected_rank}_score")
        available_bundles_scores = json.loads(available_bundles_scores)
        available_bundles_scores.pop(MechanismOutcome, None)  # Remove the mechanism outcome bundle
        offered_bundle = max(available_bundles_scores, key=available_bundles_scores.get)
        
        # if player switched assign offered bundle otherwise mechanismOutcome
        if switched == 0:
            player.participant.Final_bundle = MechanismOutcome
        else:
            player.participant.Final_bundle = offered_bundle
            
        print(f'Player {player.participant.id_in_session} has been randomly selected to choose bundle {offered_bundle}')
        variables['RandomDifficulty'] = selected_difficulty
        variables['RandomRank'] = selected_rank
        
        variables['AssignedBundle'] = get_icon(player.participant.Final_bundle.split('_')[0], player.participant.Final_bundle.split('_')[1])

        return variables



#%% Outcome pages  
    
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
                    Attributes_tasks_Dimension_4, Attributes_tasks_Dimension_4_cardinality,
                    Attributes_variety
                    ]

pages_mechanism = [
    Mechanism_Easy_rank1, 
    Mechanism_Easy_rank2_WaitPage,# Mechanism_Easy_rank2, 
    # Mechanism_Easy_rank3_WaitPage, Mechanism_Easy_rank3,
    # Mechanism_Easy_rank4_WaitPage, Mechanism_Easy_rank4,
    # Mechanism_Easy_rank5_WaitPage, Mechanism_Easy_rank5,
    Mechanism_Medium_rank1,
    Mechanism_Medium_rank2_WaitPage, #Mechanism_Medium_rank2,
    # Mechanism_Medium_rank3_WaitPage, Mechanism_Medium_rank3,
    # Mechanism_Medium_rank4_WaitPage, Mechanism_Medium_rank4,
    # Mechanism_Medium_rank5_WaitPage, Mechanism_Medium_rank5,
    Mechanism_Difficult_rank1,
    Mechanism_Difficult_rank2_WaitPage, #Mechanism_Difficult_rank2,
    # Mechanism_Difficult_rank3_WaitPage, Mechanism_Difficult_rank3,
    # Mechanism_Difficult_rank4_WaitPage, Mechanism_Difficult_rank4,
    # Mechanism_Difficult_rank5_WaitPage, Mechanism_Difficult_rank5
    ]

pages_revisit = [
    # Revisit_WaitPage,
    Revisit_explanation,
    Revisit_Easy_rank1, #Revisit_Easy_rank2, Revisit_Easy_rank3, Revisit_Easy_rank4, Revisit_Easy_rank5,
    Revisit_Medium_rank1, #Revisit_Medium_rank2, Revisit_Medium_rank3, Revisit_Medium_rank4, Revisit_Medium_rank5,
    Revisit_Difficult_rank1, #Revisit_Difficult_rank2, Revisit_Difficult_rank3, Revisit_Difficult_rank4, Revisit_Difficult_rank5,
    Revisit_complete
]

pages_outcomeplay = [ChosenBundleExplanation,
                 ChosenBundlePlay,
                 Results,
                 Attention_check_2,]
#TODO: make sure to add the TreatmentWaitPage to the page_sequence
#TODO: make sure to add Attributes and randomize order with pages_mechanism
page_sequence =  pages_mechanism +  pages_Attributes + pages_revisit + pages_outcomeplay

                
