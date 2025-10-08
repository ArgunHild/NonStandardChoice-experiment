from os import environ

SESSION_CONFIGS = [
    
    dict(name='Experiment', 
         app_sequence=[
             'Block_0_Introduction', 
            #  'Block_1_Practice', 
             'Block_1_Practice',
             'Blocks_23_Mechanism_Attributes_Revisit',
            #  'Block_4_MarketLevelOutcomes', 
             'Block_98_Play',
],
         num_demo_participants=10,
         completionlink='prolific completion link!!!!!!'), 
    dict(name='MechanismAttributesRevisit', 
         app_sequence=['Block_0_Introduction', 'Blocks_23_Mechanism_Attributes_Revisit'],
         num_demo_participants=14, #need at least 10 participants, 5 for each mechs.
         completionlink='prolific completion link!!!!!!'), 


    dict(name='FinalPlayStage', 
         app_sequence=['Block_98_Play'],
         num_demo_participants=2,
         completionlink='prolific completion link!!!!!!'), 
    
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOMS = [
    dict( name = 'Survey', display_name = 'Survey'),
]


SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="", use_browser_bots=False,
)

PARTICIPANT_FIELDS = [
    'Allowed','Comprehension_passed', #'Attention_passed',
    'task_order',
    'Treatment', 'Group', 'ID_in_Group', 'ID_in_Treatment',
    'Random_bundle', 'Final_bundle',
    'Bonus_1','Bonus_1_task',  'Bonus_2',
    'Total_bonus', 'Total_payment',
]

SESSION_FIELDS = {
                    'Male_quotas':{}, 'Female_quotas':{} 
                 }

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9007113971546'
