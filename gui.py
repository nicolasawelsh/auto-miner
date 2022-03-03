import PySimpleGUI as sg
import subprocess
import sys



def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None

    retval = p.wait(timeout)
    return (retval, output)


# https://stackoverflow.com/questions/55910191/how-do-i-print-results-to-the-command-line-instead-of-a-popup-window-using-pysim
def main():
    sg.theme('DarkAmber')
    layout1 = [
        [sg.Text('Choose your deley between mining')],
        [sg.Button(2.5), sg.Button(3.0), sg.Button(3.5), 
         sg.Button(4.0), sg.Button(4.5), sg.Button(5.0)]
    ]
    layout2 = [
        [sg.Text('Enter the command you wish to run')],
        [sg.Input(key='_IN_', default_text='python3 discord_bot.py'), sg.Button('Run')],
        [sg.Output(size=(60,15))]
    ]
    toggle_layout = [[sg.Button('Start'), sg.Button('Pause')]]

    tabgrp = [
        [sg.TabGroup(
            [
                [sg.Tab('Config', layout1, 
                    border_width=10,
                    tooltip='Delay Configuration',
                    element_justification='center'),
                sg.Tab('Macro Logs', layout2,
                    border_width=10,
                    tooltip='Macro Logs',
                    element_justification='center')
                ]
            ],
            tab_location='centertop'),
        toggle_layout]
    ]

    window = sg.Window('Auto-Miner', tabgrp, 
                    element_justification='c', resizable=True, finalize=True)

    while True:
        event, values = window.Read()
        print(event, values)
        if event in (None, 'Exit'):
            break
        elif event == 'Run':
            runCommand(cmd=values['_IN_'], window=window)
    window.Close()

main()
