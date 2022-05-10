# Imports.
import random
import tkinter as tk
import time


# Classes.
class Menu:
    """Menu class."""

    def __init__(self, gui):
        """
        Initialise.

        :param gui:
        """
        self.window = gui.window

        self.menu_canvas = tk.Canvas(self.window, width=GUI.CANVAS_WIDTH,
                                     height=GUI.CANVAS_HEIGHT, bg="cyan")
        self._menu_label = tk.Label(self.menu_canvas, text="Flappy Bird",
                                    width=10, height=2)
        self._menu_label.place(x=GUI.CANVAS_WIDTH / 2,
                               y=GUI.CANVAS_HEIGHT * 2 / 8, anchor="center")
        self._start_button = tk.Button(self.menu_canvas, text="Start game",
                                       width=10, height=2, bg="yellow",
                                       command=gui.show_game)
        self._start_button.place(x=GUI.CANVAS_WIDTH / 2,
                                 y=GUI.CANVAS_HEIGHT * 4 / 8, anchor="center")
        self._quit_button = tk.Button(self.menu_canvas, text="Quit",
                                      width=10, height=2, bg="yellow",
                                      command=self.window.destroy)
        self._quit_button.place(x=GUI.CANVAS_WIDTH / 2,
                                y=GUI.CANVAS_HEIGHT * 5 / 8, anchor="center")

    def show_menu_canvas(self):
        """
        Show menu.

        :return:
        """
        self.menu_canvas.pack()

    def hide_menu_canvas(self):
        """
        Hide menu.

        :return:
        """
        self.menu_canvas.pack_forget()


class GameOver:
    """Game over class."""

    def __init__(self, gui):
        """
        Initialise.

        :param gui:
        """
        self.window = gui.window
        self.gui = gui

        self.game_over_canvas = tk.Canvas(self.window, width=GUI.CANVAS_WIDTH,
                                          height=GUI.CANVAS_HEIGHT, bg="cyan")
        self._game_over_label = tk.Label(self.game_over_canvas,
                                         text="Game Over", width=10, height=2)
        self._game_over_label.place(x=GUI.CANVAS_WIDTH / 2,
                                    y=GUI.CANVAS_HEIGHT * 2 / 8,
                                    anchor="center")
        self._end_score_label = tk.Label(self.game_over_canvas, text="",
                                         width=10, height=2)
        self._end_score_label.place(x=GUI.CANVAS_WIDTH / 2,
                                    y=GUI.CANVAS_HEIGHT * 3 / 8,
                                    anchor="center")
        self._restart_button = tk.Button(self.game_over_canvas,
                                         text="Restart", width=10,
                                         height=2, bg="yellow",
                                         command=gui.show_game)
        self._restart_button.place(x=GUI.CANVAS_WIDTH / 2,
                                   y=GUI.CANVAS_HEIGHT * 4 / 8,
                                   anchor="center")
        self._back_button = tk.Button(self.game_over_canvas,
                                      text="Back To Menu", width=10,
                                      height=2, bg="yellow",
                                      command=gui.show_menu)
        self._back_button.place(x=GUI.CANVAS_WIDTH / 2,
                                y=GUI.CANVAS_HEIGHT * 5 / 8, anchor="center")

    def show_game_over_canvas(self):
        """
        Show game over.

        :return:
        """
        self._end_score_label.config(text="Score: " + str(self.gui.game.score))
        self.game_over_canvas.pack()

    def hide_game_over_canvas(self):
        """
        Hide game over.

        :return:
        """
        self.game_over_canvas.pack_forget()


class Game:
    """Game class."""

    _REFRESH_RATE = 10
    X_BIRD_START_POSITION = 50
    GAP_BETWEEN_PIPES = 200
    GAP_RANGE = [200, 350]
    _first_pipe_distance = 600
    _pipe_x_positions = [_first_pipe_distance,
                         _first_pipe_distance + GAP_BETWEEN_PIPES,
                         _first_pipe_distance + 2 * GAP_BETWEEN_PIPES,
                         _first_pipe_distance + 3 * GAP_BETWEEN_PIPES]

    def __init__(self, gui):
        """
        Initialise.

        :param gui:
        """
        # gui object is
        self.gui = gui
        self.window = gui.window
        self.score = 0

        self._game_started = False

        # Create canvas.
        self.canvas = tk.Canvas(self.window, width=GUI.CANVAS_WIDTH,
                                height=GUI.CANVAS_HEIGHT, bg="cyan")

        # Create score.
        self._score_text = self.canvas.create_text(GUI.CANVAS_WIDTH / 2,
                                                   GUI.CANVAS_HEIGHT / 2,
                                                   font=("Comic sans", 80),
                                                   fill="white",
                                                   text=str(self.score))

        # Create player.
        self._player = Bird(self, self.window, self.canvas,
                            Game.X_BIRD_START_POSITION)

        self._pipe_list = []

        # Create pipes.
        for pipe_position in Game._pipe_x_positions:
            self._pipe_list.append(Pipe(self, random.randint(
                Game.GAP_RANGE[0], Game.GAP_RANGE[1]), pipe_position))

        # Key bind mouse click and space button.
        self.canvas.focus_set()
        self.canvas.bind('<Button-1>', lambda event: self._player.flap(event))
        self.canvas.bind("<Key>", self._player.flap)

    def add_score(self):
        """
        Add score.

        :return:
        """
        self.score += 1
        self.canvas.itemconfigure(self._score_text, text=str(self.score))

    def _game_start(self):
        self.score = 0
        self.canvas.itemconfigure(self._score_text, text=str(self.score))
        self._player.bird_reset()
        for pipe in self._pipe_list:
            pipe.pipe_reset()
        self._game_started = True
        self._game_loop()

    def _game_loop(self):
        if self._game_started:
            self._player.move_bird()
            self._player.collision_detection()
            for pipe in self._pipe_list:
                pipe.move_pipe()
        self.window.after(Game._REFRESH_RATE, self._game_loop)

    def show_game_canvas(self):
        """
        Show game.

        :return:
        """
        self.canvas.pack()
        self._game_start()

    def hide_game_canvas(self):
        """
        Hide game.

        :return:
        """
        self.canvas.pack_forget()

    def end_game(self):
        """
        End game.

        :return:
        """
        self._game_started = False
        self.gui.show_game_over()


class Bird:
    """Class bird."""

    def __init__(self, game, window, canvas, start_x_position):
        """
        Initialise.

        :param game:
        :param window:
        :param canvas:
        :param start_x_position:
        """
        # Set variables
        self.game = game
        self.canvas = canvas
        self.window = window

        # Properties of the bird.
        self._bird_width = 30
        self._bird_height = 30
        self._y_velocity = 0
        self._y_acceleration = -800
        self._terminal_velocity = -1000
        self._flap_up_velocity = -300
        self._start_x_position = start_x_position

        # Draw bird into the canvas
        self.bird = self.canvas.create_rectangle(self._start_x_position,
                                                 (GUI.CANVAS_HEIGHT / 2) -
                                                 (self._bird_height / 2),
                                                 self._start_x_position +
                                                 self._bird_width,
                                                 (GUI.CANVAS_HEIGHT / 2) +
                                                 (self._bird_height / 2),
                                                 fill="#60261e")
        self.current_time = time.time()

    def move_bird(self):
        """
        Move bird.

        :return:
        """
        # displacement = velocity * change time
        self.canvas.move(self.bird, 0, self._y_velocity * (time.time() -
                                                           self.current_time))
        self._y_velocity = max(self._y_velocity - self._y_acceleration *
                               (time.time() - self.current_time),
                               self._terminal_velocity)
        self.current_time = time.time()

    def collision_detection(self):
        """
        Collision detect.

        :return:
        """
        _bird_coordinate = self.canvas.coords(self.bird)
        if len(self.canvas.find_overlapping(_bird_coordinate[0],
                                            _bird_coordinate[1],
                                            _bird_coordinate[2],
                                            _bird_coordinate[3])) > 1:
            self.game.end_game()
        elif _bird_coordinate[3] >= GUI.CANVAS_HEIGHT:
            self.game.end_game()
        elif _bird_coordinate[3] <= self._bird_height:
            self.game.end_game()

    def flap(self, event):
        """
        Flap.

        :param event:
        :return:
        """
        if event.char == ' ':
            self._y_velocity = self._flap_up_velocity
        else:
            self._y_velocity = self._flap_up_velocity

    def bird_reset(self):
        """
        Bird reset.

        :return:
        """
        self.current_time = time.time()
        self._y_velocity = 0
        self.canvas.delete(self.bird)
        self.bird = self.canvas.create_rectangle(self._start_x_position,
                                                 (GUI.CANVAS_HEIGHT / 2) -
                                                 (self._bird_height / 2),
                                                 self._start_x_position +
                                                 self._bird_width,
                                                 (GUI.CANVAS_HEIGHT / 2) +
                                                 (self._bird_height / 2),
                                                 fill="#60261e")


class Pipe:
    """Pipe class."""

    def __init__(self, game, _gap_position, _x_position):
        """
        Initialise.

        :param game:
        :param _gap_position:
        :param _x_position:
        """
        # Set variables
        self.game = game
        self.canvas = game.canvas
        self.window = game.window
        self._score_added = False

        # Properties of pipe.
        self._pipe_width = 50
        self._gap_length = 125
        self._velocity = 125
        self.current_time = time.time()

        # Variable properties
        self._gap_position = _gap_position
        self._pipe_x_position = _x_position

        # Draw the pipes onto the canvas
        self._bottom_pipe = self.canvas.create_rectangle(self._pipe_x_position,
                                                         GUI.CANVAS_HEIGHT -
                                                         self._gap_position +
                                                         self._gap_length,
                                                         self._pipe_x_position
                                                         + self._pipe_width,
                                                         GUI.CANVAS_HEIGHT,
                                                         fill="green")
        self._top_pipe = self.canvas.create_rectangle(self._pipe_x_position,
                                                      GUI.CANVAS_HEIGHT -
                                                      self._gap_position,
                                                      self._pipe_x_position +
                                                      self._pipe_width,
                                                      0,
                                                      fill="green")

    def move_pipe(self):
        """
        Move pipe.

        :return:
        """
        # displacement = velocity * change time
        self.canvas.move(self._bottom_pipe, -self._velocity *
                         (time.time() - self.current_time), 0)
        self.canvas.move(self._top_pipe, -self._velocity *
                         (time.time() - self.current_time), 0)
        self.current_time = time.time()
        if self.canvas.coords(self._top_pipe)[0] <\
                Game.X_BIRD_START_POSITION and not self._score_added:
            self.game.add_score()
            self._score_added = True
        if self.canvas.coords(self._top_pipe)[0] < -self._pipe_width:
            self._randomise_pipe()

    def _randomise_pipe(self):
        self._gap_position = random.randint(Game.GAP_RANGE[0],
                                            Game.GAP_RANGE[1])
        self.canvas.delete(self._bottom_pipe)
        self.canvas.delete(self._top_pipe)
        self._bottom_pipe = self.canvas.create_rectangle(GUI.CANVAS_WIDTH +
                                                         Game.GAP_BETWEEN_PIPES
                                                         - self._pipe_width,
                                                         GUI.CANVAS_HEIGHT -
                                                         self._gap_position +
                                                         self._gap_length,
                                                         GUI.CANVAS_WIDTH +
                                                         Game.
                                                         GAP_BETWEEN_PIPES,
                                                         GUI.CANVAS_HEIGHT,
                                                         fill="green")
        self._top_pipe = self.canvas.create_rectangle(GUI.CANVAS_WIDTH +
                                                      Game.GAP_BETWEEN_PIPES -
                                                      self._pipe_width,
                                                      GUI.CANVAS_HEIGHT -
                                                      self._gap_position,
                                                      GUI.CANVAS_WIDTH +
                                                      Game.GAP_BETWEEN_PIPES,
                                                      0,
                                                      fill="green")
        self._score_added = False

    def pipe_reset(self):
        """
        Pipe reset.

        :return:
        """
        self._score_added = False
        self._gap_position = random.randint(Game.GAP_RANGE[0],
                                            Game.GAP_RANGE[1])
        self.current_time = time.time()
        self.canvas.delete(self._bottom_pipe)
        self.canvas.delete(self._top_pipe)
        self._bottom_pipe = self.canvas.create_rectangle(self._pipe_x_position,
                                                         GUI.CANVAS_HEIGHT -
                                                         self._gap_position +
                                                         self._gap_length,
                                                         self._pipe_x_position
                                                         + self._pipe_width,
                                                         GUI.CANVAS_HEIGHT,
                                                         fill="green")
        self._top_pipe = self.canvas.create_rectangle(self._pipe_x_position,
                                                      GUI.CANVAS_HEIGHT -
                                                      self._gap_position,
                                                      self._pipe_x_position +
                                                      self._pipe_width,
                                                      0,
                                                      fill="green")


class GUI:
    """Class GUI."""

    # Properties of GUI.
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 400

    def __init__(self):
        """Initialise."""
        # Create window and title.
        self.window = tk.Tk()
        self.window.maxsize(GUI.CANVAS_WIDTH, GUI.CANVAS_HEIGHT)
        self.window.title(string='Flappy Bird')

        self.menu = Menu(self)
        self.game = Game(self)
        self.game_over = GameOver(self)

        self.show_menu()

        self.window.mainloop()

    def show_game(self):
        """
        Show game.

        :return:
        """
        self.menu.hide_menu_canvas()
        self.game_over.hide_game_over_canvas()
        self.game.show_game_canvas()

    def show_menu(self):
        """
        Show menu.

        :return:
        """
        self.game.hide_game_canvas()
        self.game_over.hide_game_over_canvas()
        self.menu.show_menu_canvas()

    def show_game_over(self):
        """
        Show game over.

        :return:
        """
        self.menu.hide_menu_canvas()
        self.game.hide_game_canvas()
        self.game_over.show_game_over_canvas()


GUI()
