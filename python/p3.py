import tkinter
import visualization
import time
import random
from multiprocessing import *
from visualization import TrafficVisualization


# Generates poison distribution for triggers with a mean time of 1 per 20 seconds for each trigger, not exceeding 30 seconds.
# If nonDeterminism is false just sleeps
def triggers(ew, ns, ew_sensor, ns_sensor, nonDeterminism):
	
	ew_ped_timer = min(random.expovariate(0.00005), 30000)	#Should give 1 instance every 20000 miliseconds
	ns_ped_timer = min(random.expovariate(0.00005), 30000)
	ew_sensor_timer = min(random.expovariate(0.00005), 30000)
	ns_sensor_timer = min(random.expovariate(0.00005), 30000)
	
#triggers:
	while (True):
		if nonDeterminism.value:
			if (ew_ped_timer <= 0):
				ew.value = True
				ew_ped_timer = min(random.expovariate(0.00005), 30000)
			
			if (ns_ped_timer <= 0):
				ns.value = True
				ns_ped_timer = min(random.expovariate(0.00005), 30000)

			if (ew_sensor_timer <= 0):
				ew_sensor.value = True
				ew_sensor_timer = min(random.expovariate(0.00005), 30000)

			if (ns_sensor_timer <= 0):
				ns_sensor.value = True
				ns_sensor_timer = min(random.expovariate(0.00005), 30000)
			
			sleep_time = min(ew_ped_timer,ns_ped_timer,ew_sensor_timer,ns_sensor_timer)
			ew_ped_timer -= sleep_time
			ns_ped_timer -= sleep_time
			ew_sensor_timer -= sleep_time
			ns_sensor_timer -= sleep_time
			time.sleep(sleep_time/1000.0)
		else:
			time.sleep(0.1)


timer = -1
EW = 'green'
NS = 'red'
NS_ped = 'red'
EW_ped = 'red'	
EW_ped_button = Value('b', False)
NS_ped_button = Value('b', False)
EW_sensor = Value('b', False)
NS_sensor = Value('b', False)	
nonDeterminism = Value('b', False)

def mainLoop(vis, singleStep=False):

	#Added for ease of unit testing
	global timer
	global EW
	global NS
	global NS_ped
	global EW_ped
	global EW_ped_button
	global NS_ped_button
	global EW_sensor
	global NS_sensor
	global nonDeterminism
	
#loop:
	while True:
		if (timer >= 0):
			timer = timer - 1
			
		if (timer == 3):
			if (EW_ped == 'green'):
				EW_ped = 'yellow'            
			if (NS_ped == 'green'):
				NS_ped = 'yellow'
#ped_yellow:				
		if (timer == 2):
			if (EW == 'red'):
				NS = 'yellow'
			else:
				EW = 'yellow'
#t0:				
		if (timer == 0):
			EW_ped = 'red'
			NS_ped = 'red'
		
			if (EW == 'red'):
				NS = 'red'
				
				if (EW_ped_button.value == True):
					EW_ped_button.value = False
#ped1:
					EW_ped = 'green'
#ew_green:				
				EW_sensor.value = False
				EW = 'green'
			else:
				EW = 'red'
				
				if (NS_ped_button.value == True):
					NS_ped_button.value = False
#ped2:
					NS_ped = 'green'
#ns_green:					
				NS_sensor.value = False
				NS = 'green'
#sensor:				
		if (timer == -1):
			if ((EW == 'green' and NS_sensor.value == True) or \
				(NS == 'green' and EW_sensor.value == True) or \
				NS_ped_button.value == True or \
				EW_ped_button.value == True):
#timer_reset:
				timer = 5
			
		if not singleStep:
			for i in range(0,10):
				vis.setEWLights(EW)
				vis.setNSLights(NS)
				vis.setEWPedLights(EW_ped)
				vis.setNSPedLights(NS_ped)
				vis.setPedButtonVisible('EW', EW_ped_button.value)
				vis.setPedButtonVisible('NS', NS_ped_button.value)
				vis.setSensorVisible('NS', NS_sensor.value)
				vis.setSensorVisible('EW', EW_sensor.value)
				
				vis.readClick()
				
				if vis.checkQuit():
					return
				
				if vis.checkToggle():
					nonDeterminism.value = not nonDeterminism.value
					vis.setToggleMode(nonDeterminism.value)
					
				if vis.checkEWPed():
					EW_ped_button.value = True	
				if vis.checkNSPed():
					NS_ped_button.value = True
				if vis.checkEWCar():
					EW_sensor.value = True
				if vis.checkNSCar():
					NS_sensor.value = True
				
				time.sleep(0.1)
		else:
			return
	
#Triggers use a different proccess so we need to assert that only the parent process
#	runs the main code	
if __name__ == '__main__':

	#This process will trigger events based on a poison distribution
	p = Process(target=triggers, args=(EW_ped_button, NS_ped_button, EW_sensor, NS_sensor, nonDeterminism))
	p.daemon = True
	p.start()
	
	vis = TrafficVisualization(True, True)

	mainLoop(vis)

	vis.close()
