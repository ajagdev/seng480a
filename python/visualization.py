from graphics import *
class Arrow:
	structureNS = [
		Point(0,0),
		Point(10,10),
		Point(5,10),
		Point(5,20),
		Point(-5,20),
		Point(-5,10),
		Point(-10,10)
	]
	structureEW = [
		Point(0,0),
		Point(10,-10),
		Point(10, -5),
		Point(20, -5),
		Point(20, 5),
		Point(10, 5),
		Point(10,10)
	]
	@staticmethod
	def getArrow(origin, direction, scale):
		if direction == 'N':
			return [(lambda x: Point(origin.x + x.x*scale, origin.y + x.y*scale))(x) for x in Arrow.structureNS]
		if direction == 'S':
			return [(lambda x: Point(origin.x - x.x*scale, origin.y - x.y*scale))(x) for x in Arrow.structureNS]
		if direction == 'E':
			return [(lambda x: Point(origin.x - x.x*scale, origin.y - x.y*scale))(x) for x in Arrow.structureEW]
		if direction == 'W':
			return [(lambda x: Point(origin.x + x.x*scale, origin.y + x.y*scale))(x) for x in Arrow.structureEW]

class TrafficVisualization:
	
	#Visualization window
	win = None

	ewRoad = Rectangle(Point(0,300), Point(900,600))
	nsRoad = Rectangle(Point(300,0), Point(600,900))
	
	roadLineElements = [
		Line(Point(450,0), Point(450,190)),
		Line(Point(450,710), Point(450,900)),
		Line(Point(0,450),Point(190,450)),
		Line(Point(710,450), Point(900,450))
	]
	
	crosswalkElements = [
		Rectangle(Point(300, 290), Point(600,300)),
		Rectangle(Point(300, 190), Point(600,200)),
		Rectangle(Point(600, 300), Point(610,600)),
		Rectangle(Point(700, 300), Point(710,600)),
		Rectangle(Point(300, 600), Point(600,610)),
		Rectangle(Point(300, 700), Point(600,710)),
		Rectangle(Point(290, 300), Point(300,600)),
		Rectangle(Point(190, 300), Point(200,600))
	]
	
	#Possible UI buttons
	userClick = None
	quitButton = None
	toggleButton = None
	
	EWPedUserTriggerButton = None
	NSPedUserTriggerButton = None
	EWVehicleUserTriggerButton = None
	NSVehicleUserTriggerButton = None
		
	#Pedestrian UI elements
	EWPedLights = [
		Polygon(Arrow.getArrow(Point(300,250), 'E', 1.3)),
		Polygon(Arrow.getArrow(Point(600,250), 'W', 1.3)),
		Polygon(Arrow.getArrow(Point(300,650), 'E', 1.3)),
		Polygon(Arrow.getArrow(Point(600,650), 'W', 1.3))
	]
	
	EWPedButtons = [
		Circle(Point(290,240), 10),
		Circle(Point(610,240), 10),
		Circle(Point(290,660), 10),
		Circle(Point(610,660), 10)	
	]
	EWPedButtonDrawn = False
	
	NSPedLights = [
		Polygon(Arrow.getArrow(Point(250,300), 'S', 1.3)),
		Polygon(Arrow.getArrow(Point(250,600), 'N', 1.3)),
		Polygon(Arrow.getArrow(Point(650,300), 'S', 1.3)),
		Polygon(Arrow.getArrow(Point(650,600), 'N', 1.3))	
	]
	
	NSPedButtons = [
		Circle(Point(240, 290), 10),
		Circle(Point(240, 610), 10),
		Circle(Point(660, 290), 10),
		Circle(Point(660, 610), 10)
	]
	NSPedButtonDrawn = False
	
	#Street light UI elements
	NSLights = [
		Polygon(Arrow.getArrow(Point(350,320), 'S', 3)),
		Polygon(Arrow.getArrow(Point(550,580), 'N', 3))
	]
	
	NSSensors = [
		Rectangle(Point(350, 100), Point(450, 180)),
		Rectangle(Point(550, 720), Point(450, 800))
	]
	NSSensorsDrawn = False
	
	EWLights = [
		Polygon(Arrow.getArrow(Point(320, 550), 'E', 3)),
		Polygon(Arrow.getArrow(Point(580, 350), 'W', 3))
	]
	
	EWSensors = [
		Rectangle(Point(100, 450), Point(180, 550)),
		Rectangle(Point(720, 350), Point(800, 450))
	]
	EWSensorsDrawn = False
	
	#Creates a new button UI element, p1 should be top left, p2 bottom right
	def createButton(self, p1, p2, text, colour):
		button1 = Rectangle(p1, p2)
		button1.setWidth(8)
		button1.setOutline(colour)
		button1.setFill(colour)
		textX = (p1.x+p2.x)/2
		textY = (p1.y+p2.y)/2
		buttonText = Text(Point(textX,textY), text)
		buttonText.setTextColor('Black')
		buttonText.setSize(18)
		return [button1, buttonText]
		
	#Determines if the user has clicked a button as of the last call to readClick()
	def wasButtonClicked(self, button):
		clickPoint = self.userClick
		if clickPoint is None:
			return False
		if clickPoint.x > button[0].getP1().x and clickPoint.x < button[0].getP2().x and clickPoint.y > button[0].getP1().y and clickPoint.y < button[0].getP2().y:
			return True
		else:
			return False
	
	#Creates a window and draws an intersection. The intersection optionally includes
	#	vehichle sensors and pedestrian crossings.
	def __init__(self, hasPedestrian=False, hasSensors=False):
		self.win = GraphWin("Intersection2", 900, 900)	
		self.win.setBackground("Dark Olive Green")
		
		self.nsRoad.setOutline('Dim Gray')
		self.nsRoad.setFill('Dim Gray')
		self.ewRoad.setOutline('Dim Gray')
		self.ewRoad.setFill('Dim Gray')
		
		self.nsRoad.draw(self.win)
		self.ewRoad.draw(self.win)
		
		self.quitButton = self.createButton(Point(800,0), Point(900,100), 'Quit', 'Red')
		for e in self.quitButton:
			e.draw(self.win)
			
		#we only need automatic non-determanism if there are pedestrians or sensors
		if hasPedestrian or hasSensors:
			self.toggleButton = self.createButton(Point(800,110), Point(900,210), 'Auto', 'Dark Green')
			for e in self.toggleButton:
				e.draw(self.win)
				
		for e in self.roadLineElements:
			e.setWidth(10)
			e.setOutline('Yellow')
			e.draw(self.win)
	
		
		if hasPedestrian:
			for e in self.crosswalkElements:
				e.setOutline('White')
				e.setFill('White')
				e.draw(self.win)
				
			for e in self.NSPedLights + self.EWPedLights:
				e.setFill('red')
				e.draw(self.win)
				
			for e in self.EWPedButtons + self.NSPedButtons:
				e.setFill('Yellow')
				
			self.NSPedUserTriggerButton = self.createButton(Point(0,0), Point(100,100), 'Ped:\nNS', 'Light Blue')
			self.EWPedUserTriggerButton = self.createButton(Point(130,0), Point(230,100), 'Ped:\nEW', 'Light Blue')
			for e in self.NSPedUserTriggerButton + self.EWPedUserTriggerButton:
				e.draw(self.win)	
				
		if hasSensors:
			for e in self.NSSensors + self.EWSensors:
				e.setWidth(5)
				e.setOutline('Yellow')
			
			self.NSVehicleUserTriggerButton = self.createButton(Point(0,130), Point(100,230), 'Car:\nNS', 'Blue')
			self.EWVehicleUserTriggerButton = self.createButton(Point(130,130), Point(230,230), 'Car:\nEW', 'Blue')
			for e in self.EWVehicleUserTriggerButton + self.NSVehicleUserTriggerButton:
				e.draw(self.win)	
				
		for e in self.EWLights + self.NSLights:
			e.setFill('Red')
			e.draw(self.win)
		
	#Sets the colour of the EW traffic lights (ie "Red", "Yellow", "Green" etc)
	def setEWLights(self, newColour):
		for e in self.EWLights:
			e.setFill(newColour)
	
	#Sets the colour of the NS traffic lights (ie "Red", "Yellow", "Green" etc)	
	def setNSLights(self, newColour):
		for e in self.NSLights:
			e.setFill(newColour)

	#Sets the colour of the EW pedestrian lights (ie "Red", "Yellow", "Green" etc)	
	def setEWPedLights(self, newColour):
		for e in self.EWPedLights:
			e.setFill(newColour)
	
	#Sets the colour of the NS pedestrian lights (ie "Red", "Yellow", "Green" etc)	
	def setNSPedLights(self, newColour):
		for e in self.NSPedLights:
			e.setFill(newColour)
	
	#Shows an indication that a pedestrian button has been pressed (Direction is 'NS', or 'EW')
	def setPedButtonVisible(self, direction, show):
		if direction == 'EW':
			set = self.EWPedButtons
			if show:
				if self.EWPedButtonDrawn:
					return
				else:
					self.EWPedButtonDrawn = True
			else:
				self.EWPedButtonDrawn = False
		elif direction == 'NS':
			set = self.NSPedButtons
			if show:
				if self.NSPedButtonDrawn:
					return
				else:
					self.NSPedButtonDrawn = True
			else:
				self.NSPedButtonDrawn = False
		else:
			return


		for e in set:
			if show:
				e.draw(self.win)
			else:
				e.undraw()
	
	#Shows an indication that a vehicle sensor has been triggered (Direction is 'NS', or 'EW')
	def setSensorVisible(self, direction, show):
		if direction == 'EW':
			set = self.EWSensors
			if show:
				if self.EWSensorsDrawn:
					return
				else:
					self.EWSensorsDrawn = True
			else:
				self.EWSensorsDrawn = False
		elif direction == 'NS':
			set = self.NSSensors
			if show:
				if self.NSSensorsDrawn:
					return
				else:
					self.NSSensorsDrawn = True
			else:
				self.NSSensorsDrawn = False
		else:
			return


		for e in set:
			if show:
				e.draw(self.win)
			else:
				e.undraw()
			
	#Reads any user input since the last call to readClick(), returns None if there was no input
	def readClick(self):
		self.userClick = self.win.checkMouse()
				
	#Checks if the exit button has been pressed
	def checkQuit(self):
		return self.wasButtonClicked(self.quitButton)
		
	#Checks if the auto toggle has been pressed
	def checkToggle(self):
		return self.toggleButton is not None and self.wasButtonClicked(self.toggleButton)
		
	#Checks if the EW/NS pedestrian buttons have been pressed
	def checkEWPed(self):
		return self.EWPedUserTriggerButton is not None and self.wasButtonClicked(self.EWPedUserTriggerButton)	
	def checkNSPed(self):
		return self.NSPedUserTriggerButton is not None and self.wasButtonClicked(self.NSPedUserTriggerButton)
	
	#Checks if the EW/NS vehicle buttons have been pressed
	def checkEWCar(self):
		return self.EWVehicleUserTriggerButton is not None and self.wasButtonClicked(self.EWVehicleUserTriggerButton)	
	def checkNSCar(self):
		return self.NSVehicleUserTriggerButton is not None and self.wasButtonClicked(self.NSVehicleUserTriggerButton)
		
	#Sets the display of the auto toggle
	def setToggleMode(self, mode):
		if mode:
			self.toggleButton[0].setFill('Green')
		else:
			self.toggleButton[0].setFill('Dark Green')
			
	#Closes the window
	def close(self):
		self.win.close()
