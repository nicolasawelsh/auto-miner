from pynput.keyboard import Key, Controller, Listener
from time import sleep, time
from threading import Thread
from datetime import datetime

start = datetime.now()

control_keys = {
    'toggle': Key.f9,
    'exit': Key.f10
}

flags = {
    'running': False, 
    'exit': False,
    'first_run': True
}

cmd_text = {
    'instructions': "Input delay between mining (in seconds): ",
    'tutorial_1':   "--- Type {} to  start/stop mining ---".format(control_keys['toggle']),
    'tutorial_2':   "---- Type {} to  end the script ----".format(control_keys['exit']),
    'breaker':      "=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=",
    'started':      "------------- Macro started -------------",
    'paused':       "------------- Macro  paused -------------",
    'terminated':   "---------- Program  terminated ----------",
    'warning':      "=~=~=~=~ Watch out for monsters! ~=~=~=~="
}


def on_press(key):
    if key == control_keys['toggle']:
        flags['running'] = not flags['running']
        if flags['running']:
            print_text('started')
            flags['first_run'] = False
        else:
            print_text('paused')
    elif key == control_keys['exit']:
        flags['exit'] = True
        print_text('terminated')
        return False


def macro(flags):
    keyboard = Controller()
    while not flags['exit']:
        if check_exit(mine_time + 0.01, flags): return
        if flags['running']:
            press(keyboard, 'm')
            press(keyboard, '!')
            press(keyboard, 'm')
            press(keyboard, Key.enter)
            print_mine()


def press(keyboard, key):
    keyboard.press(key)
    sleep(0.01)
    keyboard.release(key)
    sleep(0.01)


def check_exit(s, flags):
    start = time()
    while time() < (start + s):
        if flags['exit']:
            return True
    return False


def print_mine():
    print("\u26cf", end="  ")
    print(datetime.now().time())


def print_text(argument):
    if argument == 'instructions':
        return float(input(cmd_text['instructions']))
    elif argument == 'tutorial':
        print()
        print(cmd_text['tutorial_1'])
        print(cmd_text['tutorial_2'])
        print()
    elif argument == 'warning':
        print(cmd_text['breaker'])
        print(cmd_text['warning'])
        print(cmd_text['breaker'])
        print()
    elif argument == 'started':
        if flags['first_run']:
            print(cmd_text['breaker'])
            print(cmd_text['warning'])
            print(cmd_text['breaker'])
            print()
        print(cmd_text['started'])
    elif argument == 'paused':
        print(cmd_text['paused'])
    elif argument == 'terminated':
        print(cmd_text['terminated'])


if __name__ == "__main__":
    mine_time = print_text('instructions')
    print_text('tutorial')

    macro_thread = Thread(target=macro, args=(flags,))
    macro_thread.start()

    with Listener(on_press=on_press) as listener:
        listener.join()
        
    macro_thread.join()
