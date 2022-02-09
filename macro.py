# Imported libraries
from pynput.keyboard import Key, Controller, Listener
from threading       import Thread
from datetime        import datetime
from time            import sleep, time
from random          import uniform

# Local libraries
from mine_config     import control_keys, flags, cmd_text, \
                            macro_sleep, key_sleep

start = datetime.now()


def monster_event():
    pass


def repair_event():
    pass

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
        if check_exit(mine_time + uniform(macro_sleep[0], macro_sleep[1]), flags): return
        if flags['running']:
            press_key(keyboard, 'm')
            press_key(keyboard, '!')
            press_key(keyboard, 'm')
            press_key(keyboard, Key.enter)
            print_mine()


def press_key(keyboard, key):
    keyboard.press(key)
    sleep(uniform(key_sleep[0], key_sleep[1]))
    keyboard.release(key)
    sleep(uniform(key_sleep[0], key_sleep[1]))


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
