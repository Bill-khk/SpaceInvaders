from turtle import Turtle
import turtle
import random

active_monsters = []
active_fireball = []

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

    def behave(self):
        print('I do something')

    def pass_over(self):
        print('Pass over')
        self.hideturtle()
        self.exist = False
        if self in active_monsters:
            active_monsters.remove(self)
        print(f'number of active monster :{len(active_monsters)}')

    def roll_action(self):
        # TODO Change to make a monster roll every two second
        monster_lim = 2
        # luck = random.randint(1, 10000)
        # if luck % self.rate == 0:
        if len(active_monsters) < monster_lim:
            print('Behave !')
            active_monsters.append(self)
            self.behave()
        else:
            print('To many monster moving already')
        print(f'number of active monster :{len(active_monsters)}')


class Ant(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.bug_url)
        self.life = 100
        self.rate = 1000

    def behave(self):
        if self.ycor() > -450:  # Bop of screen limit
            self.forward(10)
            return False
        else:
            self.pass_over()
            return True  # Return true if it needs to be removed from monster_list


class Dragon(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.dragon_url)
        self.life = 40

    class Fireball(Turtle):
        def __init__(self, invader, x_offset):
            super().__init__()
            active_fireball.append(self)
            self.invader = invader
            self.exist = True

            self.shape('classic')
            self.setheading(90)
            self.penup()
            self.teleport(invader.xcor(), invader.ycor()-10)

        def move(self):
            if self.exist:
                if self.ycor() < -450:  # Bot of screen limit
                    self.forward(20)
                else:
                    self.hideturtle()
                    self.exist = False
                    if self in active_fireball:
                        active_fireball.remove(self)


class Spider(Invader):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape(self.spider_url)
        self.life = 60

    def behave(self):
        if self.exist:
            if self.ycor() > -450:  # Bop of screen limit
                self.setx(self.xcor() + random.choice([-10, 10]))
                self.sety(self.ycor() - 10)
                return False
            else:
                self.pass_over()
                return True




