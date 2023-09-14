from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib as mpt
import matplotlib.pyplot as plt

mpt.use("TkAgg")

class UI:
    def __init__(self, leg):
        self.fig = plt.figure()
        self.leg = leg
        self.figure_canvas_agg = None
        self.x_pos, self.y_pos = leg.get_pos()
        endefector_x, endefector_y = leg.get_current_target()
        self.layout =[
            [sg.Text("Plot test")],
            [sg.Canvas(key="canvas")],
            [sg.Text(text=f"Current x position: {endefector_x} Current y position: {endefector_y}")],
            [sg.Text('Input Desired X position of leg')], 
            [sg.InputText(key='x_pos')],
            [sg.Text('Input Desired Y position of leg')], 
            [sg.InputText(key='y_pos')],
            [sg.Button("Update", key='Update')],
        ]
        # Create the form and show it without the plot
        self.window = sg.Window(
            "Matplotlib Single Graph",
            self.layout,
            location=(0, 0),
            finalize=True,
            element_justification="center",
            font="Helvetica 18",
        )
        # self.update_available = False;
        # self.quit = False;
        # self.thread = threading.Thread(name="GUI thread", target=self.run)
        

    # def get_thread(self):
    #     return self.thread
        
    def plot_leg(self):
        plt.grid(color='purple', linestyle='-', linewidth=1)
        plt.plot(self.x_pos, self.y_pos, color='red')
        self.figure_canvas_agg = self.draw_figure(self.window['canvas'].TKCanvas, self.fig)

    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
    
    def update_plot(self):
        self.figure_canvas_agg.get_tk_widget().forget()
        self.update_coord()
        plt.clf()
        self.plot_leg()


    def close_window(self):
        self.window.close()

    def read(self):
        event, values = self.window.read()
        return event, values
    
    def update_coord(self):
        self.x_pos, self.y_pos = self.leg.get_pos()

if __name__ == "__main__":
    from kinematics_2D import kinematics_2D
    k = kinematics_2D()
    gui = UI(k)
    try:
        while True:
            print(gui.read())
    except Exception as e:
        print(repr(e))
        gui.close_window()
   

        

    
