import time
import turtle
from turtle import Screen, Turtle
from PIL import Image
from spaceship import Spaceship, active_gifts, active_missiles
from invader import Bug, Spider, Dragon, active_monsters

screen = Screen()
screen.setup(width=600, height=900)
screen.tracer(0)  #Can be used with screen.update to increase the code speed


# Used to create small version of PNG icon
def resize(URL):
    img = Image.open(URL)
    width, height = img.size
    img = img.resize((width // 8, height // 8), Image.Resampling.LANCZOS)
    new_URL = f'{URL[:URL.find('.gif')]}2.gif'
    img.save(new_URL)
    return new_URL


monster_list = []
level = 1

# TODO implement other type of monster and other behavior
# TODO detect when the game is over
# TODO implement difficulty level
# TODO manage vessel life
def spawn_monsters(level, row=3, col=7):
    y_origin = 350
    for i in range(row):
        x_origin = -250
        for y in range(col):
            monster_list.append(Bug(x_origin, y_origin))
            x_origin += 80
        y_origin -= 70
    screen.update()

def check_collision(ship, monster):
    if monster.xcor() + 20 >= ship.xcor() >= monster.xcor() - 20 and monster.ycor() + 20 >= ship.ycor() >= monster.ycor() - 20:
        print('Collision')

def game_loop(ship):
    for missile in active_missiles[:]:  # [:] means loop over a copy of the list active_missiles - avoid weird behavior or even a crash, because you're modifying the list while looping over it.
        missile.move()

    for gift in active_gifts[:]:
        gift.move()

    for monster in monster_list:
        monster.roll_action()

    for monster in active_monsters[:]:
        monster.behave()
        # check_collision(ship, monster)

    screen.update()
    screen.ontimer(lambda: game_loop(ship), 50)  # run every 50ms


vessel = Spaceship(screen, monster_list)
spawn_monsters(level)
screen.listen()
screen.onkey(vessel.move_Right, 'Right')
screen.onkey(vessel.move_Left, 'Left')

game_loop(vessel)
screen.mainloop()
