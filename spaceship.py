import time
import turtle
from turtle import Turtle


class Spaceship(Turtle):
    spaceship_url = 'gif/vessel.gif'
    turtle.register_shape(spaceship_url)  # Register first

    def __init__(self, screen):
        super().__init__()
        self.shape(self.spaceship_url)  # Then apply it
        self.teleport(0, -400)
        self.penup()
        self.speed(0)
        self.screen = screen
        self.shooting = True
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
        if self.shooting:
            Missile(self)
            turtle.ontimer(self.auto_shoot, 400)  # fire every 400 ms
            self.screen.update()


class Missile(Turtle):
    def __init__(self, vessel):
        super().__init__()
        self.shape('classic')
        self.setheading(90)
        self.penup()
        self.teleport(x=vessel.xcor(), y=vessel.ycor()+10)
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
        self.vessel.screen.update()


