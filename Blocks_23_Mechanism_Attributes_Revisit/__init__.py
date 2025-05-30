from otree.api import *
import random
import json
import ast

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
    bundles = list(return_available_bundles(player, rank, difficulty)[0].keys())
    bundle_icons = C.Bundle_icons
    result = {}

    for bundle in bundles:
        parts = bundle.split('_')
        icons = []
        for i in range(0, len(parts), 2):
            task = parts[i]
            difficulty = parts[i + 1]
            icons.append(f"{bundle_icons[task]}<sub>{difficulty}</sub>")
        result[bundle] = '&nbsp;+&nbsp;'.join(icons)
    
    return result

def return_available_bundles(player, rank, difficulty, save_to_player=False, return_unavailable_bundles=False):
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

    player_id_group = player.participant.ID_in_Group
    # Group = player.participant.Group
    # Selecting the correct bundle dictionary
    bundle_dict = {
        'Easy': C.BUNDLES_EASY,
        'Medium': C.BUNDLES_MEDIUM,
        'Difficult': C.BUNDLES_HIGH
    }[difficulty]
    
    # print(player.participant.Group)
    
    players_dict = {p.participant.ID_in_Group: p for p in player.subsession.get_players()
                if p.participant.id_in_session in player.participant.Group}  # Lookup dict for players
    
    # print("print: players_dict",players_dict.keys())
    
    # If rank is 1, return initial bundles instead of filtering
    if rank == 1:
        "if player is rank 1 he gets menu#ID_in_Group e.g. if he's the second player he gets the second menu"
        # if this is the 1st player, he gets menu 1; 2nd player gets menu 2, etc.
        menu = player_id_group  # if thiis is the 6th player, then his id is 6-5=1, set in the first app.
            
        available_bundles = bundle_dict.get(f"{menu}", {}) # if this is the 6th player, he gets menu 1 again; 7 -> 2, 8 -> 3, etc.
            
        if save_to_player:
            setattr(player, f"Available_bundles_{difficulty}_rank{rank}", json.dumps(list(available_bundles.keys())))
                
        return available_bundles, menu  # Return full dictionary for rank 1


    unavailable_bundles = []

    # Mapping difficulty to attribute names dynamically
    rank_attributes = {
        'Easy': ['Easy_rank1_choice', 'Easy_rank2_choice', 'Easy_rank3_choice', 'Easy_rank4_choice'],
        'Medium': ['Medium_rank1_choice', 'Medium_rank2_choice', 'Medium_rank3_choice', 'Medium_rank4_choice'],
        'Difficult': ['Difficult_rank1_choice', 'Difficult_rank2_choice', 'Difficult_rank3_choice', 'Difficult_rank4_choice']
    }

    # Get the correct list of attributes based on difficulty
    chosen_ranks = rank_attributes[difficulty]
    
    # Return dictionary without unavailable bundles; note that player_id_group is always <=5. even if n>20
    menu_current = ((player_id_group + rank - 2) % 5) + 1 # e.g., for player 4 in rank 2, menu will be 1
    
    '''
    for player 1 (ID_in_Group = 1) 
        - rank 1, no unavailable bundles == everythings available; menu #1
        - rank 2, unavailable bundles are: what player 2 chose in rank 1 from menu 2; menu #2
        - .. 
        - rank 5, unavailable bundles: what player 5 chose in rank1, what player 4 chose in rank 4, .. ; menu #5
        
    for player i, (for ID_in_Group i in 1, 2, 3, 4, 5)
        - rank 1, no unavailable bundles; menu #ID_in_Group
        - rank i, unavailable bundles: what player i+1 chose in rank i-1 from menu i+1; menu #ID_in_Group + i
            - if i+1 > 5, then we start from 1 again (next guy)
            
    for player i > 5
        - algorithm treats him as player i-5, so he gets menu #ID_in_Group - 5
    '''
    # Extract unavailable bundles dynamically
    # print('========DEBUGGING========')
    next_guy = player_id_group  
    next_guy_rank = rank -2
    for x in range(1, rank):  # x = 1 to rank-1 e.g, if rank=3, x = 1,2; rank = 5, x = 1,2,3,4
        next_guy += 1 # e.g., if player 1, rank 2, next_guy starts at 2.
        if next_guy > 5:
            next_guy = 1

        player_object = players_dict[next_guy]
        unavailable = getattr(player_object, chosen_ranks[next_guy_rank])  # CORRECT INDEXING!
        if unavailable:
            unavailable_clean = unavailable.strip('"').strip().lower()
            unavailable_bundles.append(unavailable_clean)

        # print(f"looped through {x} times")
        # print(f'Menu: {menu_current};id: {player_id_group} ;Rank: {rank}')
        # print(f"player with group id {next_guy}, at rank {next_guy_rank}, had picked {getattr(player_object, chosen_ranks[next_guy_rank])}")
        # print('\n')
        
        next_guy_rank -= 1  

    # returnable = {k: v for k, v in bundle_dict.get(f"{player_id_group + rank - 1}", {}).items() if k not in unavailable_bundles}
    # available_bundles = {k: v for k, v in bundle_dict.get(f"{menu_current}", {}).items() if k not in unavailable_bundles}
    available_bundles = {k: v for k, v in bundle_dict.get(f"{menu_current}", {}).items()
                     if k.strip().lower() not in unavailable_bundles}

    # unavailable_bundles = {k: v for k, v in bundle_dict.get(f"{menu_current}", {}).items() if k in unavailable_bundles}
    unavailable_bundles = {k: v for k, v in bundle_dict.get(f"{menu_current}", {}).items()
                            if k.strip().lower() in unavailable_bundles}

    # print('returnable', available_bundles, 'unavailable', unavailable_bundles)
    # print('\n\n')
    
    if save_to_player:
        setattr(player, f"Available_bundles_{difficulty}_rank{rank}", json.dumps(list(available_bundles.keys())))
        print(f"Saved to player: Available_bundles_{difficulty}_rank{rank}", json.dumps(list(available_bundles.keys())))
    
    if return_unavailable_bundles:
        return available_bundles, menu_current, unavailable_bundles
    else:    
        return available_bundles, menu_current

def calculate_task_scores(player):
    """
    Calculates and updates the player's scores for different tasks based on weighted dimensions.
    This function evaluates a player's performance across four dimensions: Cognitive Load, Engagement, 
    Confidence, and Time Efficiency. Each dimension is assigned a weight based on the player's 
    cardinality values for that dimension. These weights are then used to calculate weighted scores 
    for each task. The tasks include Quiz, MathMemory, EmotionRecognition, and SpotTheDifference.
    The process for calculating the scores is as follows:
    1. Retrieve the player's cardinality values for each dimension (Cognitive Load, Engagement, 
       Confidence, and Time Efficiency).
    2. Compute the total score by summing up the cardinality values of all dimensions.
    3. Normalize each dimension's score by dividing it by the total score to obtain weights.
    4. For each task, retrieve the player's scores for each dimension specific to that task.
    5. Multiply each task-specific dimension score by its corresponding weight.
    6. Sum up the weighted scores for all dimensions to calculate the final score for the task.
    7. Update the player's task scores with the calculated values.
    Example (Quiz task):
    - Suppose the player's cardinality values are:
        Cognitive Load: 10, Engagement: 20, Confidence: 30, Time Efficiency: 40.
    - The total score is 10 + 20 + 30 + 40 = 100.
    - The weights are:
        Cognitive Load: 10/100 = 0.1, Engagement: 20/100 = 0.2, 
        Confidence: 30/100 = 0.3, Time Efficiency: 40/100 = 0.4.
    - If the player's Quiz-specific scores are:
        Cognitive Load: 5, Engagement: 10, Confidence: 15, Time Efficiency: 20.
    - The weighted scores for Quiz are:
        Cognitive Load: 0.1 * 5 = 0.5, Engagement: 0.2 * 10 = 2.0,
        Confidence: 0.3 * 15 = 4.5, Time Efficiency: 0.4 * 20 = 8.0.
    - The final Quiz score is the sum of the weighted scores:
        0.5 + 2.0 + 4.5 + 8.0 = 15.0.
    - This process is repeated for all tasks.
    Parameters:
        player (object): An object representing the player, which contains attributes for 
                         cardinality values and task-specific scores.
    Updates:
        player.score_Quiz (float): The calculated score for the Quiz task.
        player.score_MathMemory (float): The calculated score for the MathMemory task.
        player.score_EmotionRecognition (float): The calculated score for the EmotionRecognition task.
        player.score_SpotTheDifference (float): The calculated score for the SpotTheDifference task.
    """
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
    
    # print('SCORES. Quiz:', player.score_Quiz, 'MathMemory:', player.score_MathMemory, 'EmotionRecognition:', player.score_EmotionRecognition, 'SpotTheDifference:', player.score_SpotTheDifference)
 
 
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
    # print(f"\n task_scores: {task_scores}")
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
        # # print('tasks', tasks)
        for task in tasks:
            base_task = task.split("_")[0]  # Extract task type (e.g., "Math" from "Math_3")
            task_types.add(base_task)

            # Get task score from the dictionary
            task_score = task_scores.get(base_task, 0)  # Default to 0 if task not found
            total_score += task_score
        # # print('total score before variety', total_score)
        # # print('variety', score_variety)
        # Apply variety modifier
        if len(tasks)>1:
            if len(task_types) > 1:  # Tasks are different
                total_score *= score_variety
            else:  # Tasks are the same
                total_score *= (1 - score_variety)
            # # print('total score after variety', total_score)

        # Store score in rank dictionary
        Available_bundles_scores[bundle] = total_score


    # Store the computed scores in the player model
    setattr(player, f"Available_bundles_{difficulty}_rank{rank}_score", json.dumps(Available_bundles_scores))

    return Available_bundles_scores  # Optional return for debugging

        
    
class C(BaseConstants):
    NAME_IN_URL = 'Mechanism'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1    
    
    Instructions_path = "_templates/global/Instructions.html"
    
    # bundle icons
    Bundle_icons = {
            "Math": "🔢",
            "Spot": "🔍",
            "Quiz": "📚",
            "Emotion": "😃",
    }
    
    BUNDLES_EASY = {
        "1": {
            "Math_2": "🔢<sub>2</sub>",  # Calculator with 2
            "Spot_1": "🔍<sub>1</sub>",  # Magnifying glass with 1
            "Quiz_1": "📚<sub>1</sub>",  # Books with 1
            "Emotion_1": "😃<sub>1</sub>",  # Smiley face with 1
            "Math_1": "🔢<sub>1</sub>",  # Calculator with 1
            "Emotion_2": "😃<sub>2</sub>",  # Smiley face with 2
            "Spot_2": "🔍<sub>2</sub>"  # Magnifying glass with 2
        },
        "2": {
            "Math_2": "🔢<sub>2</sub>",
            "Spot_2": "🔍<sub>2</sub>",
            "Quiz_2": "📚<sub>2</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Math_1": "🔢<sub>1</sub>",
            "Quiz_1": "📚<sub>1</sub>",
            "Spot_1": "🔍<sub>1</sub>"
        },
        "3": {
            "Math_2": "🔢<sub>2</sub>",
            "Spot_3": "🔍<sub>3</sub>",
            "Quiz_3": "📚<sub>3</sub>",
            "Emotion_3": "😃<sub>3</sub>",
            "Quiz_2": "📚<sub>2</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Spot_2": "🔍<sub>2</sub>"
        },
        "4": {
            "Math_2": "🔢<sub>2</sub>",
            "Spot_2": "🔍<sub>2</sub>",
            "Quiz_2": "📚<sub>2</sub>",
            "Emotion_3": "😃<sub>3</sub>",
            "Math_3": "🔢<sub>3</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Spot_3": "🔍<sub>3</sub>"
        },
        "5": {
            "Math_2": "🔢<sub>2</sub>",
            "Spot_3": "🔍<sub>3</sub>",
            "Quiz_3": "📚<sub>3</sub>",
            "Emotion_2": "😃<sub>2</sub>",
            "Math_3": "🔢<sub>3</sub>",
            "Emotion_3": "😃<sub>3</sub>",
            "Quiz_2": "📚<sub>2</sub>"
        }
    }

    BUNDLES_MEDIUM = { #done
        "1": {
            "Math_2_Emotion_2": "🔢<sub>2</sub> + 😃<sub>2</sub>",
            "Spot_1_Quiz_2": "🔍<sub>1</sub> + 📚<sub>2</sub>",
            "Quiz_2_Emotion_1": "📚<sub>2</sub> + 😃<sub>1</sub>",
            "Emotion_2_Quiz_1": "😃<sub>2</sub> + 📚<sub>1</sub>",
            "Math_1_Emotion_2": "🔢<sub>1</sub> + 😃<sub>2</sub>",
            "Quiz_1_Emotion_1": "📚<sub>1</sub> + 😃<sub>1</sub>",
            "Spot_1_Quiz_1": "🔍<sub>1</sub> + 📚<sub>1</sub>"
        },
        "2": { #done
            "Math_2_Spot_2": "🔢<sub>2</sub> + 🔍<sub>2</sub>",
            "Spot_1_Math_2": "🔍<sub>1</sub> + 🔢<sub>2</sub>",
            "Quiz_2_Spot_1": "📚<sub>2</sub> + 🔍<sub>1</sub>",
            "Emotion_2_Math_1": "😃<sub>2</sub> + 🔢<sub>1</sub>",
            "Math_1_Spot_2": "🔢<sub>1</sub> + 🔍<sub>2</sub>",
            "Quiz_1_Spot_1": "📚<sub>1</sub> + 🔍<sub>1</sub>",
            "Spot_1_Math_1": "🔍<sub>1</sub> + 🔢<sub>1</sub>"
        },
        "3": { #done
            "Math_2_Emotion_3": "🔢<sub>2</sub> + 😃<sub>3</sub>",
            "Spot_1_Quiz_3": "🔍<sub>1</sub> + 📚<sub>3</sub>",
            "Quiz_2_Emotion_2": "📚<sub>2</sub> + 😃<sub>2</sub>",
            "Emotion_3_Quiz_2": "😃<sub>3</sub> + 📚<sub>2</sub>",
            "Math_1_Emotion_3": "🔢<sub>1</sub> + 😃<sub>3</sub>",
            "Quiz_1_Emotion_2": "📚<sub>1</sub> + 😃<sub>2</sub>",
            "Spot_1_Quiz_2": "🔍<sub>1</sub> + 📚<sub>2</sub>"
        },
        "4": { #done
            "Math_2_Spot_3": "🔢<sub>3</sub> + 🔍<sub>3</sub>",
            "Spot_1_Math_3": "🔍<sub>1</sub> + 🔢<sub>3</sub>",
            "Quiz_2_Spot_2": "📚<sub>2</sub> + 🔍<sub>2</sub>",
            "Emotion_2_Math_2": "😃<sub>2</sub> + 🔢<sub>2</sub>",
            "Math_1_Spot_3": "🔢<sub>1</sub> + 🔍<sub>3</sub>",
            "Quiz_1_Spot_2": "📚<sub>1</sub> + 🔍<sub>2</sub>",
            "Spot_1_Math_2": "🔍<sub>1</sub> + 🔢<sub>2</sub>"
        },
        "5": { #done
            "Math_2_Emotion_3": "🔢<sub>2</sub> + 😃<sub>3</sub>",
            "Spot_2_Emotion_3": "🔍<sub>2</sub> + 😃<sub>3</sub>",
            "Quiz_2_Emotion_3": "📚<sub>2</sub> + 😃<sub>3</sub>",
            "Emotion_2_Emotion_3": "😃<sub>2</sub> + 😃<sub>3</sub>",
            "Math_1_Emotion_3": "🔢<sub>1</sub> + 😃<sub>3</sub>",
            "Quiz_1_Emotion_3": "📚<sub>1</sub> + 😃<sub>3</sub>",
            "Spot_1_Emotion_3": "🔍<sub>1</sub> + 😃<sub>3</sub>"
        }
    }


    BUNDLES_HIGH = {
        "1": { #done
            "Math_2_Emotion_2_Spot_2": "🔢<sub>2</sub> + 😃<sub>2</sub> + 🔍<sub>2</sub>",
            "Spot_1_Quiz_2_Spot_2": "🔍<sub>1</sub> + 📚<sub>2</sub> + 🔍<sub>2</sub>",
            "Quiz_2_Emotion_1_Spot_2": "📚<sub>2</sub> + 😃<sub>1</sub> + 🔍<sub>2</sub>",
            "Emotion_2_Quiz_1_Spot_2": "😃<sub>2</sub> + 📚<sub>1</sub> + 🔍<sub>2</sub>",
            "Math_1_Emotion_2_Spot_2": "🔢<sub>1</sub> + 😃<sub>2</sub> + 🔍<sub>2</sub>",
            "Quiz_1_Emotion_1_Spot_2": "📚<sub>1</sub> + 😃<sub>1</sub> + 🔍<sub>2</sub>",
            "Spot_1_Quiz_1_Spot_2": "🔍<sub>1</sub> + 📚<sub>1</sub> + 🔍<sub>2</sub>"
        },
        "2": { #done
            "Math_2_Spot_2_Emotion_1": "🔢<sub>2</sub> + 🔍<sub>2</sub> + 😃<sub>1</sub>",
            "Spot_1_Math_2_Emotion_1": "🔍<sub>1</sub> + 🔢<sub>2</sub> + 😃<sub>1</sub>",
            "Quiz_2_Spot_1_Emotion_1": "📚<sub>2</sub> + 🔍<sub>1</sub> + 😃<sub>1</sub>",
            "Emotion_2_Math_1_Emotion_1": "😃<sub>2</sub> + 🔢<sub>1</sub> + 😃<sub>1</sub>",
            "Math_1_Spot_2_Emotion_1": "🔢<sub>1</sub> + 🔍<sub>2</sub> + 😃<sub>1</sub>",
            "Quiz_1_Spot_1_Emotion_1": "📚<sub>1</sub> + 🔍<sub>1</sub> + 😃<sub>1</sub>",
            "Spot_1_Math_1_Emotion_1": "🔍<sub>1</sub> + 🔢<sub>1</sub> + 😃<sub>1</sub>"
        },
        "3": { #done
            "Math_2_Emotion_3_Math_3": "🔢<sub>2</sub> + 😃<sub>3</sub> + 🔢<sub>3</sub>",
            "Spot_1_Quiz_3_Math_3": "🔍<sub>1</sub> + 📚<sub>3</sub> + 🔢<sub>3</sub>",
            "Quiz_2_Emotion_2_Math_3": "📚<sub>2</sub> + 😃<sub>2</sub> + 🔢<sub>3</sub>",
            "Spot_2_Quiz_2_Math_3": "🔍<sub>2</sub> + 📚<sub>2</sub> + 🔢<sub>3</sub>",
            "Math_1_Emotion_3_Math_3": "🔢<sub>1</sub> + 😃<sub>3</sub> + 🔢<sub>3</sub>",
            "Quiz_1_Emotion_2_Math_3": "📚<sub>1</sub> + 😃<sub>2</sub> + 🔢<sub>3</sub>",
            "Spot_1_Quiz_2_Math_3": "🔍<sub>1</sub> + 📚<sub>2</sub> + 🔢<sub>3</sub>"
        },
        "4": { #done
            "Math_2_Spot_3_Quiz_2": "🔢<sub>2</sub> + 🔍<sub>3</sub> + 📚<sub>2</sub>",
            "Spot_1_Math_3_Quiz_2": "🔍<sub>1</sub> + 🔢<sub>3</sub> + 📚<sub>2</sub>",
            "Quiz_2_Spot_2_Quiz_2": "📚<sub>2</sub> + 🔍<sub>2</sub> + 📚<sub>2</sub>",
            "Emotion_2_Math_2_Quiz_2": "😃<sub>2</sub> + 🔢<sub>2</sub> + 📚<sub>2</sub>",
            "Math_1_Spot_3_Quiz_2": "🔢<sub>1</sub> + 🔍<sub>3</sub> + 📚<sub>2</sub>",
            "Quiz_1_Spot_2_Quiz_2": "📚<sub>1</sub> + 🔍<sub>2</sub> + 📚<sub>2</sub>",
            "Spot_1_Math_2_Quiz_2": "🔍<sub>1</sub> + 🔢<sub>2</sub> + 📚<sub>2</sub>"
        },
        "5": {
            "Math_2_Emotion_2_Spot_3": "🔢<sub>2</sub> + 😃<sub>2</sub> + 🔍<sub>3</sub>",
            "Spot_1_Quiz_2_Spot_3": "🔍<sub>1</sub> + 📚<sub>2</sub> + 🔍<sub>3</sub>",
            "Quiz_2_Emotion_1_Spot_3": "📚<sub>2</sub> + 😃<sub>1</sub> + 🔍<sub>3</sub>",
            "Emotion_2_Quiz_1_Spot_3": "😃<sub>2</sub> + 📚<sub>1</sub> + 🔍<sub>3</sub>",
            "Math_1_Emotion_2_Spot_2": "🔢<sub>1</sub> + 😃<sub>2</sub> + 🔍<sub>2</sub>",
            "Quiz_1_Emotion_1_Spot_2": "📚<sub>1</sub> + 😃<sub>1</sub> + 🔍<sub>2</sub>",
            "Spot_1_Quiz_1_Spot_2": "🔍<sub>1</sub> + 📚<sub>1</sub> + 🔍<sub>2</sub>"
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
    
    Rank_sentence = {
    1: "You are <strong>rank 1</strong>: the first to choose. Select your preferred bundle from all available options.",
    2: "You are <strong>rank 2</strong>: the second to choose. Select your preferred bundle from the remaining options.",
    3: "You are <strong>rank 3</strong>: the third to choose. Select your preferred bundle from the remaining options.",
    4: "You are <strong>rank 4</strong>: the fourth to choose. Select your preferred bundle from the remaining options.",
    5: "You are <strong>rank 5</strong>: the last to choose. Select your preferred bundle from the remaining options.",
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
    Easy_rank_1_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Easy_rank_2_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Easy_rank_3_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Easy_rank_4_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Easy_rank_5_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    
    Medium_rank_1_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Medium_rank_2_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Medium_rank_3_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Medium_rank_4_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Medium_rank_5_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    
    Difficult_rank_1_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Difficult_rank_2_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Difficult_rank_3_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Difficult_rank_4_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
    Difficult_rank_5_revisit_choice_switch = models.IntegerField(label='Please choose which of the two bundles you would prefer to receive as your final outcome for this round.', choices=[[1, 'Alternative bundle'], [0, 'Original bundle']], widget=widgets.RadioSelect)
        
    ### Outcome of the random choice
    Outcome_bundle = models.StringField()
    Performance_final_task = models.IntegerField(min=0, max=100)
    Performance_final_task_Attempts = models.IntegerField(blank=True, min=0, max=100)
    Earnings_final_task = models.FloatField()
    
    ## Dimension scores
    ranking_order = models.StringField(blank=True)  #TODO: remove blank 
    cardinality_Dimension_1 = models.IntegerField(blank=True)  #cognitive load  #TODO: remove blank 
    cardinality_Dimension_2 = models.IntegerField(blank=True) # engagement  #TODO: remove blank 
    cardinality_Dimension_3 = models.IntegerField(blank=True) # confidence #TODO: remove blank 
    cardinality_Dimension_4 = models.IntegerField(blank=True) # time efficiency #TODO: remove blank 
    
    taste_variety = models.FloatField(
        initial=1,
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
    ranking_order_CognitiveLoad = models.StringField(blank=True) # TODO: remove all blank trues
    ranking_order_Engagement = models.StringField(blank=True) #
    ranking_order_Confidence = models.StringField(blank=True) #
    ranking_order_TimeEfficiency = models.StringField(blank=True) #
    
    cardinality_Dimension_CognitiveLoad_SpotTheDifference =  models.IntegerField(blank=True)   #TODO: remove all blank true
    cardinality_Dimension_Engagement_SpotTheDifference =      models.IntegerField(blank=True) 
    cardinality_Dimension_Confidence_SpotTheDifference =    models.IntegerField(blank=True) 
    cardinality_Dimension_TimeEfficiency_SpotTheDifference = models.IntegerField(blank=True) 
     
    cardinality_Dimension_CognitiveLoad_Quiz =  models.IntegerField(blank=True)    #TODO: remove all blank true
    cardinality_Dimension_Engagement_Quiz =      models.IntegerField(blank=True)
    cardinality_Dimension_Confidence_Quiz =    models.IntegerField(blank=True)
    cardinality_Dimension_TimeEfficiency_Quiz = models.IntegerField(blank=True)
    
    cardinality_Dimension_CognitiveLoad_MathMemory =  models.IntegerField(blank=True)   #TODO: remove all blank true
    cardinality_Dimension_Engagement_MathMemory =      models.IntegerField(blank=True)
    cardinality_Dimension_Confidence_MathMemory =    models.IntegerField(blank=True)
    cardinality_Dimension_TimeEfficiency_MathMemory = models.IntegerField(blank=True)
    
    cardinality_Dimension_CognitiveLoad_EmotionRecognition =  models.IntegerField(blank=True)  #TODO: remove all blank true
    cardinality_Dimension_Engagement_EmotionRecognition =      models.IntegerField(blank=True)
    cardinality_Dimension_Confidence_EmotionRecognition =    models.IntegerField(blank=True)
    cardinality_Dimension_TimeEfficiency_EmotionRecognition = models.IntegerField(blank=True)
    
    ## Task scores
    score_Quiz = models.FloatField()
    score_MathMemory = models.FloatField()
    score_EmotionRecognition = models.FloatField()
    score_SpotTheDifference = models.FloatField()
    
    
    ## Mechanism
    Easy_rank1_choice = models.StringField(blank=True) #TODO: remove all blank true
    Easy_rank2_choice = models.StringField(blank=True)
    Easy_rank3_choice = models.StringField(blank=True)
    Easy_rank4_choice = models.StringField(blank=True)
    Easy_rank5_choice = models.StringField(blank=True)
    
    Medium_rank1_choice = models.StringField(blank=True)
    Medium_rank2_choice = models.StringField(blank=True)
    Medium_rank3_choice = models.StringField(blank=True)
    Medium_rank4_choice = models.StringField(blank=True)
    Medium_rank5_choice = models.StringField(blank=True)
    
    Difficult_rank1_choice = models.StringField(blank=True)
    Difficult_rank2_choice = models.StringField(blank=True)
    Difficult_rank3_choice = models.StringField(blank=True)
    Difficult_rank4_choice = models.StringField(blank=True)
    Difficult_rank5_choice = models.StringField(blank=True)
    
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
    def vars_for_template(player: Player):
        return {'hidden_fields': [], #hide the browser field from the participant, see the page to see how this works. #user_clicked_out
                'Instructions': C.Instructions_path,
                'MechanismPage': "_templates/global/Mechanism.html",} 
  
#%% Pages


class Attributes_explanation(MyBasePage):
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
        
    @staticmethod   
    def before_next_page(player: Player, timeout_happened):
        'FOR DEBUG ONLY: choose a random ranking order'
        pass
        player.ranking_order = json.dumps(["Cognitive Load", "Engagement", "Confidence", "Time Efficiency"])
    
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
        variables['DimensionAtHand'] = "Cognitive Load"
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
        ranking_order = player.ranking_order_CognitiveLoad 
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "Cognitive Load"
        variables['DimensionText'] = C.CognitiveLoad_text_2
        
        # TODO: remove the next 2 lines (DEBUG ONLY)
        if not ranking_order:
            ranking_order = json.dumps(random.sample(["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"], 4))
    
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
        ranking_order = player.ranking_order_Engagement 
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "Engagement"
        variables['DimensionText'] = C.Engagement_text_2
        # TODO: remove the next 2 lines (DEBUG ONLY)
        if not ranking_order:
            ranking_order = json.dumps(random.sample(["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"], 4))
    
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
        ranking_order = player.ranking_order_Confidence 
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "Confidence"
        variables['DimensionText'] = C.Confidence_text_2
                # TODO: remove the next 2 lines (DEBUG ONLY)
        if not ranking_order:
            ranking_order = json.dumps(random.sample(["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"], 4))
    
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
        variables['DimensionAtHand'] = "Time Efficiency"
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
        ranking_order = player.ranking_order_TimeEfficiency 
        
        variables = MyBasePage.vars_for_template(player)
        
        variables['DimensionAtHand'] = "Time Efficiency"
        variables['DimensionText'] = C.TimeEfficiency_text_2
        # TODO: remove the next 2 lines (DEBUG ONLY)
        if not ranking_order:
            ranking_order = json.dumps(random.sample(["SpotTheDifference", "Quiz", "MathMemory", "EmotionRecognition"], 4))
    
        variables['ranked_items'] = json.loads(ranking_order)
        return variables
    
    
class Attributes_variety(MyBasePage):
    extra_fields = ['taste_variety']
    form_fields = MyBasePage.form_fields + extra_fields
    
    @staticmethod
    def vars_for_template(player: Player):
        
        variables = MyBasePage.vars_for_template(player)
            
        return variables
    
    'this is for debug TODO: delete the following lines'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        for dimension_field in ['cardinality_Dimension_1', 'cardinality_Dimension_2', 'cardinality_Dimension_3', 'cardinality_Dimension_4']:
            if not player.field_maybe_none(dimension_field):
                setattr(player, dimension_field, random.randint(1, 10))
                
        for attribute in ['cardinality_Dimension_CognitiveLoad_Quiz', 'cardinality_Dimension_CognitiveLoad_SpotTheDifference', 'cardinality_Dimension_CognitiveLoad_MathMemory', 'cardinality_Dimension_CognitiveLoad_EmotionRecognition',
                  'cardinality_Dimension_Engagement_Quiz', 'cardinality_Dimension_Engagement_SpotTheDifference', 'cardinality_Dimension_Engagement_MathMemory', 'cardinality_Dimension_Engagement_EmotionRecognition',
                  'cardinality_Dimension_Confidence_Quiz', 'cardinality_Dimension_Confidence_SpotTheDifference', 'cardinality_Dimension_Confidence_MathMemory', 'cardinality_Dimension_Confidence_EmotionRecognition',
                  'cardinality_Dimension_TimeEfficiency_Quiz', 'cardinality_Dimension_TimeEfficiency_SpotTheDifference', 'cardinality_Dimension_TimeEfficiency_MathMemory', 'cardinality_Dimension_TimeEfficiency_EmotionRecognition']:
            if not player.field_maybe_none(attribute):
                setattr(player, attribute, random.randint(1, 10))


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




def get_variables_for_template(player: Player, rank: int, difficulty: str):
    variables = MyBasePage.vars_for_template(player)
    variables['Mechanism'] = player.participant.Treatment
    variables['player_Group_id'] = player.participant.ID_in_Group
    variables['AvailableBundles'] = list(return_available_bundles(player, rank, difficulty)[0].values())
    variables['Menu'] = return_available_bundles(player, rank, difficulty)[1]
    
    if rank==1:
        variables['UnavailableBundles'] = 'ALL IS PERMITTED TO THE FIRST BORN!'
    else:
        variables['UnavailableBundles'] = list(return_available_bundles(player, rank, difficulty, return_unavailable_bundles=True)[2].values())
    if player.participant.ID_in_Treatment >5:
        variables['Note'] = f"This players decisions have no bearing on others ({player.participant.ID_in_Treatment}th player in treatment)"
    else:
        variables['Note'] = f"This players decisions have a bearing on others ({player.participant.ID_in_Treatment}th player in treatment)"
    variables['rank_sentence'] = C.Rank_sentence[rank]
    return variables

def get_js_vars(player: Player, rank: int, difficulty: str):
    return dict(
        Mechanism = player.participant.Treatment,
        Field_name = f'{difficulty}_rank{rank}_choice',
        AvailableBundles = list(return_available_bundles(player, rank, difficulty)[0].keys()),
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

class Mechanism_Medium_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank2_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 2, 'Medium')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 2, 'Medium')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 2, 'Medium', save_to_player=True)


class Mechanism_Medium_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank3_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 3, 'Medium')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 3, 'Medium')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 3, 'Medium', save_to_player=True)


class Mechanism_Medium_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank4_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 4, 'Medium')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 4, 'Medium')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 4, 'Medium', save_to_player=True)

class Mechanism_Medium_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Medium_rank5_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 5, 'Medium')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 5, 'Medium')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 5, 'Medium', save_to_player=True)
        
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

class Mechanism_Difficult_rank2(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank2_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 2, 'Difficult')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 2, 'Difficult')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        return_available_bundles(player, 2,  'Difficult', save_to_player=True)
        
class Mechanism_Difficult_rank3(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank3_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 3, 'Difficult')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 3, 'Difficult')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 3, 'Difficult', save_to_player=True)


class Mechanism_Difficult_rank4(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank4_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 4, 'Difficult')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 4, 'Difficult')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 4, 'Difficult', save_to_player=True)


class Mechanism_Difficult_rank5(MyBasePage):
    form_fields = MyBasePage.form_fields + ['Difficult_rank5_choice']
    
    @staticmethod
    def vars_for_template(player: Player):
        return get_variables_for_template(player, 5, 'Difficult')
    
    @staticmethod
    def js_vars(player: Player):
        return get_js_vars(player, 5, 'Difficult')
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        return_available_bundles(player, 5, 'Difficult', save_to_player=True)


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

    
#%% Revisit pages
class Revisit_WaitPage(WaitPage):
    pass

    
class Revisit_explanation(MyBasePage):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        
        '''
        for each player and each choice, we check if it is empty,
            if empty we assign a random available bundle.
        This is for debug only!
        # TODO: remove these codes, replace with pass
        '''
        'setting random bundles for the player'
        for rank in range(1, 6):
            for difficulty in ['Easy', 'Medium', 'Difficult']:
                choice_field = f"{difficulty}_rank{rank}_choice"
                if not getattr(player, choice_field):
                    available_bundles = return_available_bundles(player, rank, difficulty)[0]
                    random_choice = random.choice(list(available_bundles.keys()))
                    setattr(player, choice_field, random_choice)
        
        
        
        
        calculate_task_scores(player)
        for rank in range(1, 6): 
            for difficulty in ['Easy', 'Medium', 'Difficult']:
                calculate_bundle_scores(player, difficulty, rank)
                


def get_variables_for_template_revisit(player: Player, rank: int, difficulty: str):
    variables = MyBasePage.vars_for_template(player)
    # calculate_bundle_scores(player, difficulty, rank)    
    variables['rank'] = rank
    variables['difficulty'] = difficulty
    
    available_bundles_scores =getattr(player, f"Available_bundles_{difficulty}_rank{rank}_score")
    available_bundles_scores = json.loads(available_bundles_scores)
    variables['Scores_bundles'] = available_bundles_scores
    
    print(f"Available Bundle Scores_before: {available_bundles_scores}")
    
    mechanism_outcome = getattr(player, f'{difficulty}_rank{rank}_choice')

    # Try to decode only if it starts and ends with a quote
    if isinstance(mechanism_outcome, str) and mechanism_outcome.startswith('"') and mechanism_outcome.endswith('"'):
        mechanism_outcome = ast.literal_eval(mechanism_outcome)
        
    available_bundles_scores.pop(mechanism_outcome, None)  # Remove the mechanism outcome bundle
    offered_bundle = max(available_bundles_scores, key=available_bundles_scores.get)
    
    print(f"Mechanism Outcome: {mechanism_outcome}")
    print(f"Available Bundle Scores_after: {available_bundles_scores}")
    print(f"Offered Bundle: {offered_bundle}")
    

    MechanismOutcome = getattr(player, f'{difficulty}_rank{rank}_choice')
   # variables['MechanismOutcome'] = get_icon(MechanismOutcome.split('_')[0], MechanismOutcome.split('_')[1])
    #variables['OfferedBundle'] = get_icon(offered_bundle.split('_')[0], offered_bundle.split('_')[1])

    def format_bundle_icon(bundle_str):
        clean = bundle_str.strip('"')  # Remove potential quotes
        parts = clean.split('_')
        return ' + '.join([get_icon(parts[i], parts[i+1]) for i in range(0, len(parts), 2)])

    variables['MechanismOutcome'] = format_bundle_icon(MechanismOutcome)
    variables['OfferedBundle'] = format_bundle_icon(offered_bundle)
    
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
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Choose a random round (difficulty and rank)
        difficulties = ['Easy', 'Medium', 'Difficult']
        ranks = [1, 2, 3, 4, 5]
        difficulty = random.choice(difficulties)
        rank = random.choice(ranks)
        player.participant.Random_bundle = f"{difficulty}_{rank}"



class Revisit_complete(MyBasePage):
    @staticmethod
    def vars_for_template(player: Player, timeout_happened=False):
        variables = MyBasePage.vars_for_template(player)
        
        random_bundle = player.participant.Random_bundle
        
        # check if player switched in Random_bundle[0] difficulty, Random_bundle[1] rank
        selected_difficulty = random_bundle.split('_')[0]
        selected_rank = int(random_bundle.split('_')[1])
        MechanismOutcome = getattr(player, f'{selected_difficulty}_rank{selected_rank}_choice')
        
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
            
        # print(f'Player {player.participant.id_in_session} has been randomly selected to choose bundle {offered_bundle}')
        variables['RandomDifficulty'] = selected_difficulty
        variables['RandomRank'] = selected_rank
        
        def format_bundle_icon(bundle_str):
            clean = bundle_str.strip('"')
            parts = clean.split('_')
            return ' + '.join([get_icon(parts[i], parts[i+1]) for i in range(0, len(parts), 2)])

        variables['AssignedBundle'] = format_bundle_icon(player.participant.Final_bundle)
        
        return variables



#%% Outcome pages  
  



# TODO: randomize whether mechanism or attributes comes first  
#TODO: discuss. I really dont like the ordinality pages. I think they are unnecessary and unintuitive. 
pages_Attributes = [
    Attributes_explanation,
    Attributes_rank, Attributes_rank_cardinality, 
    Attributes_tasks_Dimension_1, Attributes_tasks_Dimension_1_cardinality,
    Attributes_tasks_Dimension_2, Attributes_tasks_Dimension_2_cardinality,
    Attributes_tasks_Dimension_3, Attributes_tasks_Dimension_3_cardinality,
    Attributes_tasks_Dimension_4, Attributes_tasks_Dimension_4_cardinality,
    Attributes_variety
                    ]

pages_mechanism = [
    Mechanism_Easy_rank1, 
    Mechanism_Easy_rank2_WaitPage, Mechanism_Easy_rank2, 
    Mechanism_Easy_rank3_WaitPage, Mechanism_Easy_rank3,
    Mechanism_Easy_rank4_WaitPage, Mechanism_Easy_rank4,
    Mechanism_Easy_rank5_WaitPage, Mechanism_Easy_rank5,
    Mechanism_Medium_rank1,
    Mechanism_Medium_rank2_WaitPage, Mechanism_Medium_rank2,
    Mechanism_Medium_rank3_WaitPage, Mechanism_Medium_rank3,
    Mechanism_Medium_rank4_WaitPage, Mechanism_Medium_rank4,
    Mechanism_Medium_rank5_WaitPage, Mechanism_Medium_rank5,
    Mechanism_Difficult_rank1,
    Mechanism_Difficult_rank2_WaitPage, Mechanism_Difficult_rank2,
    Mechanism_Difficult_rank3_WaitPage, Mechanism_Difficult_rank3,
    Mechanism_Difficult_rank4_WaitPage, Mechanism_Difficult_rank4,
    Mechanism_Difficult_rank5_WaitPage, Mechanism_Difficult_rank5
    ]

pages_revisit = [
    Revisit_WaitPage,
    Revisit_explanation,
    Revisit_Easy_rank1, Revisit_Easy_rank2, Revisit_Easy_rank3, Revisit_Easy_rank4, Revisit_Easy_rank5,
    Revisit_Medium_rank1, Revisit_Medium_rank2, Revisit_Medium_rank3, Revisit_Medium_rank4, Revisit_Medium_rank5,
    Revisit_Difficult_rank1, Revisit_Difficult_rank2, Revisit_Difficult_rank3, Revisit_Difficult_rank4, Revisit_Difficult_rank5,
    Revisit_complete
]



page_sequence =  pages_Attributes + pages_mechanism +   pages_revisit

                
