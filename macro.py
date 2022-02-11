# Imported libraries
from pynput.keyboard import Key, Controller, Listener
from threading       import Thread
from datetime        import datetime
from time            import sleep, time
from random          import uniform

# Local libraries
from mine_config     import control_keys, flags, cmd_text, \
                            macro_sleep, key_sleep
from discord_bot     import monster, repair


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


def mine_macro(flags):
    keyboard = Controller()
    while not flags['exit']:
        if check_exit(mine_time + rand_sleep(macro_sleep, do_sleep=False), flags): return
        flags['monster'] = monster
        if flags['running']:
            press_keys(keyboard, 'm!m')
            press_key(keyboard, Key.enter)
            print_text('mine')


def repair_macro(flags):
    keyboard = Controller()
    while not flags['exit']:
        if check_exit(0, flags): return
        flags['repair'] = repair
        if flags['repair'] and flags['running']:
            press_keys(keyboard, 'm!repair')
            press_key(keyboard, Key.enter)
            print_text('repair')


def press_key(keyboard, key):
    keyboard.press(key)
    rand_sleep(key_sleep)
    keyboard.release(key)
    rand_sleep(key_sleep)


def press_keys(keyboard, key_str):
    for key in key_str:
        keyboard.press(key)
        rand_sleep(key_sleep)
        keyboard.release(key)
        rand_sleep(key_sleep)


def check_exit(s, flags):
    start = time()
    while time() < (start + s):
        if flags['exit']:
            return True
    return False


def rand_sleep(range_arr, do_sleep=True):
    sleep_time = uniform(range_arr[0], range_arr[-1])
    if do_sleep:
        sleep(sleep_time)
    return sleep_time


def print_text(argument):
    if argument == 'mine':
        print("\u26cf", end="  ")
        print(datetime.now().time())
    elif argument == 'repair':
        print("Pickaxe repaired!")
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

    mine_thread = Thread(target=mine_macro, args=(flags,))
    mine_thread.start()

    repair_thread = Thread(target=repair_macro, args=(flags,))
    repair_thread.start()

    with Listener(on_press=on_press) as listener:
        listener.join()
        
    mine_thread.join()
    repair_thread.join()
