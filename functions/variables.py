delay_time = 0.1 #delay between operations in seconds

mouse_locations = {
    "start": (33, 76), #top left
    "bet1": (225, 76), #top second
    "bet1raise": (443, 76), #top third
    "check": (230, 117), #mid second
    "donk2": (230, 158), #bottom second
    "action3opt3": (443, 117),
    "checkbetraise": (616, 76) #top fourth

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
    'flush': 'flush'
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
    'set': 'set'
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
    'set': 'set'
}