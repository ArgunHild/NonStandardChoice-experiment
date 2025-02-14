from os import environ

SESSION_CONFIGS = [
    
    dict(name='Skeleton', 
         app_sequence=[
             'Block_0_Introduction', 
            #  'Block_1_Practice', 
             'Block_2_Mechanism_Attributes', 'Block_3_Revisit_choice',
             'Block_4_MarketLevelOutcomes', 'Block_99_Results'],
         num_demo_participants=1,
         completionlink='prolific completion link!!!!!!'), #TODO: add the proper completion link from prolific
    dict(name='Mechanism', 
         app_sequence=['Block_2_Mechanism_Attributes'],
         num_demo_participants=1,
         completionlink='prolific completion link!!!!!!'), #TODO: add the proper completion link from prolific

    
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOMS = [
    dict( name = 'Survey', display_name = 'Survey'),
]

#TODO: add use use_browser_bots=True, to test with website bots
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="", use_browser_bots=False,
)
#TODO: add the relevant participant fields if you wanna pass them thourgh apps
PARTICIPANT_FIELDS = [
    'Allowed','Comprehension_passed', 'Attention_passed',
    'Treatment',
    'Final_bundle'
]
#TODO: add the treatments here
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
