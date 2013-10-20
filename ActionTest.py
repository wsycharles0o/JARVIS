import Action
import time
import random
x, y = 400,400
while True:
    x = x+ random.randint(0,50)
    y = y + random.randint(0,50)
    Action.MoveCursor(x, y)
    prevx, prevy = x, y
    print prevx, prevy
    time.sleep(0.2)
    
