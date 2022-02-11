from pynput.keyboard import Key


# Time ranges for randomized execution time
macro_sleep = [0, 0.1]
key_sleep   = [0.01, 0.02]


# Config dictionaries
control_keys = {
    'toggle': Key.f9,
    'exit'  : Key.f10
}


# Control dictionaries
flags = {
    'running'  : False, 
    'exit'     : False,
    'first_run': True,
    'monster'  : False,
    'repair'   : False
}

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