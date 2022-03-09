from pynput.keyboard import Key


# Time ranges for randomized execution time
execution_sleep = {
    'key'           : [0.01, 0.02],
    'macro'         : [0.01, 0.1],
    'command_sleep' : [0.01, 0.1]
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
    'first_run': True,
    'monster'  : False,
    'repair'   : False
}

# Alerts sent by discord_bot, received by macro
alerts = {
    'repair_needed'    : False,
    'monster_appeared' : False
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
