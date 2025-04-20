import time
import turtle
from turtle import Screen, Turtle
from PIL import Image
from spaceship import Spaceship, active_gifts, active_missiles
from invader import Ant, Spider, Dragon, active_monsters
from tkinter import messagebox


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
active_life = []
level = 1

# TODO correct the "to many monster moving already state"
# TODO detect when the game is over
# TODO implement difficulty level
# TODO manage vessel life
def spawn_monsters(level, row=3, col=7):
    y_origin = 350
    for i in range(row):
        x_origin = -250
        for y in range(col):
            monster_list.append(Ant(x_origin, y_origin))
            x_origin += 80
        y_origin -= 70
    screen.update()


def check_collision(ship, monster):
    if monster.exist:
        if monster.xcor() + 20 >= ship.xcor() >= monster.xcor() - 20 and monster.ycor() + 20 >= ship.ycor() >= monster.ycor() - 20:
            print('Collision')
            monster.exist = False
            monster.hideturtle()
            monster.teleport(1000, 1000)
            active_monsters.remove(monster)
            ship.life -= 1
            print(ship.life)
            update_life(ship)


def update_life(vessel):
    screen_anchor = (290, 420)
    offset = 45

    life_url = 'gif/life.gif'
    turtle.register_shape(life_url)
    shield_url = 'gif/shield_life.gif'
    turtle.register_shape(shield_url)
    for i in active_life:
        i.hideturtle()

    for i in range(1, vessel.life + 1):
        print(i)
        life_icon = Turtle()
        life_icon.penup()
        life_icon.shape(life_url)
        life_icon.teleport(screen_anchor[0] - offset * i, screen_anchor[1])
        active_life.append(life_icon)

    if vessel.extra_life:
        shield_icon = Turtle()
        shield_icon.penup()
        shield_icon.shape(shield_url)
        shield_icon.teleport(screen_anchor[0] - offset * (vessel.life + 1), screen_anchor[1])
        active_life.append(shield_icon)

def check_game(screen, vessel):
    if vessel.life == 0:
        vessel.shooting = False

        if messagebox.askokcancel("Game over", "Want to continue?"):
            print('Restart the game')
            #TODO
        else:
            return True
    else:
        return False


def game_loop(ship):
    for missile in active_missiles[
                   :]:  # [:] means loop over a copy of the list active_missiles - avoid weird behavior or even a crash, because you're modifying the list while looping over it.
        missile.move()

    for gift in active_gifts[:]:
        gift.move()

    for monster in monster_list:
        monster.roll_action()

    for monster in active_monsters[:]:
        monster.behave()
        check_collision(ship, monster)

    if check_game(screen, vessel):
        turtle.bye()

    screen.update()
    screen.ontimer(lambda: game_loop(ship), 50)  # run every 50ms


vessel = Spaceship(screen, monster_list)
spawn_monsters(level)
update_life(vessel)
screen.listen()
screen.onkey(vessel.move_Right, 'Right')
screen.onkey(vessel.move_Left, 'Left')

game_loop(vessel)
screen.mainloop()
