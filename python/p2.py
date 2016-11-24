import tkinter
import graphics
from random import *
from multiprocessing import *
from graphics import *

def triggers(ew, ns):
	global EW_ped_button
	global NS_ped_button
	while (True):
		choice = randint(0, 20)
		if (choice == 0):
			ew.value = True
		choice = randint(0, 20)
		if (choice == 0):
			ns.value = True
		time.sleep(1)

		
if __name__ == '__main__':
	EW_ped_button = Value('b', False)
	NS_ped_button = Value('b', False)

	p = Process(target=triggers, args=(EW_ped_button, NS_ped_button))
	p.start()
	
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

	northPedLoc = Point(630, 680)
	southPedLoc = Point(270, 220)
	eastPedLoc = Point (220, 630)
	westPedLoc = Point (680, 270)

	northLight = Circle(northLoc, 30)
	southLight = Circle(southLoc, 30)
	eastLight = Circle(eastLoc, 30)
	westLight = Circle(westLoc, 30)

	northPedLight = Circle(northPedLoc, 15)
	southPedLight = Circle(southPedLoc, 15)
	eastPedLight = Circle(eastPedLoc, 15)
	westPedLight = Circle(westPedLoc, 15)

	northLight.setFill('red')
	southLight.setFill('red')
	eastLight.setFill('red')
	westLight.setFill('red')

	northPedLight.setFill('red')
	southPedLight.setFill('red')
	eastPedLight.setFill('red')
	westPedLight.setFill('red')

	nsRoad.draw(win)
	ewRoad.draw(win)

	northLight.draw(win)
	southLight.draw(win)
	eastLight.draw(win)
	westLight.draw(win)
	northPedLight.draw(win)
	southPedLight.draw(win)
	eastPedLight.draw(win)
	westPedLight.draw(win)

	timer = 5
	EW = 'green'
	NS = 'red'
	NS_ped = 'red'
	EW_ped = 'red'

	
	while True:
		if (timer > 0):
			timer = timer - 1
			
		if (timer == 3):
			if (EW_ped == 'green'):
				EW_ped = 'yellow'            
			if (NS_ped == 'green'):
				NS_ped = 'yellow'
		
		if (timer == 2):
			if (EW == 'red'):
				NS = 'yellow'
			else:
				EW = 'yellow'
		
		if (timer == 0):
			EW_ped = 'red'
			NS_ped = 'red'
		
			if (EW == 'red'):
				NS = 'red'
				
				if (EW_ped_button.value == True):
					EW_ped_button.value = False
					EW_ped = 'green'
				
				EW = 'green'
			else:
				NS = 'green'
				EW = 'red'
				
				if (NS_ped_button.value == True):
					NS_ped_button.value = False
					NS_ped = 'green'
				
			timer = 5
			
		northLight.setFill(NS)
		southLight.setFill(NS)
		eastLight.setFill(EW)
		westLight.setFill(EW)
		
		northPedLight.setFill(NS_ped)
		southPedLight.setFill(NS_ped)
		eastPedLight.setFill(EW_ped)
		westPedLight.setFill(EW_ped)
		
		time.sleep(1)
	p.join()