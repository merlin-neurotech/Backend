#space invaders part one 

#setting up the screen 

import turtle
import os

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Space Boys")

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

#create the player 
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

## players bullet
bullet = turtle.Turtle()
bullet.color("green")
bullet.shape("square")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.25,0.7)
bullet.hideturtle()

#bullet will have states ready,firing 
bulletstate = "ready"


vel = 15
evil_vel = 2
bull_vel = 20

#create the enemy 
evil = turtle.Turtle()
evil.color("red")
evil.shape("circle")
evil.penup()
evil.speed(0)
evil.setposition(-200,250)



def move_left( ):
    if(player.xcor() <= -280):
        player.setx(-280)
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
    

#creating the key bindings 

screen.onkeypress(move_left,"Left")
screen.onkeypress(move_right,"Right")
screen.onkey(fire_bull,"space")
screen.listen()

#main game loop! 
while True:

    #move the evil person 
    evil.setx(evil.xcor() + evil_vel)
    if(evil.xcor() > 280 or evil.xcor() < -280):
        evil.sety(evil.ycor() - 10)
        evil_vel = evil_vel*-1.01
    
    if(bulletstate == "fire"):
        bullet.sety(bullet.ycor() + bull_vel)
    

delay =  input("press enter to finish")