# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 20:16:47 2019

@author: munich
"""
import os
from constants import *
from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.keyboard import Keyboard
from pygaze.mouse import Mouse
from pygaze.eyetracker import EyeTracker
from psychopy import event
import pygaze.libtime as timer
import pandas
import time

# Get game structure values
gloc=os.path.join(DIR,'games\games_own.csv')
df_own = pandas.read_csv(gloc)
game_vectors_own = df_own.values

gloc2 = os.path.join('games\games_other.csv')
df_other = pandas.read_csv(gloc2)
game_vectors_other = df_other.values


# Specify size of matrices (number of choices available to players)
p1=3
p2=3


# Draw game matrices
xax=DISPSIZE[0]
yax=DISPSIZE[1]

cy=yax/2
cx=xax/2

### Set size of game matrix relative to screen with 'margin'.
margin = 0.7
side=yax*margin
t_side=side/p1
tloc=t_side/p1

owncol = (255,255,255)
othercol = (255,255,255)

disp = Display(dispsize=DISPSIZE, screennr=2)
mse = Mouse(visible=False, timeout=10)

gamescreen = Screen(dispsize=DISPSIZE)

#tracker = EyeTracker(disp)


fixscr = Screen(dispsize=DISPSIZE)
fixscr.draw_fixation(fixtype='cross', diameter=8)

introscreen = Screen(dispsize=DISPSIZE)
introscreen.draw_text("Welcome to the experiment", fontsize=30)
introscreen.draw_text("\n\n\n (To proceed, press any key)", fontsize=25)

istrscreen = Screen(dispsize=DISPSIZE)
istrscreen.draw_text("In this experiment, you will \n play a sequence of games \n like the one displayed on the right", fontsize=30)
istrscreen.draw_text("You", fontsize=25)

exscreen = Screen(dispsize=DISPSIZE)
exvec = [3,2,1,3,2,3,5,2,3,6,3,2,3,4,1,2,3,4]

ycor = cy-(side/2)
count = 0

for i in range(p2):
    xcor = cx-(side/2)
    exscreen.draw_text("You", pos=(cx,cy-(side/2)-((yax*(1-margin))/6)), center=True, fontsize=30)
    exscreen.draw_text("Other", pos=(cx-(side/2)-((yax*(1-margin))/4),cy), center=True, fontsize=30)

    for j in range(p1):
        a=[xcor, ycor]
        b=[xcor + t_side, ycor]
        c=[xcor + t_side, ycor + t_side]
        d=[xcor,ycor + t_side]
        
        pointsown=[a,c,d]
        pointsother=[a,b,c]
        

        exscreen.draw_polygon(pointsown, colour=owncol, pw=1, fill=False)
        exscreen.draw_polygon(pointsother, colour=othercol, pw=1, fill=False)
 
        c=0
        for k in range(2):
            c=1+k
            d=2-k
            A=(xcor+(d*tloc), ycor+(c*tloc))
            exscreen.draw_text(text=str(exvec[count]), pos=A, center=True, fontsize=30)
            count +=1
        xcor += t_side
    ycor += t_side



##Set number of games played
rounds = 4






tracker = EyeTracker(disp)
##Experiment
choice=[]

wait=True
while wait==True:
    disp.fill(introscreen)
    disp.show()
    pressed = mse.get_pressed()
    if sum(pressed)>0:
        event.clearEvents(eventType='mouse')
        wait=False

      
pressed = [0,0,0] 
wait=True
while wait==True:
    tryscreen = exscreen
    tryscreen.draw_text('Press the \n middle button', pos=(((1-margin)/4)*xax,((1-margin)/4)*yax), fontsize=20)
    disp.fill(tryscreen)
    disp.show()
    resp = mse.get_pressed()
    if resp[2]==1:
        event.clearEvents(eventType='mouse')
        wait=False

timer.pause(1000)

pressed = () 
wait=True
print(wait)
disp.fill(introscreen)
disp.show()
while wait==True:
    print(pressed)
    pressed = mse.get_pressed()
    introscreen.draw_text(str(pressed), pos=(((1-margin)/4)*xax,((1-margin)/4)*yax), fontsize=20)
    disp.fill(introscreen)
    disp.show()
    print(pressed)
    if sum(pressed)>0:
        event.clearEvents(eventType='mouse')
        wait=False
    print(wait)
 
        
dsp = Display(dispsize=DISPSIZE, screennr=2)
tracker = EyeTracker(dsp, trackertype='eyelink')
tracker.calibrate()
tracker.close()
dsp.close()
tracker.start_recording()
######### Trials

for r in range(rounds):
    tracker.status_msg('Trial with matrix {}'.format(r))
    tracker.log('TRIALSTART')
    disp.fill(fixscr)
    disp.show()
    timer.pause(1000)
    tracker.log('fixation_onset')

    
    gamescreen.clear()
    ycor = cy-(side/2)
    count = 0

    for i in range(p2):
        xcor = cx-(side/2)
        gamescreen.draw_text("You", pos=(cx,cy-(side/2)-((yax*(1-margin))/6)), center=True, fontsize=30)
        gamescreen.draw_text("Other", pos=(cx-(side/2)-((yax*(1-margin))/4),cy), center=True, fontsize=30)

        for j in range(p1):
            a=[xcor, ycor]
            b=[xcor + t_side, ycor]
            c=[xcor + t_side, ycor + t_side]
            d=[xcor,ycor + t_side]
            
            pointsown=[a,c,d]
            pointsother=[a,b,c]
            

            gamescreen.draw_polygon(pointsown, colour=owncol, pw=1, fill=False)
            gamescreen.draw_polygon(pointsother, colour=othercol, pw=1, fill=False)
 
            c=0

            for k in range(2):
                c=1+k
                d=2-k
                A=(xcor+(d*tloc), ycor+(c*tloc))
                if(c==1):
                    gamescreen.draw_text(text=str(game_vectors_own[r][count]), pos=A, center=True, fontsize=30)
                if(c==2):
                    gamescreen.draw_text(text=str(game_vectors_other[r][count]), pos=A, center=True, fontsize=30)
                
            count +=1
            xcor += t_side
        ycor += t_side
    wait=True
    disp.fill(gamescreen)
    disp.show()
    while wait==True:
        pressed = mse.get_clicked()
#        if not pressed[0] is None:
#            choice.append(pressed)
        if not pressed[0] is None:
            choice.append(pressed)
            pressed2=[0,0,0]
            wait=False
    wait = True
# So that humans do not hold a button through all trials (Kahveci & Kucharsky, 2019)
    while wait:
            pressed2 = mse.get_clicked()
            if pressed2[0] is None:
                wait=False

    tracker.log('trial_offset')
    tracker.log('TRIALEND')
        
#    disp.fill()
#    disp.show()
#    timer.pause(1000)

tracker.stop_recording()
tracker.close()
disp.close()
