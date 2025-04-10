import turtle
from turtle import Screen, Turtle
from PIL import Image
from spaceship import Spaceship
screen = Screen()
screen.setup(width=600, height=900)
# screen.tracer(0) #Can be used with screen.update to increase the code speed


# Used to create small version of PNG icon
def resize(URL):
    img = Image.open(URL)
    width, height = img.size
    img = img.resize((width // 8, height // 8), Image.Resampling.LANCZOS)
    new_URL = f'{URL[:URL.find('.gif')]}2.gif'
    img.save(new_URL)
    return new_URL


vessel = Spaceship()
playing = True
screen.listen()
screen.onkey(vessel.move_Right, 'Right')
screen.onkey(vessel.move_Left, 'Left')

# screen.update()
screen.mainloop()
