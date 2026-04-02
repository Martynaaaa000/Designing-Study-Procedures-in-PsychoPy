from psychopy import visual, core, monitors, gui
from psychopy.hardware import keyboard

import os
import time

import logging

logging.basicConfig(level=logging.INFO)

script_path = os.path.abspath(os.path.dirname(__file__))

results_path = script_path + '/Results/'

os.makedirs(results_path, exist_ok=True)

def save_gui_data(gui_data: dict):
    
    #for key in gui_data:
    #    ...
    
    string_gui_data = ''
    
    for key, value in gui_data.items():
        string_gui_data += f'{key}: {value}\n'
    
    participant_id = gui_data['Participant ID']
    
    experiment_timestamp = time.strftime('%Y-%m-%d_%H-%M', time.gmtime())
    
    #with open('C:/Users/student/Documents/gui_data.txt', 'w', encoding='utf-8') as file:
    with open(results_path + f'gui_data_{participant_id}_{experiment_timestamp}.txt', 'w', encoding='utf-8') as file:
        file.write(string_gui_data)

def collect_gui_data():
    
    gui_dict = {'Participant ID': '',
                'Handedness': ['Left', 'Right', 'Ambidextrous'],
                'Number of trials': 10}
    
    gui_window = gui.DlgFromDict(gui_dict, title = 'Test title', sortKeys = False, show = False)
    
    while True:
    
        gui_data = gui_window.show()
        
        control_condition = len(gui_data['Participant ID']) > 0 and 'id' in gui_data['Participant ID']
        
        if gui_window.OK:
            if control_condition:
                logging.info(f'Collected gui data: {gui_data}')
                save_gui_data(gui_data)
                return
            else:
                warning_window = gui.Dlg(title='Warning!')
                warning_message = 'Participant ID missing!'
                warning_window.addText(warning_message)
                warning_data = warning_window.show()
        else:
            core.quit()

def experiment():
    #create a window
    
    for monitor in monitors.getAllMonitors():
        logging.info(monitor)
        
    logging.info(monitors.Monitor('testMonitor').getSizePix())
    
    collect_gui_data()
        
    win_width = monitors.Monitor('testMonitor').getSizePix()[0]
    win_height = monitors.Monitor('testMonitor').getSizePix()[1]
    
    mywin = visual.Window([win_width,win_height],fullscr = True, monitor="testMonitor", color = 'green', units="deg")
     
    #create some stimuli
    grating = visual.GratingStim(win=mywin, mask="circle", size=3, pos=[-4,0], sf=3)
    fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0,0], sf=0, rgb=-1)

    #create a keyboard component
    kb = keyboard.Keyboard()

    #draw the stimuli and update the window
    grating.draw()
    #fixation.draw()
    mywin.update()

    #pause, so you get a chance to see it!
    core.wait(2.0)

if __name__ == "__main__":
    experiment()