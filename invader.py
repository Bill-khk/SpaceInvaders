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
        self.rate = 1000

    # TODO Correct those methode
    def behave(self):
        print('I do something')

    def roll_action(self):
        monster_lim = 2
        luck = random.randint(1, 10000)
        if luck % self.rate == 0:
            if len(active_monsters) < monster_lim:
                print('Behave !')
                active_monsters.append(self)
                self.behave()
            else:
                print('To many monster moving already')


class Ant(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.bug_url)
        self.life = 100
        self.rate = 2500

    def behave(self):
        if self.ycor() > -450:  # Bop of screen limit
            self.forward(10)
        else:
            print('Pass over')
            self.hideturtle()
            self.exist = False
            active_monsters.remove(self)


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
