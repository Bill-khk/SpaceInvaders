import turtle
from turtle import Turtle


class Spaceship(Turtle):
    spaceship_url = 'gif/vaisseau-spatial2.gif'
    turtle.register_shape(spaceship_url)  # Register first

    def __init__(self):
        super().__init__()
        self.shape(self.spaceship_url)  # Then apply it
        self.teleport(0, -400)
        self.penup()
        self.speed(0)

    def move_Right(self):
        self.setheading(0)
        self.forward(40)

    def move_Left(self):
        self.setheading(180)
        self.forward(40)
