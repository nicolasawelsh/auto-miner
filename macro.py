# Imported libraries
from pynput.keyboard import Key, Controller, Listener
from threading       import Thread
from datetime        import datetime
from time            import sleep, time
from random          import uniform

# Local libraries
from config.pickle_db import read_db, build_db
from config.config    import control_keys, flags, cmd_text, \
                             execution_sleep


def on_press(key):
    if key == control_keys['toggle']:
        toggle()
    elif key == control_keys['exit']:
        flags['exit'] = True
        print_text('terminated')
        return False


def toggle(toggle=True, pause=False):
    if toggle:
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


def mine_macro(flags):
    keyboard = Controller()
    while not flags['exit']:
        overhead_start_time = time()

        sleep(2)  # Wait for messages
        try:        # Read for db changes
            db = read_db()
        except Exception as e:
            build_db()
            db = read_db()
        
        # Check for monster, wait for defeat
        if db['monster_appeared']:
            toggle(toggle=False, pause=True)
            print_text('monster')
            press_keys(keyboard, 'm!fight ')
            while db['monster_appeared']:
                sleep(0.1)  # Wait for response
                db = read_db()
            print_text('defeat')
            toggle(toggle=False, pause=False)
        # Check for repair, wait for success
        elif db['repair_needed']:
            toggle(toggle=False, pause=False)
            print_text('repair')
            press_keys(keyboard, 'm!repair')
            press_keys(keyboard, [Key.enter])
            rand_sleep('macro', do_sleep=True)
            while db['repair_needed']:
                sleep(0.1)
                db = read_db()
            print_text('repaired')
            toggle(toggle=False, pause=False)

        overhead_time = time() - overhead_start_time
        
        # Macro loop delay
        delay = mine_time + rand_sleep('macro', do_sleep=False) - overhead_time
        if check_exit(delay, flags): 
            return
        
        # Mine macro
        if flags['running']:
            press_keys(keyboard, 'm!m')
            press_keys(keyboard, [Key.enter])
            print_text('mine')


def press_keys(keyboard, keys):
    for key in keys:
        keyboard.press(key)
        rand_sleep('key')
        keyboard.release(key)
        rand_sleep('key')


def check_exit(s, flags):
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

    mine_thread = Thread(target=mine_macro, args=(flags,))
    mine_thread.start()

    with Listener(on_press=on_press) as listener:
        listener.join()
        
    mine_thread.join()
