from otree.api import *
import random
import numpy as np

doc = """
Your app description
"""

TASK_LABELS = {
    'Spot':    'Spot the Difference',
    'Quiz':    'Quiz',
    'Math':    'MathMemory',
    'Emotion': 'Emotion Recognition',
}

def readable_task(token: str) -> str:
    """Strip stray quotes and map to a display label."""
    clean = token.strip('"')
    return TASK_LABELS.get(clean, clean)  # fallback = raw token

def clean_split(bundle_str: str):
    return bundle_str.strip('"').split('_')

PLAIN_ICONS = {
    'Math':    '🔢',
    'Spot':    '🔍',
    'Quiz':    '📚',
    'Emotion': '😃',
}


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
    
    Round_length = 120 
    Timer_text = "Time left to complete this round:" 
    
    Instructions_general_path = "_templates/global/Instructions.html"

    Return_redirect = "https://www.wikipedia.org/" 
    
    # Task instruction paths
    Emotion_template = "_templates/global/Task_templates/Emotion.html"
    Quiz_template = "_templates/global/Task_templates/Quiz.html"
    Math_template = "_templates/global/Task_templates/Math.html"
    Spot_template_3 = "_templates/global/Task_templates/Spot_3.html" 
    Spot_template_4 = "_templates/global/Task_templates/Spot_4.html" 
    # Task instruction paths
    Math_instructions = "_templates/global/Task_instructions/Math.html"
    Emotion_instructions = "_templates/global/Task_instructions/Emotion.html"
    Quiz_instructions = "_templates/global/Task_instructions/Quiz.html"
    Spot_instructions = "_templates/global/Task_instructions/Spot.html"

    
    Completion_fee = 5 
    Bonus_max_practice = 4.50 
    Bonus_max = 20 
    
    
    Minimum_scores = {
        "Quiz": {
            1: 8,
            2: 14,
            3: 17
        },
        "Math": {
            1: 12,
            2: 16,
            3: 24,
        },
        "Spot": {
            1: 2,
            2: 6,
            3: 8
        },
        "Emotion": {
            1: 3,
            2: 5,
            3: 8
        }        
    }
    
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Demographics
    prolific_id = models.StringField(default=str("None")) #prolific id, will be fetched automatically.
    age = models.IntegerField(blank=False, 
                                label="Age", min=18, max=100)
    gender = models.StringField(blank=False, 
                                label='Gender at birth',
                                choices=['Male', 'Female', 'Other/Prefer not to say'], widget=widgets.RadioSelect)
    education = models.StringField(blank=False, 
                                label = 'Education level',
                                   choices=['Haven’t graduated high school','GED','High school graduate','Bachelors','Masters','Professional degree (JD, MD, MBA)','Doctorate', 'Other'], widget=widgets.RadioSelect) 
    # education = models.StringField(label = 'Education level',
    #                                choices=['High school or lower','Bachelors degree','Masters degree','PhD','Other'], widget=widgets.RadioSelect) 
    
    employment = models.StringField(blank=False, 
                                label='Employment status',
                                    choices=['Employed full-time', 'Employed part-time', 'Self-employed', 'Out of work, or seeking work',
                                             'Student', 'Out of labor force (e.g. retired or parent raising one or more children)'], widget=widgets.RadioSelect)
    
    income = models.StringField(blank=False, 
                                label='Approximately, what was your <strong>total household income</strong> in the last year, before taxes?',
                            choices=['$0-$10.000', '$10.000-$20.000','$20.000-$30.000','$30.000-$40.000','$40.000-$50.000','$50.000-$60.000',
                                     '$50.000-$75.000', '$75.000-$100.000', '$100.000-$150.000', '$150.000-$200.000', '$200.000+', 'Prefer not to answer',
                                     ],)
    
    
    
    Attention_2 = models.IntegerField(min=0, max=100, initial=0)
    
    Game_1_performance = models.IntegerField(min=0, max=100, initial=0)
    Game_2_performance = models.IntegerField(min=0, max=100, initial=0)
    Game_3_performance = models.IntegerField(min=0, max=100, initial=0)
    
    Bonus_final_bundle = models.FloatField(min=0, max=100, initial=0)
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
                'Instructions': C.Instructions_general_path,
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
    
    Final_bundle = Final_bundle.strip('"')
    task = Final_bundle.split('_')[field_num]
    difficulty = int(Final_bundle.split('_')[field_num+1])
    performance = getattr(player, f'Game_{game_num}_performance')
    
    bonus = 0
    # print('DEBUGGING:', Final_bundle, task, difficulty)
    if performance >= C.Minimum_scores[task][difficulty]:
        bonus = 1
    # print('DEBUGGING:', Final_bundle, task, difficulty, bonus)
    setattr(player, f'Bonus_2_{game_num}', bonus)
    

class Game_1(MyBasePage):
    extra_fields = ['Game_1_performance'] 
    form_fields = MyBasePage.form_fields + extra_fields
    
    timeout_seconds, timer_text = C.Round_length, C.Timer_text

    @staticmethod
    def js_vars(player): 
        
        # player.participant.Final_bundle = "Emotion_2_Emotion_2_Emotion_2"
        
        returnable = dict(field_name = 'Game_1_performance',
                          trial='trial',)
        if player.participant.Final_bundle.startswith('Quiz'):
            returnable['trial'] = 'trial3'
        elif player.participant.Final_bundle.startswith('Spot'):
            returnable['trial'] = 'trial3'
        elif player.participant.Final_bundle.startswith('Emotion'):
            returnable['trial'] = 'trial3'
        else:
            returnable['trial'] = 'trial'
        return returnable
        
    @staticmethod
    def vars_for_template(player: Player):
        
        # player.participant.Final_bundle = "Emotion_2_Emotion_2_Emotion_2"


        
        variables = MyBasePage.vars_for_template(player)
        
        bundle = clean_split(player.participant.Final_bundle)
        num         = 0                       # <- Game_1 always reads the 1st task
        task_code   = bundle[num].strip('"')  # strip errant quotes once
        task_name   = readable_task(task_code)
        variables['Icon'] = PLAIN_ICONS[task_code]


        variables['Task']            = task_name
        variables['Difficulty']      = int(bundle[num + 1])  # true level 1-3
        variables['Task_instructions'] = getattr(C, f'{task_code}_instructions')
        
        
        if player.participant.Final_bundle.startswith('Spot'):
            GameTemplate = getattr(C, f'{task_code}_template_3')
        else:
            GameTemplate = getattr(C, f'{task_code}_template')    
        
        variables['GameTemplate']      = GameTemplate
        

        return variables
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_bonus(player, 0)

class Game_2_Transition(MyBasePage):
    @staticmethod
    def is_displayed(player: Player):
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        return len(bundle) > 2
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        bundle    = clean_split(player.participant.Final_bundle)
        num       = 2                       # Game_2 reads the 2nd task (index 2)
        task_code = bundle[num].strip('"')
        task_name = readable_task(task_code)
        variables['Icon'] = PLAIN_ICONS[task_code]


        variables['Task']            = task_name

        return variables


class Game_2(MyBasePage):
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
        
        returnable = dict(field_name = 'Game_2_performance',
                          trial='trial',)
        Final_bundle = player.participant.Final_bundle
        bundle_list = Final_bundle.split('_') 
        
        if bundle_list[2] == 'Quiz':
            if bundle_list[0] == 'Quiz':
                returnable['trial'] = 'trial4'
            else: 
                returnable['trial'] = 'trial3'
        if bundle_list[2] == 'Spot':
            if bundle_list[0] == 'Spot':
                returnable['trial'] = 'trial4'
            else: 
                returnable['trial'] = 'trial3'
        if bundle_list[2] == 'Emotion':
            if bundle_list[0] == 'Emotion':
                returnable['trial'] = 'trial4'
            else: 
                returnable['trial'] = 'trial3'
        return returnable

    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        bundle    = clean_split(player.participant.Final_bundle)
        num       = 2                       # Game_2 reads the 2nd task (index 2)
        task_code = bundle[num].strip('"')
        task_name = readable_task(task_code)
        variables['Icon'] = PLAIN_ICONS[task_code]


        variables['Task']            = task_name
        variables['Difficulty']      = int(bundle[num + 1])   # true level (1-3)
        variables['Task_instructions'] = getattr(C, f'{task_code}_instructions')
        
        Final_bundle = player.participant.Final_bundle
        bundle_list = Final_bundle.split('_') 
        
        if bundle_list[2] == 'Spot':
            GameTemplate = getattr(C, f'{task_code}_template_4')
        else:
            GameTemplate = getattr(C, f'{task_code}_template')    
        
        variables['GameTemplate']      = GameTemplate

        return variables

    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_bonus(player, 2)
class Game_3_Transition(MyBasePage):
    @staticmethod
    def is_displayed(player: Player):
        Final_bundle = player.participant.Final_bundle
        bundle = Final_bundle.split('_')
        return len(bundle) > 4
    
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        bundle    = clean_split(player.participant.Final_bundle)
        num       = 4                       # Game_2 reads the 2nd task (index 2)
        task_code = bundle[num].strip('"')
        task_name = readable_task(task_code)
        variables['Icon'] = PLAIN_ICONS[task_code]


        variables['Task']            = task_name

        return variables
class Game_3(MyBasePage):
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
        
        returnable = dict(field_name = 'Game_3_performance',)
        Final_bundle = player.participant.Final_bundle
        bundle_list = Final_bundle.split('_') 
        
        if bundle_list[4] == 'Quiz':
            if 'Quiz' in (bundle_list[0], bundle_list[2]):
                returnable['trial'] = 'trial4'
            else: 
                returnable['trial'] = 'trial3'
        if bundle_list[4] == 'Spot':
            if 'Spot' in (bundle_list[0], bundle_list[2]):
                returnable['trial'] = 'trial4'
            else: 
                returnable['trial'] = 'trial3'
        if bundle_list[4] == 'Emotion':
            if 'Emotion' in (bundle_list[0], bundle_list[2]):
                returnable['trial'] = 'trial4'
            else: 
                returnable['trial'] = 'trial3'
        return returnable

        
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        bundle    = clean_split(player.participant.Final_bundle)
        num       = 4                       # Game_2 reads the 2nd task (index 2)
        task_code = bundle[num].strip('"')
        task_name = readable_task(task_code)
        variables['Icon'] = PLAIN_ICONS[task_code]


        variables['Task']            = task_name
        variables['Difficulty']      = int(bundle[num + 1])   # true level (1-3)
        variables['Task_instructions'] = getattr(C, f'{task_code}_instructions')
        
        Final_bundle = player.participant.Final_bundle
        bundle_list = Final_bundle.split('_') 
        
        if bundle_list[4] == 'Spot':
            GameTemplate = getattr(C, f'{task_code}_template_4')
        else:
            GameTemplate = getattr(C, f'{task_code}_template')    
        
        variables['GameTemplate']      = GameTemplate

        return variables
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        calculate_bonus(player, 4)
        
        if player.Bonus_2_1 == 1 and player.Bonus_2_2 == 1 and player.Bonus_2_3 == 1:
            player.Bonus_final_bundle == C.Bonus_max


class ResultsWaitPage(WaitPage):
    """
    This is a wait page that is used to ensure that all players have completed
    the tasks before proceeding to the results page.
    """
    body_text = "Please wait for all players to complete their tasks."



class Results(MyBasePage):

    # ───────────────── bookkeeping AFTER the page ──────────────────
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     # Compute the bundle bonus again for payoff records
    #     tokens = clean_split(player.participant.Final_bundle)
    #     task_slots = range(0, len(tokens), 2)          # 0, 2, 4 …

    #     passed_every_task = all(
    #         getattr(player, f'Bonus_2_{i//2 + 1}') == 1 for i in task_slots
    #     )



    # ───────────── variables FOR the template (shown immediately) ─────────────
    @staticmethod
    def vars_for_template(player: Player):
        v = MyBasePage.vars_for_template(player)

        # ---------- recompute pass/fail *here* so display is correct ----------
        tokens = clean_split(player.participant.Final_bundle)
        task_slots = range(0, len(tokens), 2)

        passed_every_task = all(
            getattr(player, f'Bonus_2_{i//2 + 1}') == 1 for i in task_slots
        )
        player.Bonus_final_bundle = C.Bonus_max if passed_every_task else 0

        total_pay =  (
            C.Completion_fee
            + player.participant.Bonus_1/100
            + player.Bonus_final_bundle
        )
        # Round up to the next 0.5 EUR
        def ceil_to_half_eur(amount):
            return np.ceil(amount * 2) / 2
        total_pay = ceil_to_half_eur(total_pay)
        player.participant.payoff = cu(total_pay)
        
        # ---------- build per-task list ----------
        list_items = []
        for i in task_slots:
            t_code   = tokens[i]
            diff     = int(tokens[i + 1])
            icon     = get_icon(t_code, diff)
            game_no  = i // 2 + 1
            achieved = getattr(player, f'Game_{game_no}_performance')
            required = C.Minimum_scores[t_code][diff]
            passed   = getattr(player, f'Bonus_2_{game_no}') == 1

            status = (
                '<span style="color:green">Cutoff reached. Your performance/Cutoff:</span>'
                if passed else
                '<span style="color:red">Cutoff not reached. Your performance/Cutoff:</span>'
            )
            list_items.append(
                f'<li>{icon}: {status} '
                f'({achieved}&nbsp;/&nbsp;{required})</li>'
            )

        v['Performance_Text'] = '<ol>' + ''.join(list_items) + '</ol>'

        # ---------- bundle-bonus message ----------
        v['ResultsText'] = (
            f'✔️ <strong>Congratulations!</strong> All tasks passed – '
            f'you earn <strong>{player.Bonus_final_bundle} €</strong>.'
            if player.Bonus_final_bundle else
            '❌ <strong>No bonus.</strong> At least one task did not meet '
            'its required score.'
        )

        # ---------- payment breakdown ----------

        
        print(total_pay, player.participant.Bonus_1/100, player.Bonus_final_bundle)
        print('player.payoff:', player.participant.payoff)
        v['Payments'] = (
            f'<ol>'
            f'<li>Participation fee: {C.Completion_fee} €</li>'
            f'<li>Practice-stage bonus: {player.participant.Bonus_1/100} €</li>'
            f'<li>Bundle bonus: {player.Bonus_final_bundle} €</li>'
            f'</ol>'
            f'<strong>Total payment: {total_pay} €</strong>'
        )

        return v


# Results2 is just as a safety backup for the moment.
# class Results2(MyBasePage):
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         player.participant.vars['Bonus_2'] = player.Bonus_final_bundle
#         player.participant.vars['Total_Bonus'] = player.participant.Bonus_1 + player.Bonus_final_bundle
#         player.participant.vars['Total_payment'] = player.participant.Bonus_1 + player.Bonus_final_bundle + C.Completion_fee
#         player.participant.payoff = player.participant.Bonus_1 + player.Bonus_final_bundle + C.Completion_fee
    
#     @staticmethod
#     def vars_for_template(player: Player):
#         variables = MyBasePage.vars_for_template(player)
        
#         Final_bundle = player.participant.Final_bundle
#         Final_bundle = Final_bundle.strip('"')
        
#         bundle = Final_bundle.split('_')
        
#         bundle_1 = get_icon(bundle[0], int(bundle[1]))  
#         try: 
#             bundle_2 = get_icon(bundle[2], int(bundle[3]))
#         except:
#             bundle_2 = False
#         try:
#             bundle_3 = get_icon(bundle[4], int(bundle[5]))
#         except:
#             bundle_3 = False
            
#         final_bundle = f'{bundle_1}+{bundle_2}+{bundle_3}'
        
#         variables['Final_bundle'] = final_bundle
#         if bundle_2 and bundle_3:
#             Performance_Text = f'''
#             <ol>
#             <li> {bundle_1}: {player.Game_1_performance} points </li>
#             <li> {bundle_2}: {player.Game_2_performance} points </li>
#             <li> {bundle_3}: {player.Game_3_performance} points </li>
#             </ol>
#             '''
#         elif bundle_2:
#             Performance_Text = f'''
#             <ol>
#             <li> {bundle_1}: {player.Game_1_performance} points </li>
#             <li> {bundle_2}: {player.Game_2_performance} points </li>
#             </ol>
#             '''
#         else:
#             Performance_Text = f'''
#             <ol>
#             <li> {bundle_1}: {player.Game_1_performance} points </li>
#             </ol>
#             '''
        
#         if player.Bonus_final_bundle >0:
#             results_text = f'''
#             <strong>Congratulations!</strong> You have successfully completed the tasks in your bundle and earned a bonus of <strong>{player.Bonus_final_bundle}€</strong>.
#             '''
#         else:
#             results_text = f'''
#             <strong>Unfortunately, you did not meet the required minimum scores in all tasks.</strong> Therefore, you will not receive a bonus for this bundle.
#             '''
            
#         payments =  f'''
#             <ol>
#             <li> Participation payment: {C.Completion_fee}€ </li>
#             <li> Bonus from practice stage: {player.participant.Bonus_1}€ </li>
#             <li> Bonus from bundle performance: {player.Bonus_final_bundle}€ </li>
#             </ol>
#             <strong>Total payment: {player.participant.Bonus_1 + player.Bonus_final_bundle + C.Completion_fee}€</strong>
            
#             <br><br>
#             Thank you for participating in this experiment! Your total payment will be processed shortly.
             
#             '''
        
#         variables['Performance_Text'] = Performance_Text
#         variables['ResultsText'] = results_text
        
#         variables['Payments'] = payments
        


#         return variables
    
    
class Demographics(MyBasePage):
    extra_fields = ['age', 'gender', 'education', 'employment', 'income'] 
    form_fields = MyBasePage.form_fields + extra_fields

        
    @staticmethod
    def vars_for_template(player: Player):
        variables = MyBasePage.vars_for_template(player)

        variables['hidden_fields'].append('browser') 
        return variables
       
        
class Study_complete(MyBasePage):
    pass
        
page_sequence = [Game_1, Game_2_Transition, Game_2, Game_3_Transition, Game_3, Demographics, ResultsWaitPage,
                 Results , Study_complete]
