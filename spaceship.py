import time
import turtle
from turtle import Turtle
import random
from invader import active_monsters

active_missiles = []
active_gifts = []


class Spaceship(Turtle):
    spaceship_url = 'gif/vessel.gif'
    turtle.register_shape(spaceship_url)  # Register first

    def __init__(self, screen, invaders):
        super().__init__()
        # Initialization
        self.shape(self.spaceship_url)  # Then apply it
        self.teleport(0, -400)
        self.penup()
        self.speed(0)
        self.exist = True
        # Characteristics
        self.speed = 30
        self.power = 20
        self.missile = 1
        self.life = 3
        self.extra_life = False
        # Game
        self.screen = screen
        self.shooting = True
        self.invaders = invaders

        self.auto_shoot()

    def move_Right(self):
        self.setheading(0)
        self.forward(20)
        self.screen.update()

    def move_Left(self):
        self.setheading(180)
        self.forward(20)
        self.screen.update()

    def upgrade_weapon(self):
        if self.missile < 5:
            self.missile += 1
        else:
            print("Maximum power reached!")

    def auto_shoot(self):
        if self.shooting:
            spacing = 15  # pixels between missiles
            total_missiles = self.missile
            offset = (total_missiles - 1) / 2 * spacing
            # Ex:
            # total_missiles 4 : offset = 1.5*20 = 30
            # total_missiles 2 : offset = 0.5*20 = 10

            for i in range(total_missiles):
                # Positions are centered around the ship: left to right
                x_offset = (i * spacing) - offset
                # Ex:
                # x_offset 4 missiles = 0-30 = -30, 20-30 = -10, 40-30 = 10, 60-30 = 30
                # x_offset 2 missiles = 0-10 = -10, 20-10 = 10

                Missile(self, x_offset)
        turtle.ontimer(self.auto_shoot, 600)
        self.screen.update()


class Missile(Turtle):
    def __init__(self, vessel, x_offset):
        super().__init__()
        active_missiles.append(self)
        self.shape('classic')
        self.setheading(90)
        self.penup()

        # Positioning missile based on offset
        self.teleport(x=vessel.xcor() + x_offset, y=vessel.ycor() + 10)

        self.exist = True
        self.vessel = vessel
        self.move()  # Missile always moves

    def move(self):
        if self.ycor() < 450:  # Top of screen limit
            self.forward(20)
        else:
            self.hideturtle()
            self.exist = False
            if self in active_missiles:
                active_missiles.remove(self)

    def random_drop(self, invader):
        luck = random.randint(1, 80)
        if luck % 10 == 0:
            result = random.randint(1, 3)

            match result:
                case 1:
                    print('Star')
                    Star(self.vessel, invader)
                case 2:
                    print('Heart')
                    Heart(self.vessel, invader)
                case 3:
                    print('Shield')
                    Shield(self.vessel, invader)


class Gift(Turtle):
    gift_url = 'gif/star.gif'
    turtle.register_shape(gift_url)  # Register first

    def __init__(self, vessel, invader):
        super().__init__()
        active_gifts.append(self)
        self.penup()
        self.teleport(0, 0)
        self.teleport(x=invader.xcor(), y=invader.ycor())
        self.setheading(270)
        self.vessel = vessel
        self.exist = True
        self.move()

    def move(self):
        if self.exist:
            # print('Gift moving')
            if self.ycor() > -400:  # Bop of screen limit
                self.forward(10)
                #self.check_pickup()
            else:
                print('Lost gift')
                self.hideturtle()
                self.exist = False
                if self in active_gifts:
                    active_gifts.remove(self)

    def check_pickup(self):
        if self.exist:
            if self.vessel.xcor() + 30 >= self.xcor() >= self.vessel.xcor() - 30 and self.ycor() <= self.vessel.ycor() + 20:
                # print(f'picked up : {self.vessel.xcor() + 20} >= {self.xcor()} >= {self.vessel.xcor() - 20} and {self.ycor()} <= {self.vessel.ycor() + 20}')
                self.exist = False
                self.hideturtle()
                self.teleport(1000, 1000)
                self.bonus()
                return True

    def bonus(self):
        print('I grant a bonus')

class Star(Gift):
    gift_url = 'gif/star.gif'
    turtle.register_shape(gift_url)  # Register first

    def __init__(self, vessel, invader):
        super().__init__(vessel, invader)
        self.shape(self.gift_url)

    def bonus(self):
        self.vessel.upgrade_weapon()

class Heart(Gift):
    Heart_url = 'gif/life_gift.gif'
    turtle.register_shape(Heart_url)  # Register first

    def __init__(self, vessel, invader):
        super().__init__(vessel, invader)
        self.shape(self.Heart_url)

    def bonus(self):
        self.vessel.life +=1

class Shield(Gift):
    Shield_url = 'gif/shield_life.gif'
    turtle.register_shape(Shield_url)  # Register first

    def __init__(self, vessel, invader):
        super().__init__(vessel, invader)
        self.shape(self.Shield_url)

    def bonus(self):
        self.vessel.extra_life = True

