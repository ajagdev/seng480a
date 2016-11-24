import tkinter
import graphics
from graphics import *

win = GraphWin("Intersection", 900, 900)
win.setBackground("Dark Olive Green")



ewRoad = Rectangle(Point(0,300), Point(900,600))
nsRoad = Rectangle(Point(300,0), Point(600,900))
nsRoad.setOutline('Dim Gray')
nsRoad.setFill('Dim Gray')
ewRoad.setOutline('Dim Gray')
ewRoad.setFill('Dim Gray')

northLoc = Point(600, 650)
southLoc = Point(300, 250)
eastLoc = Point (250, 600)
westLoc = Point (650, 300)

northLight = Circle(northLoc, 30)
southLight = Circle(southLoc, 30)
eastLight = Circle(eastLoc, 30)
westLight = Circle(westLoc, 30)

northLight.setFill('red')
southLight.setFill('red')
eastLight.setFill('red')
westLight.setFill('red')

nsRoad.draw(win)
ewRoad.draw(win)

northLight.draw(win)
southLight.draw(win)
eastLight.draw(win)
westLight.draw(win)

timer = 5
EW = 'green'
NS = 'red'
while True:
	if (timer > 0):
		timer = timer - 1
	if (timer == 2):
		if (EW == 'red'):
			NS = 'yellow'
		else:
			EW = 'yellow'
	
	if (timer == 0):
		if (EW == 'red'):
			EW = 'green'
			NS = 'red'
		else:
			NS = 'green'
			EW = 'red'
			
		timer = 5
		
	northLight.setFill(NS)
	southLight.setFill(NS)
	eastLight.setFill(EW)
	westLight.setFill(EW)
	
	time.sleep(1)
			