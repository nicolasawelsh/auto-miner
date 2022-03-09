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
    layout = [
        [sg.Multiline(size=(110, 30), echo_stdout_stderr=True, reroute_stdout=True, autoscroll=True, background_color='black', text_color='white', key='-MLINE-')],
        [sg.T('Promt> '), sg.Input(key='-IN-', focus=True, do_not_clear=False)],
        [sg.Button('Run', bind_return_key=True), sg.Button('Exit')]]

    window = sg.Window('Realtime Shell Command Output', layout)
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Run':
            sp = sg.execute_command_subprocess(values['-IN-'], pipe_output=True, wait=False)
            results = sg.execute_get_results(sp)
            print(results[0])

    window.close()


main()