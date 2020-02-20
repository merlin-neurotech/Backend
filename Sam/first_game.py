#space invaders part one 

#setting up the screen 

import turtle
import os
import math

def writeScore(score):
    scorePen.clear()
    score_string = "Score: {}".format(score)
    scorePen.write(score_string,False,align="left", font= ("Arial",14,"normal"))
    scorePen.hideturtle()
def move_left():
    if(player.xcor() <= -280):
        player.setx(-280)
    else:
        player.setx(player.xcor() - vel)

def move_right():
    if (player.xcor() >= 280):
        player.setx(280)
    player.setx(player.xcor() + vel)

def fire_bull():
    global bulletstate
    if (bulletstate == "ready"):
        #move bull to just above the player 
        bullet.setposition(player.xcor(),player.ycor() + 10)
        bullet.showturtle()
        bulletstate = "fire"

def isCollision(t1,t2):
    distance = math.sqrt((t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2)
    if (distance < 15):
        return True
    else:
        return False
#main game loop! 
def move():
    global bulletstate
    global score
    global evil_vel 
    global bull_vel
    #move the evil person 
    for evil in evils:
        evil.setx(evil.xcor() + evil_vel)
        if(evil.xcor() > 280 or evil.xcor() < -280):
            for e in evils:
                e.sety(e.ycor() - 10)
            evil_vel = evil_vel*-1.01
        if (isCollision(bullet,evil)):
            #update the score 
            score += 10
            writeScore(score)
            #reset the bullet 
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(player.xcor(),player.ycor())
            #reset the enemy 
            evil.hideturtle()
            evil.setposition(500,500)
            evils.remove(evil)
        if (isCollision(evil,player)):
            evil.hideturtle()
            player.hideturtle()
            print("game over")
            break 
    
    if(bulletstate == "fire"):
        if(bullet.ycor() > 275):
            bullet.hideturtle()
            bulletstate = "ready"
        else:
            bullet.sety(bullet.ycor() + bull_vel)
    screen.update()
    screen.ontimer(move,50)

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Space Boys")
screen.tracer(False)

screen.register_shape("player.gif")
screen.register_shape("invader.gif")
#drawing the boarders

border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#setting the score 
score = 0
scorePen = turtle.Turtle()
scorePen.speed(0)
scorePen.color("white")
scorePen.penup()
scorePen.setposition(-290,280)
score_string = "Score: {}".format(score)
scorePen.write(score_string,False,align="left", font= ("Arial",14,"normal"))
scorePen.hideturtle()


#create the player 
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

## players bullet
bullet = turtle.Turtle()
bullet.color("red")
bullet.shape("square")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.15,0.7)
bullet.hideturtle()

#bullet will have states ready,firing 
bulletstate = "ready"


vel = 15
bull_vel = 25
evil_vel = 2

#creating mutliple enimies 
Number_of_evil = 30
number_ofrows = int(Number_of_evil/5)
evils = []
for j in range(number_ofrows):
    yspot = 30
    for i in range(5):
        #create the enemy 
        evils.append(turtle.Turtle())
        evils[len(evils)-1].color("red")
        evils[len(evils)-1].shape("invader.gif")
        evils[len(evils)-1].penup()
        evils[len(evils)-1].speed(0)
        evils[len(evils)-1].setposition(-150 + (i*50),250 - j*yspot)


#creating the key bindings 

screen.onkeypress(move_left,"Left")
screen.onkeypress(move_right,"Right")
screen.onkey(fire_bull,"space")
screen.listen()
move()
screen.mainloop()

    

delay =  input("press enter to finish")