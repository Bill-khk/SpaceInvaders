import time
import turtle
from turtle import Turtle
import random


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
        # Characteristics
        self.speed = 40
        self.power = 20
        self.missile = 1
        # Game
        self.screen = screen
        self.shooting = True
        self.invaders = invaders

        self.auto_shoot()

    def move_Right(self):
        self.setheading(0)
        self.forward(40)
        self.screen.update()

    def move_Left(self):
        self.setheading(180)
        self.forward(40)
        self.screen.update()

    def auto_shoot(self):
        if self.shooting: # TODO Correct this
            for nb_missile in range(1, self.missile+1):
                if self.missile % 2 == 0:
                    Missile(self, True, nb_missile+1)
                else:
                    Missile(self, False, nb_missile+1)
        turtle.ontimer(self.auto_shoot, 400)  # fire every 400 ms
        self.screen.update()


class Missile(Turtle):
    def __init__(self, vessel, option, nb):
        super().__init__()
        self.shape('classic')
        self.setheading(90)
        self.penup()
        if option:  # If pair
            if nb % 2 == 0:  # Half are positioned on the left part of the vessel
                index = -1
            else:
                index = 1
            self.teleport(x=vessel.xcor() + (index * nb * 15), y=vessel.ycor() + 10)
        else:
            if nb == 1:
                self.teleport(x=vessel.xcor(), y=vessel.ycor() + 10)
                self.color('red')
            else:
                if nb % 2 == 0:  # Half are positioned on the left part of the vessel
                    index = -1
                    nb_index = nb/2
                else:
                    index = 1
                    nb_index = (nb-1)/2
                self.teleport(x=vessel.xcor() + (index * nb_index * 15) + (index * 10), y=vessel.ycor() + 10)

        self.exist = True
        self.vessel = vessel
        self.move()  # Missile always moves

    def move(self):
        if self.ycor() < 450:  # Top of screen limit
            self.forward(20)
            turtle.ontimer(self.move, 50)  # Automatically call move every 50ms
        else:
            self.hideturtle()
            self.exist = False
        self.check_hit()
        self.vessel.screen.update()

    def check_hit(self):
        if self.exist:
            for invader in self.vessel.invaders:
                if invader.xcor() + 20 >= self.xcor() >= invader.xcor() - 20 and self.ycor() >= invader.ycor() - 20:
                    self.exist = False
                    self.hideturtle()
                    invader.life -= self.vessel.power
                    if invader.life <= 0:
                        print('Invader destroyed')
                        invader.hideturtle()
                        self.random_drop(invader)
                        invader.teleport(1000, 1000)

    def random_drop(self, invader):
        luck = random.randint(1, 10)
        if luck % 2 == 0:
            print('Gift')
            Gift(self.vessel, invader)


class Gift(Turtle):
    gift_url = 'gif/star.gif'
    turtle.register_shape(gift_url)  # Register first

    def __init__(self, vessel, invader):
        super().__init__()
        self.penup()
        self.teleport(0, 0)
        self.teleport(x=invader.xcor(), y=invader.ycor())
        self.shape(self.gift_url)
        self.setheading(270)
        self.vessel = vessel
        self.exist = True
        self.move()

    def move(self):
        if self.ycor() > -450:  # Bop of screen limit
            self.forward(20)
            self.check_pickup()
            turtle.ontimer(self.move, 100)  # Automatically call move every 50ms
        else:
            print('Lost gift')
            self.hideturtle()
            self.exist = False

        self.vessel.screen.update()

    def check_pickup(self):
        if self.exist:
            if self.vessel.xcor() + 30 >= self.xcor() >= self.vessel.xcor() - 30 and self.ycor() <= self.vessel.ycor() + 20:
                # print(f'picked up : {self.vessel.xcor() + 20} >= {self.xcor()} >= {self.vessel.xcor() - 20} and {self.ycor()} <= {self.vessel.ycor() + 20}')
                self.hideturtle()
                self.teleport(1000, 1000)
                self.vessel.missile += 1
