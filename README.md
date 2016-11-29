# Set up
    SENG 480A - undergraduate project
	
	To run TLA files:

		Project1:
			Properties to check:
				NoCollisions
				Cycle

		Project2:
			Properties to check:
				Properties
				p1!Cycle
				p1!NoCollisions


		Project3:
			Properties to check:
				Sensors
				p2!Properties
				p2!p1!NoCollisions
				p2!p1!Cycle
				


	To run the python implementation:
		1) Make sure you have python 3 (tkinter module should come with python 3)
		2) make sure that you have graphics.py included in the same env as the project files
		3) exectue "python <file name>.py" on windows, or "python3 <file name>.py" on Unix systems
		
	UI:
		The UI for parts 2 and 3 include an Auto button as well as trigger buttons. The Auto button
		will enable a poison distribution generator which will automatically trigger the behaviour.
		The trigger buttons allow manual triggering of the various events even if the automatic mode
		is enabled.


	To execute testing:
		1) exectue "python test.py"

		If there are no errors the sample output will be 
		
		Sample Output:
		...
		----------------------------------------------------------------------
		Ran 3 tests in 35.002s

		OK
		
		
