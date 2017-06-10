try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from math import sqrt
import random
random.seed()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
RADIUS = 64
FPS = int(1000/60)
NORMAL_SPEED = 3000
GRAVITY = 0.15
SPEED_LIMIT = 2
LIFES = 5

NORMAL_BUTTON_COLOR = '#%02x%02x%02x' % (0, 200, 255)
CLICKED_BUTTON_COLOR = '#%02x%02x%02x' % (0, 150, 255)
NORMAL_BUTTON_COLOR_RED = '#%02x%02x%02x' % (255, 50, 25)
CLICKED_BUTTON_COLOR_RED = '#%02x%02x%02x' % (255, 0, 0)
BALL_COLORS = [['#%02x%02x%02x' % (255, 0, 0)], ['#%02x%02x%02x' % (0, 255, 0)], ['#%02x%02x%02x' % (0, 0, 255)],
               ['#%02x%02x%02x' % (255, 255, 0)]]

window = Tk()
window.geometry('{}x{}+30+30'.format(SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = Canvas(window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.place(x=0, y=0)
active_widgets = []
balls = []


class Ball():
    def __init__(self, clicks):
        self.x = random.randint(1, SCREEN_WIDTH-RADIUS*2-1)
        self.y = -2*RADIUS
        self.color = BALL_COLORS[random.randint(0, len(BALL_COLORS)-1)]
        self.y_change = 0
        self.clicks = clicks
        balls.append(self)

    def draw(self):
        canvas.create_oval(self.x, self.y, self.x + 2 * RADIUS, self.y + 2 * RADIUS,
                           fill=self.color, outline=self.color)
        canvas.create_text(self.x+RADIUS, self.y+RADIUS, anchor='c', text=self.clicks, font=('TkDefaultFont', 20))


def new_ball():
    Ball(3*(int(time//(FPS*30))+1))
    window.after(NORMAL_SPEED, new_ball)


def draw_balls():
    global time
    canvas.delete(ALL)
    for i in balls:
        i.draw()
    canvas.create_text(1, 1, anchor='nw', text="Lifes: {}".format(LIFES), font=('TkDefaultFont', 16))
    time += 1
    seconds = int(time / (1000 / FPS))
    canvas.create_text(SCREEN_WIDTH/2, 0, anchor='n', text='{}'.format(seconds), font=('TkDefaultFont', 16))
    canvas.create_text(1, 20, anchor='nw', text="Score: {}".format(score), font=('TkDefaultFont', 16))
    canvas.create_text(1, 40, anchor='nw', text="Multiplier: x{}".format(int(time//(FPS*30))+1), font=('TkDefaultFont', 16))
    window.after(FPS, draw_balls)


def gravity():
    global LIFES
    for i in balls:
        if i.y < SPEED_LIMIT:
            i.y_change += GRAVITY
        i.y += i.y_change
        if i.y >= SCREEN_HEIGHT:
            LIFES -= 1
            balls.pop(balls.index(i))
    if LIFES <= 0:
        canvas.delete("all")
        main()
    window.after(FPS, gravity)


def click(event):
    global score
    for i in balls:
        if sqrt((i.x+RADIUS-event.x)**2+(i.y+RADIUS-event.y)**2) <= RADIUS and i.y_change >= 0:
            i.y_change *= -1
            i.clicks -= 1
            score += (int(time//(FPS*30))+1)
            if i.clicks <= 0:
                balls.pop(balls.index(i))
                score += (int(time//(FPS*30))+1)**2


def play(arg):
    global time, score
    for i in active_widgets:
        i.place_forget()
    time = 0
    score = 0
    new_ball()
    draw_balls()
    gravity()
    canvas.bind("<Button-1>", click)
    canvas.update_idletasks()


def quiting(arg):
    quit()


def main():
    global active_widgets, window
    for i in active_widgets:
        i.place_forget()

    naslov = Label(window, text='Balls', font=('TkDefaultFont', 96))
    naslov.place(relx=.5, rely=.15, anchor='c')

    play_button = Button(window, text='Play')
    play_button.bind('<Button>', play)
    play_button.config(background=NORMAL_BUTTON_COLOR, activebackground=CLICKED_BUTTON_COLOR, height=3, width=30)
    play_button.place(relx=.5, rely=.4, anchor='c')

    quit_button = Button(window, text='Quit')
    quit_button.bind('<Button>', quiting)
    quit_button.config(background=NORMAL_BUTTON_COLOR_RED, activebackground=CLICKED_BUTTON_COLOR_RED, height=3, width=30)
    quit_button.place(relx=.5, rely=.8, anchor='c')
    active_widgets = [naslov, play_button, quit_button]

    window.mainloop()

if __name__ == '__main__':
    main()
