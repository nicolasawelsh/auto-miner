# Imported libraries
from pynput.keyboard import Key, Controller, Listener
from threading       import Thread
from datetime        import datetime
from time            import sleep, time
from random          import uniform

# Local libraries
from config.pickle_db import read_db, build_db
from config.dicts     import control_keys, flags, cmd_text, \
                             execution_sleep


def on_press(key):
    if key == control_keys['toggle']:
        toggle()
    elif key == control_keys['exit']:
        flags['exit'] = True
        print_text('terminated')
        return False


def toggle(toggle_pause=True, pause=False):
    if toggle_pause:
        flags['running'] = not flags['running']
    else:
        if pause:
            flags['running'] = False
        else:
            flags['running'] = True

    if flags['running']:
        print_text('started')
    else:
        print_text('paused')
    flags['first_run'] = False


# Threaded as "mine_thread"
def mine_macro():
    keyboard = Controller()
    while not flags['exit']:
        # Mine macro
        if flags['running']:
            press_keys(keyboard, 'm!m')
            press_keys(keyboard, [Key.enter])
            print_text('mine')

        # Macro loop delay
        delay = mine_time + rand_sleep('macro', do_sleep=False)
        if check_exit(delay): 
            return


# Threaded as "detection_thread"
def alert_detection():
    keyboard = Controller()
    while not flags['exit']:
        # Read for db changes
        db = read_db()
        
        # Check for monster
        if db['monster_appeared']:
            toggle(toggle_pause=False, pause=True)
            print_text('monster')
            press_keys(keyboard, 'm!fight ')
            
            # Wait for defeat
            while db['monster_appeared']:
                if flags['exit']:
                    return
                sleep(0.1)  # Wait for response
                db = read_db()
            print_text('defeat')
            toggle(toggle_pause=False, pause=False)

        # Check for repair
        elif db['repair_needed']:
            toggle(toggle_pause=False, pause=False)
            print_text('repair')
            # Wait for repair
            while db['repair_needed']:
                if flags['exit']:
                    return
                press_keys(keyboard, 'm!repair')
                press_keys(keyboard, [Key.enter])
                sleep(1)  # Reasonable time for bot to detect repair
                db = read_db()
            print_text('repaired')
            toggle(toggle_pause=False, pause=False)

            
def press_keys(keyboard, keys):
    for key in keys:
        keyboard.press(key)
        rand_sleep('key')
        keyboard.release(key)
        rand_sleep('key')


def check_exit(s):
    start = time()
    if s < 0:
        s = rand_sleep('macro', do_sleep=False)
    while time() < (start + s):
        if flags['exit']:
            return True
    return False


def rand_sleep(sleep_key, do_sleep=True):
    sleep_arr = execution_sleep[sleep_key]
    sleep_time = uniform(sleep_arr[0], sleep_arr[-1])
    if do_sleep:
        sleep(sleep_time)
        return
    return sleep_time


def print_text(argument):
    if argument == 'mine':
        global previous_time
        current_time = datetime.now()
        if not previous_time:
            previous_time = current_time
        diff_time = current_time - previous_time
        print("\u26cf" + "  " + str(current_time.time()) + 
              " : {}.{} seconds since last mine".format(diff_time.seconds, diff_time.microseconds))
        previous_time = current_time
        
    elif argument == 'defeat':
        print("Monster defeated!")
    elif argument == 'monster':
        print("Type the code to kill the monster!")
    elif argument == 'repair':
        print("Repairing pickaxe...")
    elif argument == 'repaired':
        print("Pickaxe repaired!")
    
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
    
    elif argument == 'instructions':
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


if __name__ == "__main__":
    previous_time = False

    mine_time = print_text('instructions')
    print_text('tutorial')

    mine_thread      = Thread(target=mine_macro)
    detection_thread = Thread(target=alert_detection)

    mine_thread.start()
    detection_thread.start()

    with Listener(on_press=on_press) as listener:
        listener.join()
    
    mine_thread.join()
    detection_thread.join()
    