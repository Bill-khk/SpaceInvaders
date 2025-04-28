import random
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
vessel = None
game_on = False
start_time = time.time()  # Used in the main loop, to activate a monster every two sec
last_behave = 0  # Used to know last time we activate a monster behavior

def spawn_monsters(level, row=1, col=7):
    global active_monsters, monster_list
    active_monsters.clear()
    monster_list.clear()
    y_origin = 350
    if level % 3 == 0:
        row = + 1
    for i in range(row):
        x_origin = -250
        for y in range(col):
            if level < 2:
                monster = Ant(x_origin, y_origin)
            elif level < 4:
                monster = random.choice([Ant(x_origin, y_origin), Spider(x_origin, y_origin)])
            else:
                monster = random.choice(
                    [Ant(x_origin, y_origin), Spider(x_origin, y_origin), Dragon(x_origin, y_origin)])
            monster_list.append(monster)
            x_origin += 80
        y_origin -= 70
    screen.update()


def check_collision(monster):
    global vessel
    if monster.exist:
        if monster.xcor() + 20 >= vessel.xcor() >= monster.xcor() - 20 and monster.ycor() + 20 >= vessel.ycor() >= monster.ycor() - 20:
            print('Collision')
            monster.exist = False
            monster.hideturtle()
            monster.teleport(1000, 1000)
            active_monsters.remove(monster)
            vessel.life -= 1
            update_life()
            return True
        else:
            return False
    else:
        return False


def update_life():
    global vessel
    screen_anchor = (290, 420)
    offset = 45

    life_url = 'gif/life.gif'
    turtle.register_shape(life_url)
    shield_url = 'gif/shield_life.gif'
    turtle.register_shape(shield_url)
    for i in active_life:
        i.hideturtle()

    for i in range(1, vessel.life + 1):
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


def check_game():
    global vessel, game_on, level
    if vessel.life == 0:  # Used to check if the vessel still have lives
        #vessel.shooting = False

        if messagebox.askokcancel("Game over", "Want to continue?"):
            game_on = False
            end_game()
            run_game()
        else:
            return True
    elif len(monster_list) == 0:
        messagebox.showinfo(title='Level done', message="Going to the next level !", )
        level += 1
        # end_game()
        #run_game()
        spawn_monsters(level)
    else:
        return False


def check_missile_hit(monster):
    for missile in active_missiles:
        if missile.exist:
            if monster.xcor() + 20 >= missile.xcor() >= monster.xcor() - 20 and missile.ycor() >= monster.ycor() - 20:
                missile.exist = False
                missile.hideturtle()
                monster.life -= missile.vessel.power
                if monster.life <= 0:
                    print(f'Invader destroyed - {len(monster_list)}')
                    monster_list.remove(monster)
                    monster.hideturtle()
                    missile.random_drop(monster)
                    monster.teleport(1000, 1000)


def game_loop():
    global vessel, game_on, last_behave
    timelapse = round(time.time() - start_time, 0)
    for missile in active_missiles[
                   :]:  # [:] means loop over a copy of the list active_missiles - avoid weird behavior or even a crash, because you're modifying the list while looping over it.
        missile.move()
        #check_missile_hit(missile, monster_list)

    for gift in active_gifts[:]:
        gift.move()

    if timelapse % 5 == 0 and timelapse != last_behave:
        last_behave = timelapse
        monster = random.choice(monster_list)
        monster.roll_action()

    for monster in monster_list:
        check_missile_hit(monster)

    for monster in active_monsters[:]:
        if monster.behave():
            monster_list.remove(monster)
        if check_collision(monster):
            monster_list.remove(monster)

    if check_game():
        turtle.bye()

    screen.update()
    if game_on:
        screen.ontimer(lambda: game_loop(), 50)  # run every 50ms


def run_game():
    global vessel, game_on
    game_on = True
    vessel = Spaceship(screen, monster_list)  # Restarting behavior cleanly
    print_game()  # Check game state
    screen.listen()
    screen.onkey(vessel.move_Right, 'Right')
    screen.onkey(vessel.move_Left, 'Left')
    spawn_monsters(level)
    update_life()
    game_loop()
    screen.mainloop()


def print_game():
    print(f'new game:\n'
          f'current vessel missile :{vessel.missile}\n'
          f'active monster: {active_monsters}\n'
          f'active gift {active_gifts}\n'
          f'monster list {monster_list}')


# Function used only when resetting the game
def end_game():
    global monster_list, active_life, level, active_monsters
    for monster in monster_list:
        monster.hideturtle()
        monster.teleport(1000, 1000)
    monster_list.clear()

    for missile in active_missiles:
        missile.hideturtle()
        missile.teleport(1000, 1000)

    for gift in active_gifts:
        gift.hideturtle()
        gift.teleport(1000, 1000)

    vessel.hideturtle()
    vessel.teleport(1000, 1000)

    active_monsters.clear()
    active_life.clear()
    level = 1


run_game()
