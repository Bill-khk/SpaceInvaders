from turtle import Turtle
import turtle

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

    def move_Suicide(self):
        pass


class Bug(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.bug_url)
        self.life = 100

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

