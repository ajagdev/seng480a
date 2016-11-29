import tkinter
import graphics
from graphics import *

from visualization import TrafficVisualization

timer = 5
EW = 'green'
NS = 'red'

#Direct translation of project1.tla Pluscal algorithm.
#	Will loop until the user clicks the quit button in the visualization.
def mainLoop():
	global timer
	global EW
	global NS
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
			
		for i in range(0,10):
			vis.setEWLights(EW)
			vis.setNSLights(NS)
			
			vis.readClick()
			if vis.checkQuit():
				return
			time.sleep(0.1)
	
vis = TrafficVisualization(False, False)
mainLoop()
vis.close()
			