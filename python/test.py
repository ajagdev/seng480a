
from multiprocessing import *
import unittest
import time


from p3 import triggers

class TestClass(unittest.TestCase):

    def test_triggers(self):

		EW_ped_button = Value('b', False)
		NS_ped_button = Value('b', False)
		EW_sensor = Value('b', False)
		NS_sensor = Value('b', False)

		p = Process(target=triggers, args=(EW_ped_button, NS_ped_button, EW_sensor, NS_sensor))
		p.daemon = True
		p.start()

		time.sleep(35)

		self.assertTrue(EW_ped_button.value)
		self.assertTrue(NS_ped_button.value)
		self.assertTrue(EW_sensor.value)
		self.assertTrue(NS_sensor.value)

if __name__ == '__main__':
	unittest.main()
	