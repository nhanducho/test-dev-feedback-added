from os import environ

SESSION_CONFIGS = [
    dict(
        name='experiment_1_prolific',
        app_sequence=['experiment_1_prolific'],
        num_demo_participants=5,
        participation_fee=3.00,
    ),
    dict(
        name='experiment_1_lab',
        app_sequence=['experiment_1_lab'],
        num_demo_participants=10,
        participation_fee=3.00,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.0,
    real_world_currency_decimal_places=1,
    doc=""
)

ROOMS = [
    dict(
        name='exp_room',
        display_name='Experiment 1 Room',
    )
]

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 1
DEBUG = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5632304548013'
