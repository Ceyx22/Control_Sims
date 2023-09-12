from kinematics_2D import kinematics_2D
from UI import UI
from util import *
import PySimpleGUI as sg
import coms

#threading cannot be done in Py Simple GUI

def main():
    k = kinematics_2D()
    gui = UI(k)
    gui.plot_leg()
    while True:
        event, values = gui.read()
        print(event)
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        if event == "Update":
            print(values)
            new = np.array([float(values["x_pos"]), float(values["y_pos"])])
            print(new)
            k.inverse_kinmatics(new)
            print(k.get_pos())
            gui.update_plot()
            
            
if __name__ == "__main__":
    main()