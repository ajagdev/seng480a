import tkinter
import graphics
from random import *
from multiprocessing import *
from graphics import *
from visualization import TrafficVisualization
import random

# Generates poison distribution for triggers with a mean time of 1 / 20 seconds for each trigger, not exceeding 30 seconds.
def triggers(ew, ns):
	global EW_ped_button
	global NS_ped_button
	
	ew_ped_timer = random.expovariate(0.00005)	#Should give 1 instance every 20000 miliseconds
	ns_ped_timer = random.expovariate(0.00005)
	
	while (True):
		if (ew_ped_timer <= 0):
			ew.value = True
			ew_ped_timer = min(random.expovariate(0.00005), 30000)
		
		if (ns_ped_timer <= 0):
			ns.value = True
			ns_ped_timer = min(random.expovariate(0.00005), 30000)
		
		sleep_time = min(ew_ped_timer,ns_ped_timer)
		ew_ped_timer -= sleep_time
		ns_ped_timer -= sleep_time
		time.sleep(sleep_time/1000.0)

		
if __name__ == '__main__':
	EW_ped_button = Value('b', False)
	NS_ped_button = Value('b', False)

	p = Process(target=triggers, args=(EW_ped_button, NS_ped_button))
	p.daemon = True
	p.start()

	vis = TrafficVisualization(True, False)
	
	timer = 5
	EW = 'green'
	NS = 'red'
	NS_ped = 'red'
	EW_ped = 'red'

	
	while not vis.checkQuit():
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
			
		vis.setEWLights(EW)
		vis.setNSLights(NS)
		vis.setEWPedLights(EW_ped)
		vis.setNSPedLights(NS_ped)
		vis.setPedButtonVisible('EW', EW_ped_button.value)
		vis.setPedButtonVisible('NS', NS_ped_button.value)
		
		time.sleep(1)
	vis.close()