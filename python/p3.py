import tkinter
import visualization
import time
import random
from multiprocessing import *
from visualization import TrafficVisualization

def triggers(ew, ns, ew_sensor, ns_sensor):
	global EW_ped_button
	global NS_ped_button
	
	ew_ped_timer = random.expovariate(0.00005)	#Should give 1 instance every 20000 miliseconds
	ns_ped_timer = random.expovariate(0.00005)
	ew_sensor_timer = random.expovariate(0.00005)
	ns_sensor_timer = random.expovariate(0.00005)
	
	while (True):
		if (ew_ped_timer <= 0):
			ew.value = True
			ew_ped_timer = random.expovariate(0.00005)
		
		if (ns_ped_timer <= 0):
			ns.value = True
			ns_ped_timer = random.expovariate(0.00005)

		if (ew_sensor_timer <= 0):
			ew_sensor.value = True
			ew_sensor_timer = random.expovariate(0.00005)

		if (ns_sensor_timer <= 0):
			ns_sensor.value = True
			ns_sensor_timer = random.expovariate(0.00005)
		
		sleep_time = min(ew_ped_timer,ns_ped_timer,ew_sensor_timer,ns_sensor_timer)
		ew_ped_timer -= sleep_time
		ns_ped_timer -= sleep_time
		ew_sensor_timer -= sleep_time
		ns_sensor_timer -= sleep_time
		time.sleep(sleep_time/1000.0)
	
def main():
	EW_ped_button = Value('b', False)
	NS_ped_button = Value('b', False)
	EW_sensor = Value('b', False)
	NS_sensor = Value('b', False)

	p = Process(target=triggers, args=(EW_ped_button, NS_ped_button, EW_sensor, NS_sensor))
	p.daemon = True
	p.start()

	timer = -1
	EW = 'green'
	NS = 'red'
	NS_ped = 'red'
	EW_ped = 'red'
	
	vis = TrafficVisualization(True, True)
	
	while not vis.checkQuit():
		if (timer >= 0):
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
				
				EW_sensor.value = False
				EW = 'green'
			else:
				EW = 'red'
				
				if (NS_ped_button.value == True):
					NS_ped_button.value = False
					NS_ped = 'green'
					
				NS_sensor.value = False
				NS = 'green'
				
		if (timer == -1):
			if ((EW == 'green' and NS_sensor.value == True) or \
				(NS == 'green' and EW_sensor.value == True) or \
				NS_ped_button.value == True or \
				EW_ped_button.value == True):
				timer = 5
			
		
		vis.setEWLights(EW)
		vis.setNSLights(NS)
		vis.setEWPedLights(EW_ped)
		vis.setNSPedLights(NS_ped)
		vis.setPedButtonVisible('EW', EW_ped_button.value)
		vis.setPedButtonVisible('NS', NS_ped_button.value)
		vis.setSensorVisible('NS', NS_sensor.value)
		vis.setSensorVisible('EW', EW_sensor.value)
		
		time.sleep(1)
	vis.close()

	
if __name__ == '__main__':
	main()