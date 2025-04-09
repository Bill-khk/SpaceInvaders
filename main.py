import turtle
from turtle import Screen, Turtle
from PIL import Image

screen = Screen()
screen.setup(width=600, height=900)
# screen.tracer(0)

# Using pgn icon as turtle
shape_spaceship = 'gif/vaisseau-spatial.gif'


def resize(URL):
    img = Image.open(URL)
    width, height = img.size
    img = img.resize((width // 8, height // 8), Image.Resampling.LANCZOS)
    new_URL = f'{URL[:URL.find('.gif')]}2.gif'
    img.save(new_URL)
    return new_URL


shape_spaceship_shape = resize(shape_spaceship)
turtle.register_shape(shape_spaceship_shape)

spaceship = Turtle()
spaceship.shape(shape_spaceship_shape)
spaceship.teleport(0, -400)

# screen.update()
screen.exitonclick()
