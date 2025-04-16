from turtle import Turtle
import turtle
import random

active_monsters = []

class Invader(Turtle):
    bug_url = 'gif/bug.gif'
    turtle.register_shape(bug_url)
    dragon_url = 'gif/dragon.gif'
    turtle.register_shape(dragon_url)
    spider_url = 'gif/spider.gif'
    turtle.register_shape(spider_url)


    def __init__(self, x, y):
        super().__init__()
        self.shape(self.bug_url)  # Then apply it
        self.penup()
        self.speed(0)
        self.setheading(270)
        self.teleport(x=x, y=y)
        # Game parameters
        self.life = 0
        self.exist = True
        self.doing_action = False
        self.rate = 1000

# TODO Correct those methode
    def behave(self):
        print('I do something')

    def behavior(self):
        if not self.doing_action:
            luck = random.randint(1, 20)
            if luck % self.rate == 0:
                print('Behave !')
                self.behave()
                self.doing_action = True

class Bug(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.bug_url)
        self.life = 100
        self.rate = 5

    def behave(self):
        if self.ycor() > -450:  # Bop of screen limit
            self.forward(10)
        else:
            print('Pass over')
            self.hideturtle()
            self.exist = False
            self.doing_action = False


class Dragon(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.dragon_url)
        self.life = 40

class Spider(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.spider_url)
        self.life = 60

