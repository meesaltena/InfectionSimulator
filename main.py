# Mees Altena 31-03-2020
# https://github.com/meesaltena

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from person import *
from graphics import *
from PIL import ImageFont
import time
import PIL.Image
import time


# Dimensions of the 'playing field' of the populations
width = 800
height = 600
# Radius of every dot (person) in pixels
circle_radius = 5
# Create the graphics window
win = GraphWin('InfectionSimulator', width+800, height+10)

# ------- Simulation parameters ------- 
# Amount of ticks to simulate for
timesteps = 1000
# Size of the population
n = 400
# Minimum time in seconds each tick should take, only used if simulating the tick takes less time than this value
delay = 0.05
# Chance someone moves per tick
move_chance = 0.8

# ------- Disease parameters -------
# Radius of the 'sphere of influence', i.e. how close someone needs to be to get infected
soi_radius = 25
# Max pixels a person can move per step
step = 15
# Chance an infected person dies per tick
death_chance = 0.001
# Chance an infected person recoveres per tick, given that they don't die in the same tick
recovery_chance = 0.001
# Whether the disease provides immunity after recovery or not 
immune_after_recovery = True

# Create various stat counters
susceptible_counter = Text(Point(1000,510), 'Amount susceptible: ')
infected_counter = Text(Point(990,530), 'Amount infected: ')
dead_counter = Text(Point(990,550), 'Amount dead: ')
recovered_counter = Text(Point(990,570), 'Amount recovered: ')

Population = []
Circles = []

# Generate a population with random x and y coordinates
def generateRandomPopulation(n):
    for i in range(n):
        x = random.randint(0,width)
        y = random.randint(0,height)
        Population.append(Person(x,y))

# Generate a circle object for every person in the populaion
def generateCircles():
    for p in Population:
        pt = Point(p.x, p.y)
        c = Circle(pt, circle_radius)
        c.setFill("blue")
        Circles.append(c)

# Draw the circles to the window, only used once
# TODO: remove this function, integrate with generateCircles
def drawCircles():
    for c in Circles:
        c.draw(win)

# Infect a random person 
def infectRandom():
    random.choice(Population).infected = True

# Updates all persons state
# TODO: split the view from the model, do c.move somewhere else
def updatePersons():
    for p in Population:
        
        # Continue if alive
        if(p.alive):
            c = Circles[Population.index(p)]

            if(p.infected):
                c.setFill("red")

                # Kill
                if(random.random() < death_chance):
                    p.alive = False
                    c.setFill("black")
                    continue
                
                # Recover
                if(random.random() < recovery_chance):
                    p.infected = False
                    p.recovered = True
                    c.setFill("green")

            # Move the person
            if(random.random() < move_chance):

                sx = random.randint(-step,step)
                while(p.x + sx >= width or p.x + sx <= 0):
                    sx = random.randint(-step,step)     

                sy = random.randint(-step,step)
                while(p.y + sy >= height or p.y + sy <= 0):
                    sy = random.randint(-step,step)     
                
                p.move(sx, sy)
                c.move(sx, sy)   

# Infect other people 
# N.B. below function has a time complexity of O(n^2), can get slow with large population
def infectOthers():
    infected = []
    for p in Population:
        if(p.infected and p.alive):
            infected.append(p)

    for i in infected:
        xmin = i.x - soi_radius
        xmax = i.x + soi_radius
        ymin = i.y - soi_radius
        ymax = i.y + soi_radius

        for p in Population:
            # Move on to next person if they're recovered and disease offers immunity after recovery
            if(p.recovered and immune_after_recovery):
                continue

            # If person is in the 'sphere of influence' of the infected person, infect them
            if(xmin < p.x < xmax and ymin < p.y < ymax):
                p.infected= True

# Update the SIR compartment statistics for the line graph
def updateStats():
    infected = sum(p.infected == True and p.alive == True for p in Population)
    susceptible = sum(p.infected == False and p.alive == True for p in Population)
    dead = sum(p.alive == False for p in Population)
    recovered = sum(p.alive == True and p.recovered == True for p in Population)

    infected_counter.setText("Amount infected: " + str(infected))
    susceptible_counter.setText("Amount susceptible: " + str(susceptible))
    dead_counter.setText("Amount dead: " + str(dead))
    recovered_counter.setText("Amount recovered: " + str(recovered))
    
    return [susceptible, infected, recovered, dead]

# Show a window in which the user can input parameters, currently not used
def getInputParameters():
    input_win = GraphWin('Input parameters', 400, 300)
    t = Text(Point(190,12), "Please input the parameters for the simulation.")
    t.setSize(13)
    t.setStyle("bold")
    t.draw(input_win)

    Text(Point(107,40), "Population size (n) (0-1000): ").draw(input_win)
    pop_input = Entry(Point(255, 40), 10)
    pop_input.draw(input_win)

    Text(Point(120,70), "Simulation length (default:1000): ").draw(input_win)
    ticks_input = Entry(Point(280, 70), 10)
    ticks_input.draw(input_win)
    
    keyString = win.getKey()
    while(keyString != "Return"):
        time.sleep(delay)
    input_win.close()   

# Draw the counters to the main window to show it
def showMainWindow():
    susceptible_counter.draw(win)
    infected_counter.draw(win)
    dead_counter.draw(win)
    recovered_counter.draw(win)   

def main():
    # getInputParameters()
    # print("Passed input parameters")
    showMainWindow()
    generateRandomPopulation(n)
    generateCircles()
    drawCircles()
    # Infect a random person to start the spread
    infectRandom()

    stats = pd.DataFrame()

    # # Wait until enter is pressed to start the simulation
    # keyString = win.getKey()
    # while(keyString != "Return"):
    #     time.sleep(delay)

    # Time taken to execute the last tick.
    elapsed_time = 0
    for i in range(timesteps):
        start_time = time.time()

        updatePersons()
        infectOthers()

        # Get new stats and append them to the dataframe
        u = updateStats()
        stats = stats.append({'Susceptible': u[0], 'Infected': u[1], 'Recovered': u[2], 'Dead': u[3]}, ignore_index=True)
        # Every 10th tick, update the plot
        if(i % 10 == 0):
            plt.plot(stats['Susceptible'], label = 'Susceptible', c='b')
            plt.plot(stats['Infected'], label = 'Infected', c='r')
            plt.plot(stats['Recovered'],label = 'Recovered', c='g')
            plt.plot(stats['Dead'], label = 'Dead', c='k')
            plt.title("SIR compartments")
            
            # Only add legend on the 0th tick so it doesn't keep duplicating
            if(i == 0):
                plt.legend(prop={'size': 8})

            # Save the plot as a figure, convert it to gif (graphics.py doesnt support jpg), and draw it on screen
            plt.savefig('lib/plot.jpg')
            im = PIL.Image.open('lib/plot.jpg')
            im.save('lib/plot.gif')
            Image(Point(1200,250), 'lib/plot.gif').draw(win)

            # Calculate how long the current tick took to simulate
            elapsed_time = time.time()-start_time

        # If tick took less time than delay, sleep until delay time is met  
        if(elapsed_time < delay):
            time.sleep(delay-elapsed_time)
            print("Sleeping for " + str(delay-elapsed_time) + " seconds.")
    

main()
# Wait for mouse input to close the window
win.getMouse()









