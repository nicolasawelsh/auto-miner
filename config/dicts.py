from pynput.keyboard import Key
from re              import compile


# File to store database
dbfile = 'dbfile'

# Time ranges for randomized execution time
execution_sleep = {
    'key'           : [0.01, 0.02],
    'macro'         : [0.01, 0.05]
}

# Control keys for script pausing and exiting
control_keys = {
    'toggle': Key.f9,
    'exit'  : Key.f10
}

# Control flags
flags = {
    'running'  : False, 
    'exit'     : False,
    'first_run': True
}

# Alerts used by database
alerts = {
    'repair_needed'    : False,
    'monster_appeared' : False
}

# Regex patterns for message searches
regex_patterns = {
    # Bot messages
    'repair_needed'    : compile(r'broke'),
    'repair_success'   : compile(r'successfully repaired'),
    'monster_appeared' : compile(r'being attacked|got problems'),
    'monster_defeated' : compile(r'defeated the enemy'),
    # User messages
    'request_mine'     : compile(r'm!m'),
    'request_repair'   : compile(r'm!repair'),
    'request_fight'    : compile(r'm!fight')
}

# Text used in stdout
cmd_text = {
    'instructions': "Input delay between mining (in seconds): ",
    'tutorial_1'  : "--- Type {} to  start/stop mining ---".format(control_keys['toggle']),
    'tutorial_2'  : "---- Type {} to  end the script ----".format(control_keys['exit']),
    'breaker'     : "=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=",
    'started'     : "------------- Macro started -------------",
    'paused'      : "------------- Macro  paused -------------",
    'terminated'  : "---------- Program  terminated ----------",
    'warning'     : "=~=~=~=~ Watch out for monsters! ~=~=~=~="
}
