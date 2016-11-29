import tkinter
import graphics
from random import *
from multiprocessing import *
from graphics import *
from visualization import TrafficVisualization
import random

# Generates poison distribution for triggers with a mean time of 1 per 20 seconds for each trigger, not exceeding 30 seconds.
# If nonDeterminism is false just sleeps
def triggers(ew, ns, nonDeterminism):
	global EW_ped_button
	global NS_ped_button
	
	ew_ped_timer = min(random.expovariate(0.00005), 30000)	#Should give 1 instance every 20000 miliseconds
	ns_ped_timer = min(random.expovariate(0.00005), 30000)
	
#triggers:
	while (True):
		if nonDeterminism.value:
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
		else:
			time.sleep(0.1)

def mainLoop(vis):
	timer = 5
	EW = 'green'
	NS = 'red'
	NS_ped = 'red'
	EW_ped = 'red'

#loop:
	while True:
		if (timer > 0):
			timer = timer - 1
			
		if (timer == 3):
			if (EW_ped == 'green'):
				EW_ped = 'yellow'            
			if (NS_ped == 'green'):
				NS_ped = 'yellow'
		
		if (timer == 2):
#ped_yellow
			if (EW == 'red'):
				NS = 'yellow'
			else:
				EW = 'yellow'
		
		if (timer == 0):
#t0:
			EW_ped = 'red'
			NS_ped = 'red'
		
			if (EW == 'red'):
				NS = 'red'
				
				if (EW_ped_button.value == True):
					EW_ped_button.value = False
#ped1:
					EW_ped = 'green'
#ew_green:				
				EW = 'green'
			else:
				EW = 'red'
				
				if (NS_ped_button.value == True):
					NS_ped_button.value = False
#ped2
					NS_ped = 'green'
#ns_green:
				NS = 'green'
#timer_reset:
			timer = 5
			
		for i in range(0,10):
			#Visualization updates
			vis.setEWLights(EW)
			vis.setNSLights(NS)
			vis.setEWPedLights(EW_ped)
			vis.setNSPedLights(NS_ped)
			vis.setPedButtonVisible('EW', EW_ped_button.value)
			vis.setPedButtonVisible('NS', NS_ped_button.value)
			
			vis.readClick()
			
			if vis.checkQuit():
				return

			if vis.checkToggle():
				print('pressed')
				nonDeterminism.value = not nonDeterminism.value
				vis.setToggleMode(nonDeterminism.value)
				
			if vis.checkEWPed():
				EW_ped_button.value = True	
			if vis.checkNSPed():
				NS_ped_button.value = True
			
			time.sleep(0.1)

#Triggers use a different proccess so we need to assert that only the parent process
#	runs the main code.
if __name__ == '__main__':
	EW_ped_button = Value('b', False)
	NS_ped_button = Value('b', False)
	nonDeterminism = Value('b', False)

	#This process will trigger events based on a poison distribution
	p = Process(target=triggers, args=(EW_ped_button, NS_ped_button, nonDeterminism))
	p.daemon = True
	p.start()

	vis = TrafficVisualization(True, False)
	
	mainLoop(vis)
	
	vis.close()