output_file = 'test.xlsx'  # output file name

twotone_column = 'AOS'  # column where all two-tone boards are listed in the template

rainbow_column = 'CCV'  # column where all rainbow boards are listd in the template

delay_time = 0.1  # delay between operations in seconds

prefix_location = 'C3'

mouse_locations = {
    "start": (33, 76),  # top left
    "col2top": (225, 76),  # top second
    "col3top": (443, 76),  # top third
    "col2mid": (230, 117),  # mid second
    "col2bottom": (230, 150),  # bottom second
    "col3mid": (443, 117),
    "col4top": (616, 76)  # top fourth

}

options_mt = {  # values as they are in the class vs as they are in dataframes
    'overpair': 'overpair',
    'top_pair': 'top pair',
    'mid_pair': 'middle pair',
    'ace_high': 'ace high',
    'gutshot': 'gutshot',
    'oesd': 'oesd',
    'overcards': 'overcards',
    'nut_fd': 'nut flushdr.',
    'weak_fd': 'weak flushdr.',
    'set': 'set',
    'two_pair': 'two pair',
    'flush': 'flush',
    'straight': 'straight',
    'second_nut_fd': '2nd Nut fd.',
    'third_nut_fd': '3rd Nut fd.',
    'pp_top_card': 'pp<top card',
    'weak_pair': "weak pair",
    'premium_draws': "Premium Draws",
    'strong_draw': "Strong Draw",
    "bare_gutshot": "Bare Gutshot",
    "combo_draw": "Combo Draw",
    "bare_ace_high": "Bare Ace High",
    "bare_overcards": "Bare Overcards",
    "premium": "Premium",
    "strong": "Strong",
    "mediocre": "Mediocre"

}
options_2t = {
    'overpair': 'overpair',
    'top_pair': 'top pair',
    'mid_pair': 'middle pair',
    'ace_high': 'ace high',
    'gutshot': 'gutshot',
    'oesd': 'oesd',
    'overcards': 'overcards',
    'fd': 'flushdraw',
    '2c_bd_fd': '2crd bckdr fd.',
    'set': 'set',
    'two_pair': 'two pair',
    'straight': 'straight',
    'full_house': 'full house',
    'quads': 'quads',
    'pp_top_card': 'pp<top card',
    'weak_pair': "weak pair",
    'premium_draws': "Premium Draws",
    'strong_draw': "Strong Draw",
    "bare_gutshot": "Bare Gutshot",
    "combo_draw": "Combo Draw",
    "bare_ace_high": "Bare Ace High",
    "bare_overcards": "Bare Overcards",
    "premium": "Premium",
    "strong": "Strong",
    "mediocre": "Mediocre"
}

options_r = {
    'overpair': 'overpair',
    'top_pair': 'top pair',
    'mid_pair': 'middle pair',
    'ace_high': 'ace high',
    'gutshot': 'gutshot',
    'oesd': 'oesd',
    'overcards': 'overcards',
    '2c_bd_fd': '2crd bckdr fd.',
    'set': 'set',
    'two_pair': 'two pair',
    'straight': 'straight',
    'full_house': "full house",
    'quads': "quads",
    'pp_top_card': 'pp<top card',
    'weak_pair': "weak pair",
    'premium_draws': "Premium Draws",
    'strong_draw': "Strong Draw",
    "bare_gutshot": "Bare Gutshot",
    "combo_draw": "Combo Draw",
    "bare_ace_high": "Bare Ace High",
    "bare_overcards": "Bare Overcards",
    "premium": "Premium",
    "strong": "Strong",
    "mediocre": "Mediocre"
}

normal_actions = [
    ('col2top', 1),  # bet1
    ('col3top', 2),  # bet1raise
    ('col2mid', 5),  # check
    ('col3mid', 6),  # check bet 1
    ('col4top', 7),  # check bet 1 raise
    ('col3top', 8),  # check bet 2
    ('col4top', 9)  # check bet 2 raise
]

donk_actions = [
    ('col2mid', 1),  # bet1
    ('col3top', 2),  # bet1raise
    ('col2top', 3),  # bet2
    ('col3top', 4),  # bet2raise
    ('col2bottom', 5),  # check
    ('col3mid', 6),  # check bet 1
    ('col4top', 7),  # check bet 1 raise
    ('col3top', 8),  # check bet 2
    ('col4top', 9)  # check bet 2 raise
]
