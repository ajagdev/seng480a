import tkinter
import graphics
from graphics import *

from visualization import TrafficVisualization

timer = 5
EW = 'green'
NS = 'red'

vis = TrafficVisualization(False, False)

#Direct translation of project1.tla Pluscal algorithm.
#	Will loop until the user clicks the quit button in the visualization.
while not vis.checkQuit():
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
		
	vis.setEWLights(EW)
	vis.setNSLights(NS)

	#The logical timer is arbitrarialy set to one second.
	time.sleep(1)
vis.close()
			