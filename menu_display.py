import tkinter
from tkinter import ttk
import settings
import sys
import ast

class EntryBox(tkinter.Frame):
    def __init__(self, parent, label, variable, bg = '#c1c1bf'):
        tkinter.Frame.__init__(self, parent, bg = bg)
        self.variable = variable
        self.entrybox = tkinter.ttk.Entry(self, textvariable = self.variable, font = ('Arial', 16), width = 5)
        if label:
            self.label = tkinter.Label(self, text = label, font = ('Arial', 15), bg = bg)
            self.label.pack(side = tkinter.LEFT, padx = (0,5))
        self.entrybox.pack(side = tkinter.LEFT)

class DropBox(tkinter.Frame):
    def __init__(self, parent, label, values, variable, bg = '#c1c1bf'):
        tkinter.Frame.__init__(self, parent, bg = bg)
        self.variable = variable
        self.dropbox = tkinter.ttk.Combobox(self, textvariable = self.variable, values = values, font = ('Arial', 16), state = 'readonly', width = 15)
        if label:
            self.label = tkinter.Label(self, text = label, font = ('Arial', 15), bg = bg)
            self.label.pack(side = tkinter.LEFT, padx = (0,5))
        self.dropbox.pack(side = tkinter.LEFT)

class ScrollBox(tkinter.Frame):
    def __init__(self, parent, title, label1, label2, defaults, bg = '#c1c1bf'):
        tkinter.Frame.__init__(self, parent, bg = bg)
        self.bg = bg
        self.values = defaults
        self.submissions = {}
        if title:
            self.title = tkinter.Label(self, text = title, font = ('Arial', 20), bg = bg)
            self.title.pack(side = 'top')
        self.entry_frame = tkinter.Frame(self, bg = bg)
        self.entry_frame.pack(side = 'top', pady = 10)
        self.entry_frame.grid_columnconfigure((0, 1, 2), pad = 10)
        self.entry1 = EntryBox(parent = self.entry_frame, label = label1, variable = tkinter.StringVar(), bg = bg)
        self.entry1.grid(row = 0, column = 0)
        self.entry2 = EntryBox(parent = self.entry_frame, label = label2, variable = tkinter.StringVar(), bg = bg)
        self.entry2.grid(row = 0, column = 1)
        self.add_button = tkinter.Button(self.entry_frame, text = 'Add', font = ('Arial', 16), command = self.add_pressed)
        self.add_button.grid(row = 0, column = 2)
        self.canvas = ScrollFrame(parent = self, size = (250, 150))
        self.canvas.pack(side = 'top')
        for default in self.values.keys():
            self.submit(default, self.values[default])

    def add_pressed(self):
        if ast.literal_eval(self.entry1.variable.get()) in self.values:
            pass
        else:
            self.submit(ast.literal_eval(self.entry1.variable.get()), ast.literal_eval(self.entry2.variable.get()))

    def submit(self, value1, value2):
        sub_frame = tkinter.Frame(self.canvas.frame, bg = self.bg)
        sub_frame.pack(side = 'top', expand = True, fill = 'both')
        label = tkinter.Label(sub_frame, text = '{} : {}'.format(value1, value2), font = ('Arial', 16), bg = self.bg)
        label.pack(expand = True, fill = 'both', side = 'left')
        button = SpecifiedButton(sub_frame, text = 'Remove', key = value1, function = self.remove)
        button.pack(padx = 20, side = 'left')
        self.submissions[value1] = sub_frame
        self.values[value1] = value2

    def remove(self, key):
        self.submissions.pop(key).destroy()
        self.values.pop(key)

class SpecifiedButton(tkinter.Button):
    def __init__(self, parent, text, key, function):
        tkinter.Button.__init__(self, parent, text = text, command = self.pressed)
        self.key = key
        self.function = function

    def pressed(self):
        self.function(self.key)

class ScrollFrame(tkinter.Frame):
    def __init__(self, parent, size, bg = '#c1c1bf'):
        tkinter.Frame.__init__(self, parent, bg = bg, bd = 5, relief = 'sunken')
        self.canvas = tkinter.Canvas(self, borderwidth=0, highlightthickness = 0, height = size[1], width = size[0], bg = bg)
        self.frame = tkinter.Frame(self.canvas, bg = bg)
        self.scrollbar = tkinter.Scrollbar(self, orient = 'vertical', command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        self.scrollbar.pack(side = 'right', fill = 'y')
        self.canvas.pack(side = 'left', padx = (10, 0), pady = 10)
        self.canvas.create_window((size[0]/2, 5), anchor = 'n', window = self.frame, tags = 'self.frame')
        self.frame.bind('<Configure>', self.configure_call)

    def configure_call(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox('all'))

class MenuManager:
    def __init__(self, root,  bigboss, size = (750, 750)):
        self.bigboss = bigboss
        self.size = size
        self.root = root
        self.create_title_screen()

    def quit_program(self):
        sys.exit(0)

    def create_title_screen(self):
        self.title_screen = TitleScreen(parent = self.root, size = self.size, boss = self)
        self.title_screen.pack()

    def create_game_mode_menu(self):
        self.game_mode_menu = GameModeMenu(parent = self.root, size = self.size, boss = self)
        self.game_mode_menu.pack()

    def create_settings_menu(self):
        self.settings_menu = SettingsWindow(parent = self.root, size = self.size, boss = self, settings = settings.layout, order = settings.order, defaults = settings.presets['NES_Level19']['settings'])
        self.settings_menu.pack()

class TitleScreen(tkinter.Frame):
    def __init__(self, parent, size, boss):
        self.boss = boss
        tkinter.Frame.__init__(self, parent)
        self.name = tkinter.Label(self, text = 'TETRIS SIMULATOR', font = ("Arial", 50))
        self.name.grid(column = 0, row = 0, padx = 50, pady = 50)
        self.new_game_button = tkinter.Button(self, text = 'NEW GAME', font = ("Arial", 30), bd = 5, command = self.new_game_pressed)
        self.new_game_button.grid(column = 0, row = 1, padx = 50, pady = 20)
        self.quit_button = tkinter.Button(self, text = 'QUIT', font = ("Arial", 30), bd = 5, command = self.quit_pressed)
        self.quit_button.grid(column = 0, row = 2, padx = 50, pady = 20)

    def new_game_pressed(self):
        self.destroy()
        self.boss.create_game_mode_menu()

    def quit_pressed(self):
        self.boss.quit_program()

class GameModeMenu(tkinter.Frame):
    def __init__(self, parent, size, boss):
        tkinter.Frame.__init__(self, parent)
        self.boss = boss
        self.size = size
        self.top = tkinter.Frame(self)
        self.top.pack(side = tkinter.TOP)
        self.title = tkinter.Label(self.top, text = 'Game Mode', font = ("Arial", 30))
        self.title.pack(pady = (10, 30))
        self.middle = tkinter.Frame(self)
        self.middle.pack(side = tkinter.TOP, fill = tkinter.X)
        self.footer = tkinter.Frame(self)
        self.footer.pack(side = tkinter.BOTTOM, fill = tkinter.X)
        self.next_button = tkinter.Button(self.footer, text = 'Next', font = ('Arial', 16), bd = 3, command = self.next_pressed)
        self.next_button.pack(side = tkinter.RIGHT, padx = 10, pady = 10)
        self.back_button = tkinter.Button(self.footer, text = 'Back', font = ('Arial', 16), bd = 3, command = self.back_pressed)
        self.back_button.pack(side = tkinter.LEFT, padx = 10, pady = 10)
        self.bottom = tkinter.Frame(self)
        self.bottom.pack(side = tkinter.BOTTOM)
        self.description = (
        'Choose your game mode.\n\n'
        '"Standard" mode matches the mechanics of most commerical Tetris games, where a piece will fall from the top of the screen and '
        'eventually lock into place. Once locked, the tiles can only be altered by a line clear.\n\n'
        '"Point and Click" mode allows you to place pieces at your own leisure using a mouse. Top-outs are impossible, and a '
        'move record is creared as you play, allowing past moves to be reviewed. Piece type can be manually selected if desired.'
        )
        self.create_description_label(self.description)
        self.mode_variable = tkinter.StringVar(value = 'standard')
        self.standard_button = tkinter.Radiobutton(self.middle, text = 'Standard', variable = self.mode_variable, value = 'standard', indicatoron = 0, font = ('Arial', 25), bd = 5)
        self.standard_button.grid(column = 0, row = 0)
        self.pointclick_button = tkinter.Radiobutton(self.middle, text = 'Point and Click', variable = self.mode_variable, value = 'pointclick', indicatoron = 0, font = ('Arial', 25), bd = 5)
        self.pointclick_button.grid(column = 1, row = 0)
        self.middle.grid_rowconfigure(0, weight = 1)
        self.middle.grid_columnconfigure(0, weight = 1)
        self.middle.grid_columnconfigure(1, weight = 1)

    def create_description_label(self, description):
        self.description_label = tkinter.Label(self.bottom, text = description, justify = tkinter.LEFT, font = ("Arial", 16), wraplength = self.size[1] - 60)
        self.description_label.pack(pady = 30, padx = 30)

    def back_pressed(self):
        self.destroy()
        self.boss.create_title_screen()

    def next_pressed(self):
        if self.mode_variable.get() == 'standard':
            self.boss.pointclick = False
        else:
            self.boss.pointclick = True
        self.destroy()
        self.boss.create_settings_menu()

class SettingsWindow(tkinter.Frame):
    def __init__(self, parent, size, boss, settings, order, defaults):
        tkinter.Frame.__init__(self, parent, bd = 3)
        self.settings = settings
        self.order = order
        self.defaults = defaults
        self.boss = boss
        self.size = size
        self.settings_title = tkinter.Label(self, text = 'Settings', font = ("Arial", 30))
        self.settings_title.grid(row = 0, column = 0)
        self.descr_title = tkinter.Label(self, text = 'Description', font = ("Arial", 30))
        self.descr_title.grid(row = 0, column = 1)
        self.settings_canvas = ScrollFrame(self, size = (400, 450), bg = '#c1c1bf')
        self.settings_canvas.grid(row = 1, column = 0, padx = 10)
        self.text_canvas = ScrollFrame(self, size = (400, 450), bg = '#c1c1bf')
        self.text_canvas.grid(row = 1, column = 1, padx = 10)
        self.footer = tkinter.Frame(self)
        self.footer.grid(row = 2, column = 0, columnspan = 2)
        self.grid_columnconfigure((0, 1), weight = 1)
        self.next_button = tkinter.Button(self.footer, text = 'Next', font = ('Arial', 16), bd = 3, command = self.next_pressed)
        self.next_button.pack(side = tkinter.RIGHT, padx = 10, pady = 10)
        self.back_button = tkinter.Button(self.footer, text = 'Back', font = ('Arial', 16), bd = 3, command = self.back_pressed)
        self.back_button.pack(side = tkinter.LEFT, padx = 10, pady = 10)
        self.populate_settings()

    def populate_settings(self):
        self.variables = {}
        self.var_dicts = {}
        self.widgets = {}
        for setting in self.order:
            attr = self.settings[setting]
            if attr['type'] == 'dropbox':
                self.variables[setting] = tkinter.StringVar(value = str(self.defaults[setting]))
                self.widgets[setting] = DropBox(parent = self.settings_canvas.frame, label = attr['label'], values = attr['values'], variable = self.variables[setting])
            elif attr['type'] == 'entry':
                self.variables[setting] = tkinter.StringVar(value = str(self.defaults[setting]))
                self.widgets[setting] = EntryBox(parent = self.settings_canvas.frame, label = attr['label'], variable = self.variables[setting])
            elif attr['type'] == 'scroll':
                self.var_dicts[setting] = self.defaults[setting].copy()
                self.widgets[setting] = ScrollBox(parent = self.settings_canvas.frame, title = attr['title'], label1 = attr['label1'], label2 = attr['label2'], defaults = self.var_dicts[setting])
            self.widgets[setting].pack(side = 'top', pady = 10, expand = True, fill = 'both')

    def process_settings(self):
        self.setting_output = {}
        for setting in self.variables.keys():
            try:
                self.setting_output[setting] = ast.literal_eval(self.variables[setting].get())
            except ValueError:
                self.setting_output[setting] = self.variables[setting].get()
            if self.settings[setting]['type'] == 'dropbox':
                self.setting_output[setting] = self.settings[setting]['assets'][self.variables[setting].get()]
        for setting in self.var_dicts.keys():
            self.setting_output[setting] = self.var_dicts[setting].copy()

    def next_pressed(self):
        self.process_settings()
        if self.boss.pointclick == True:
            self.boss.bigboss.run_pointclick()
        else:
            self.boss.bigboss.run_simulator()

    def back_pressed(self): pass
