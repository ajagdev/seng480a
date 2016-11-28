
from multiprocessing import *
import unittest
import time
import p3

class TestClass(unittest.TestCase):

	# check if sensors are triggered in p3
	def test_triggers(self):

		EW_ped_button = Value('b', False)
		NS_ped_button = Value('b', False)
		EW_sensor = Value('b', False)
		NS_sensor = Value('b', False)

		p = Process(target=p3.triggers, args=(EW_ped_button, NS_ped_button, EW_sensor, NS_sensor))
		p.daemon = True
		p.start()

		time.sleep(35)

		self.assertTrue(EW_ped_button.value)
		self.assertTrue(NS_ped_button.value)
		self.assertTrue(EW_sensor.value)
		self.assertTrue(NS_sensor.value)

	# check EW ped lights are changed when the specific sensor is triggerd
	def test_EW_ped_lights(self):

		p3.EW = 'red'
		p3.NS = 'green'
		p3.EW_ped = 'red'
		p3.NS_ped = 'red'
		p3.EW_sensor.value = False
		p3.NS_sensor.value = False
		p3.EW_ped_button.value = True
		p3.NS_ped_button.value = False
		p3.timer = 5
		
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)

		self.assertEqual(p3.EW_ped, 'green')

	# check EW lights are changed when the specific sensor is triggerd and make sure that 
	# NS_ped sensor is triggerd but not reached becuase EW is still green
	# and ew_ped sensor is also triggered and it changes from the red to green because that is acceptable state
	def test_EW_lights(self):

		p3.EW = 'red'
		p3.NS = 'green'
		p3.EW_ped = 'red'
		p3.NS_ped = 'red'
		p3.EW_sensor.value = True
		p3.NS_sensor.value = False
		p3.EW_ped_button.value = True
		p3.NS_ped_button.value = True
		p3.timer = 6
		
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		p3.mainLoop(None, True)
		
		# EW light goes green for the cars
		self.assertEqual(p3.EW, 'green')
		# when ew is green and ew ped is pressed the ped can cross
		self.assertEqual(p3.EW_ped, 'green')
		# when the ew is green ped cannot cross from NS
		self.assertEqual(p3.NS_ped, 'red')

if __name__ == '__main__':
	unittest.main()




	""" 
	This is trying to do a exhatisitve search of states to detemine the non-detemenstic testing like tla model checker was not implemented because this is not what was required. and we went back to doing deterministic testing
	def recursiveSearch(self, testCondition, i, EW, NS, EW_ped, NS_ped, EW_sensor, NS_sensor, EW_ped_button, NS_ped_button, timer):
		if testCondition():
			return True
		if i > 900:
			return False

		p3.mainLoop(None, True)
		r1 = self.recursiveSearch(testCondition, i+1, p3.EW, p3.NS, p3.EW_ped, p3.NS_ped, p3.EW_sensor.value, p3.NS_sensor.value, p3.EW_ped_button.value, p3.NS_ped_button.value, p3.timer)
		p3.EW = EW
		p3.NS = NS
		p3.EW_ped = EW_ped
		p3.NS_ped = NS_ped
		p3.EW_sensor.value = EW_sensor
		p3.NS_sensor.value = NS_sensor
		p3.EW_ped_button.value = EW_ped_button
		p3.NS_ped_button.value = NS_ped_button
		p3.timer = timer

		#EW_ped_button
		if not EW_ped_button:
			p3.EW_ped_button.value = True
			p3.mainLoop(None, True)
			r2 = self.recursiveSearch(testCondition, i+1, p3.EW, p3.NS, p3.EW_ped, p3.NS_ped, p3.EW_sensor.value, p3.NS_sensor.value, p3.EW_ped_button.value, p3.NS_ped_button.value, p3.timer)
			p3.EW = EW
			p3.NS = NS
			p3.EW_ped = EW_ped
			p3.NS_ped = NS_ped
			p3.EW_sensor.value = EW_sensor
			p3.NS_sensor.value = NS_sensor
			p3.EW_ped_button.value = EW_ped_button
			p3.NS_ped_button.value = NS_ped_button
			p3.timer = timer

		#NS_ped_button
		if not NS_ped_button:
			p3.NS_ped_button.value = True
			p3.mainLoop(None, True)
			r3 = self.recursiveSearch(testCondition, i+1, p3.EW, p3.NS, p3.EW_ped, p3.NS_ped, p3.EW_sensor.value, p3.NS_sensor.value, p3.EW_ped_button.value, p3.NS_ped_button.value, p3.timer)
			p3.EW = EW
			p3.NS = NS
			p3.EW_ped = EW_ped
			p3.NS_ped = NS_ped
			p3.EW_sensor.value = EW_sensor
			p3.NS_sensor.value = NS_sensor
			p3.EW_ped_button.value = EW_ped_button
			p3.NS_ped_button.value = NS_ped_button
			p3.timer = timer

		#EW_sensor
		if not EW_sensor:
			p3.EW_sensor.value = True
			p3.mainLoop(None, True)
			r4 = self.recursiveSearch(testCondition, i+1, p3.EW, p3.NS, p3.EW_ped, p3.NS_ped, p3.EW_sensor.value, p3.NS_sensor.value, p3.EW_ped_button.value, p3.NS_ped_button.value, p3.timer)
			p3.EW = EW
			p3.NS = NS
			p3.EW_ped = EW_ped
			p3.NS_ped = NS_ped
			p3.EW_sensor.value = EW_sensor
			p3.NS_sensor.value = NS_sensor
			p3.EW_ped_button.value = EW_ped_button
			p3.NS_ped_button.value = NS_ped_button
			p3.timer = timer

		#NS_sensor
		if not NS_sensor:
			p3.NS_sensor.value = True
			p3.mainLoop(None, True)
			r5 = self.recursiveSearch(testCondition, i+1, p3.EW, p3.NS, p3.EW_ped, p3.NS_ped, p3.EW_sensor.value, p3.NS_sensor.value, p3.EW_ped_button.value, p3.NS_ped_button.value, p3.timer)
			p3.EW = EW
			p3.NS = NS
			p3.EW_ped = EW_ped
			p3.NS_ped = NS_ped
			p3.EW_sensor.value = EW_sensor
			p3.NS_sensor.value = NS_sensor
			p3.EW_ped_button.value = EW_ped_button
			p3.NS_ped_button.value = NS_ped_button
			p3.timer = timer

		return (r1 and r2 and r3 and r4 and r5)
	"""		
	