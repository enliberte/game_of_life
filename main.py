from tkinter import *


class Point(Button):
    states = None
    size = 0

    @classmethod
    def define_size(cls, size):
        cls.size = size
        cls.states = [[False for row in range(size)] for column in range(size)]

    @classmethod
    def get_alive_count(cls):
        states_list = []
        for row in cls.states:
            states_list += row
        return states_list.count(True)

    def __init__(self, master, row, column):
        self.is_alive = False
        self.row = row
        self.column = column
        self.is_alive_next_turn = False
        self.alive_neighbours_count = 0
        super().__init__(master, height=1, width=1, bg='white', command=lambda: self.click())

    def click(self):
        self.is_alive = not self.is_alive
        self.change_state()
        self.color()

    def live(self):
        self.is_alive = True
        self.color()

    def die(self):
        self.is_alive = False
        self.color()

    def color(self):
        color = 'black' if self.is_alive else 'white'
        self.configure(bg=color)

    def count_alive_neighbours(self):
        self.alive_neighbours_count = 0
        next_row = 0 if self.row == self.size - 1 else self.row + 1
        next_column = 0 if self.column == self.size - 1 else self.column + 1
        self.alive_neighbours_count += self.states[self.row - 1][self.column - 1]
        self.alive_neighbours_count += self.states[self.row][self.column - 1]
        self.alive_neighbours_count += self.states[next_row][self.column - 1]
        self.alive_neighbours_count += self.states[self.row - 1][self.column]
        self.alive_neighbours_count += self.states[next_row][self.column]
        self.alive_neighbours_count += self.states[self.row - 1][next_column]
        self.alive_neighbours_count += self.states[self.row][next_column]
        self.alive_neighbours_count += self.states[next_row][next_column]

    def define_state(self):
        self.count_alive_neighbours()
        if not self.is_alive and self.alive_neighbours_count == 3:
            self.live()
        if self.is_alive and (self.alive_neighbours_count < 2 or self.alive_neighbours_count > 3):
            self.die()

    def change_state(self):
        self.states[self.row][self.column] = self.is_alive


class GameField:
    def __init__(self):
        self.size = 0
        self.points = {}
        self.window = Tk()
        self.window.wm_title('Game of Life')
        self.window.geometry('800x600')
        self.points_frame = Frame(self.window)
        self.game_is_over_label = Label(self.window, text='Game is over')
        self.size_label = Label(self.window, text='Please insert game field size')
        self.size_entry = Entry(self.window)
        self.create_btn = Button(self.window,
                                 text='Create a game field',
                                 command=lambda: self.draw_field(int(self.size_entry.get())))
        self.start_btn = Button(self.window, text='Start', command=lambda: self.turn())
        self.show_menu()
        self.window.mainloop()

    def initials(self):
        self.size = 0
        self.points = {}

    def show_menu(self):
        self.size_label.pack()
        self.size_entry.pack()
        self.create_btn.pack()

    def hide_menu(self):
        self.size_entry.pack_forget()
        self.size_label.pack_forget()
        self.create_btn.pack_forget()

    def draw_field(self, size):
        self.points_frame.pack()
        self.size = size
        self.hide_menu()
        Point.define_size(self.size)
        for row in range(self.size):
            for column in range(self.size):
                self.points['Point%s%s' % (row, column)] = Point(self.points_frame, row, column)
                self.points['Point%s%s' % (row, column)].grid(row=row, column=column)
        self.start_btn.pack()

    def turn(self):
        self.start_btn.pack_forget()
        self.window.after(500, self.turn)
        for point in self.points.values():
            point.define_state()
        for point in self.points.values():
            point.change_state()
        if Point.get_alive_count() == 0:
            # self.show_menu()
            self.game_is_over_label.pack()
            self.points_frame.pack_forget()
            self.initials()
            self.start_btn.pack_forget()


field = GameField()
