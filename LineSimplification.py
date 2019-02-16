
from tkinter import *
from tkinter import filedialog  # to handle file manager windows for saving and loading
import os  # to get the current directory to set it as a default directory in file manager window
from Distance import Distance
from nthPoint import nthPoint
from GUIconnection import GUIconnection
from Pt import Pt

MAIN_DATA_FILE = 'MainlandUKoutline.csv'

class LineSimplification:
    """
    This class deals with all displaying aspects of the line simplification process.
    Master is a Tk object so it is used to create the window and frames and all other GUI related tasks.
    """

    listbox_index = None  # index of the user's chosen method in the listbox
    entry_box = '' # entery box to get parameter from the users
    current_data_dic = {} # the current revised/thined dictionary of points
    bottom_frame = '' # bottom side of the window where the map & canvas is displayed

    def __init__(self, master = None):
        """
        :param master: Tk object that will be used to create the GUI
        """
        self.master = master

    def scaleData(self, data_dic):
        """
        :param data_dic: a dictionary with points references as keys and tuples of (X,Y) as their values
        :return: a similar dictionary to the above dictionary but with scaled data so it suits the screen size better
        and a list of two items [X, Y] that will be used as width and height of the canvas in the next function.
        """

        scaled_data_dic = {}  # dictionary of scaled data
        canvas_size = []  # list containing the canvas width and height

        CANVAS_SCALE = 80   # Multiply each entry to this figure to enlarge the map
        MAX_SCREEN_Y = 800  # Max acceptable Y size, so the entire map fits on the screen
        EXTRA_SPACE_RATE = 0.04  # just to GIVE extra space around the map

        x_set = set()  # set of X values of the data
        y_set = set()  # set of Y values of the data
        for key in data_dic:
            x_set.add(data_dic[key][0])
            y_set.add(data_dic[key][1])
        x_range = [min(x_set), max(x_set)]   # Minimum & maximum X values
        y_range = [min(y_set), max(y_set)]   # Minimum & maximum Y values
        max_width = x_range[1] - x_range[0]  # Maximum data width
        max_height = y_range[1] - y_range[0] # Maximum data height
        canvas_width = CANVAS_SCALE * max_width
        canvas_height = CANVAS_SCALE * max_height
        if canvas_height > MAX_SCREEN_Y:  # If canvas height is bigger than maximum suitable size for screen it sets it as MAX_SCREEN_Y
            canvas_height = MAX_SCREEN_Y
            canvas_width = canvas_width * MAX_SCREEN_Y / canvas_height # adjusts canvas width accordingly

        canvas_size.append(canvas_width * (1 + EXTRA_SPACE_RATE))
        canvas_size.append(canvas_height * (1 + EXTRA_SPACE_RATE))

        for key in data_dic:  # the data is being scaled based on the size of the canvas so map fills the page
            scaled_data_dic[key] = ((data_dic[key][0] - x_range[0]) * canvas_width / max_width +
                                    EXTRA_SPACE_RATE / 2 * canvas_size[0],)  # last part just to move the map to the middle
            scaled_data_dic[key] = scaled_data_dic[key] + (canvas_size[1] - ((data_dic[key][1] - y_range[0]) *
                                    canvas_height / max_height) - EXTRA_SPACE_RATE / 2 * canvas_size[1],)

        return canvas_size, scaled_data_dic

    def displayWindow(self):
        """
        :return: Displays the main window with menu bar, listbox, entry box, button, labels and all the functionalities.
        There are two frames, one for the top part and their functionalities, which will be done in this function and
        the second one which contains the canvas with the map. The second part will be defined in the next function, displayMap.
        """

        top_frame = Frame(self.master)  # top frame
        top_frame.pack(side = TOP, fill=X)

        separator = Frame(self.master, height=5, bd=1, background='black') # to separate top frame from the bottom
        separator.pack(fill=X, padx=5, pady=5)

        self.the_label = Label(top_frame, text='Select Method') # Select Method label
        self.the_listbox = Listbox(top_frame, height = 3, width = 12) # The list box containing the availanle methods
        self.entrybox_label_1 = Label(top_frame, text='min distance') # Label associated with distance method
        self.entrybox_label_2 = Label(top_frame, text='n = ') # Label associated with nth point method

        def on_select(event):
            """
            To bind the method selection with displaying the relevant labels next to entry box.
            """
            listbox_list = event.widget.curselection()
            self.entrybox_label_1.grid_remove() # to remove the previously displayed label 1 if there is any
            self.entrybox_label_2.grid_remove() # to remove the previously displayed label 2 if there is any

            if listbox_list[0] == 0:
                self.entrybox_label_1.grid(row=0, column=2, sticky=E) # display the relevant label next to entry box
                LineSimplification.listbox_index = 0 # class variable so can be traced later for alocating relevant object
            elif listbox_list[0] == 1:
                self.entrybox_label_2.grid(row=0, column=2, sticky=E) # display the relevant label next to entry box
                LineSimplification.listbox_index = 1 # class variable so can be traced later for alocating relevant object
            else: # new labels can be added for new methods
                pass

        plugins_file_list = []  # list of available methods extracted from the plugins text file using displayName method
        for subclass_name in [Distance(), nthPoint()]:
            the_object = subclass_name
            plugins_file_list.append(the_object.displayName()) # Uses displayName method of different subclasses to get the method name

        for item in plugins_file_list:  # add the method names to the listbox
            self.the_listbox.insert(END, item)
        self.the_listbox.bind('<<ListboxSelect>>', on_select) # binds the selected method with displaying the relevant label

        LineSimplification.entry_box = Entry(top_frame, width = 10) # entry box to receive the parameter from the user, class variable
        the_button = Button(top_frame, text='Process', command = self.processData) # button sets to triger processData to process data anddisplay the map

        self.the_listbox.configure(background='grey', highlightbackground='black', highlightthickness=1)
        LineSimplification.entry_box.configure(background='grey', highlightbackground='black', highlightthickness=1)
        the_button.configure(background='grey', highlightthickness=1)

        self.the_label.grid(row=0, column=0, sticky=W) # griding, similar method to packing, the label to the frame
        self.the_listbox.grid(row=0, column=1, sticky=W + S) # griding the listbox to the frame
        self.entrybox_label_1.grid(row=0, column=2, sticky=E) # griding entrybox label 1 as the default label
        LineSimplification.entry_box.grid(row=0, column=3, sticky=W) # griding the entry box to the frame
        the_button.grid(row=0, column=4, sticky=W) # griding the process button to the frame

        top_frame.grid_columnconfigure(0, minsize=120)  # column sizes
        top_frame.grid_columnconfigure(1, minsize=150)
        top_frame.grid_columnconfigure(2, minsize=130)
        top_frame.grid_columnconfigure(3, minsize=130)
        top_frame.grid_columnconfigure(4, minsize=80)
        top_frame.grid_rowconfigure(0, minsize=60)

        window_menu = Menu(self.master) # to set the menu containing File as sub menu
        self.master.config(menu=window_menu)
        window_submenu = Menu(window_menu)
        window_menu.add_cascade(label="File", menu=window_submenu)
        window_submenu.add_command(label="Save", command=self.saveData) # adds Save command to the menu
        window_submenu.add_command(label="Load", command=self.loadData) # adds Load command to the menu

        return self.the_listbox

    def displayMap(self, data_dic):
        """
        :param data_dic: receives a dictionary of points with references as keys and tuple of (X, Y) as their values.
        :return: displays the second frame which uses the data it receives to display the map on a canvas. The canvas is
        displayed on the second frame, bottom_frame, which is a class variable.
        """

        canvas_size = self.scaleData(data_dic)[0]  # uses scaleData function to get the canvas size

        try:
            LineSimplification.bottom_frame.destroy()  # to remove any existing canvas on the frame, if there is any
        except:
            pass

        LineSimplification.bottom_frame = Frame(self.master) # create the bottom frame
        LineSimplification.bottom_frame.pack(side=BOTTOM)
        the_canvas = Canvas(LineSimplification.bottom_frame, width=canvas_size[0], height=canvas_size[1])
        the_canvas.pack()

        scaled_dic = self.scaleData(data_dic)[1]  # uses scaleData function to scale the data so it suits the window size

        points_list = [] # the list of tuples canvas will uses to connect the points together, list format [(x1,y1),(x2,y2),...]
        for i in range(1, len(scaled_dic) + 1): # update the list according to the scaled data dictionary
            points_list.append(scaled_dic[i])

        my_polygon = the_canvas.create_polygon(points_list, outline='black', fill='')  #displays the image
        return the_canvas

    def processData(self):
        """
        This function is called when user presses the process button. The program checks what method has been selected
        by the user and based on that an object of the appropriate class will be created. The users input in the entry box
        is also collected.
        :return: Processes the data, displays the map saves the data dictionary as the current dictionary so the process
        can be done with the new data from now on.
        """

        if LineSimplification.listbox_index == 0: # Index 0 of the listbox, shows the Distance method has been selected
            the_object = Distance()  # An object of appropriate class is created
        elif LineSimplification.listbox_index == 1: # Index 1 of the listbox, shows the nthPoint method has been selected
            the_object = nthPoint()  # An object of appropriate class is created
        elif LineSimplification.listbox_index == None: # no method has been selected yet
             print('Please select a method')
        else: # more objects can be added if there are more methods available
            pass


        def repeatProcess(data_dictionary, parameter):
            """
            Calls thinPoints method (chooses the appropriate class based on the object - Poymorphism) to return a
            revised dictionary.
            :param data_dictionary: gets a dictionary of points
            :param parameter: gets the parameter required to reduce the data either the distance or the number of points to skip
            :return: calls thinPoints method to remove the appropriate points and return a smaller dictionary
            """
            revised_dic = the_object.thinPoints(data_dictionary, parameter) # using thinPoints method returns new dictionary
            new_window = self.displayMap(revised_dic) # displays a new map based on the new dictionary by calling displayMap method
            return revised_dic

        the_entry = LineSimplification.entry_box.get()  # gets the entry by the user

        if LineSimplification.listbox_index != None:
            try:
                users_entry = float(the_entry)
                LineSimplification.current_data_dic = repeatProcess(LineSimplification.current_data_dic,
                                                                    users_entry)  # the class variable dic changes to the new dictionary
            except ValueError: # asks users to enter valid numbers instead of letters, characters, leaving it empty or entering invalid numebr
                print('Please enter a valid number')

    def saveData(self):
        """
        :return: Saves the current data in the excat format as the original one. Uses the filedialog library to display
        file manager window to ask users for the name and directory. The default directory is set to be the current
        working directory.
        """
        default_directory = os.getcwd()
        file_name_dir = filedialog.asksaveasfilename(initialdir=default_directory) + '.csv'
        new_file = open(file_name_dir, "w")
        line_content = ''
        for key in LineSimplification.current_data_dic:
            line_content = '"' + str(key) + '"' + ',' + str(LineSimplification.current_data_dic[key][0]) + ',' \
                           + str(LineSimplification.current_data_dic[key][1]) + '\n' # turns the current dictionary to the original data format
            new_file.write(line_content) # writes the data line by line
        new_file.close()

    def loadData(self):
        """
        :return: Gets a file name from the user and reads the data and process it the same way as processing the original
        data file. It process the data and displays the window and the map in the same state as when it was saved. Uses the
        filedialog library to display file manager window to ask users for the name of the file. The default directory
        is set to be the current working directory.
        """
        default_directory = os.getcwd()
        loaded_file = filedialog.askopenfilename(initialdir=default_directory, title="Select file")
        new_class = Distance()
        LineSimplification.current_data_dic = initial_object.makeDic(loaded_file)
        load_window = self.displayMap(LineSimplification.current_data_dic)

initial_object = Distance() # to be able to use the makeDic method in Distance class
LineSimplification.current_data_dic = initial_object.makeDic(MAIN_DATA_FILE) # to turn the initial data into the dictionary format

the_window = Tk()
the_window.title('Line Simplification')
page = LineSimplification(the_window) # sets the page to be an object of the LineSimplification class

windows_top = page.displayWindow() # displays the top side of the initial window

try: # to deal with a situation where an error such as IOError was raised, no file was found and no initial data dictionary was made
    windows_bottom = page.displayMap(LineSimplification.current_data_dic) # uses displayMap method to display the initial map
    the_window.mainloop()
except:
    pass # If it can't display one frame (for instance due to having no data in data dictionary) it doesn't run the loop so it doesn't display the window at all.