#!/usr/bin/python
import math
import serial
import time
import struct
from gps3 import gps3
from api import Api

#Global variables
latitud = 28.674793
longitud = -106.079706

#- CLASSES -#
#Coordinates
#Longitud = x, latitud = y
class Coordinate:
    def __init__(self,y,x):
        self.x = x
        self.y = y

    def getX(self):
        return self.x;
    def getY(self):
        return self.y;
    def printCoor(self):
        print("== Kart GPS Location ==")
        print(self.y,", ",self.x)

#- Methods -#
#Method to convert string to float
def isFloat(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

#Check if GPS brought a valid value
def isGPS(gps_fix):
    try:
        float(gps_fix.TPV['lon'])
        float(gps_fix.TPV['lat'])
        return True
    except ValueError:
        return False

#Call to get the coordinates of the GPS
def get_KartLocation():
    for new_data in gps_connection:
        if new_data:
            gps_fix.refresh(new_data)
            if isGPS(gps_fix):
                global longitud
                global latitud
                longitud = isFloat(gps_fix.TPV['lon'])
                latitud = isFloat(gps_fix.TPV['lat'])
        break
    return Coordinate(latitud,longitud);

#Call to get a test kart location
def get_KartLocationTest():
    return Coordinate(28.674793, -106.079706)

#Call to get the next location the car must go
def get_KartDestination():
    return Coordinate(28.673943, -106.079427);

#Full calculation code, called everytime the compass changes
def get_NewAngle(heading_Kart):
    #Points to draw the triangle
    point_Kart = get_KartLocation()
    #point_Kart = get_KartLocationTest()
    point_Kart.printCoor()
    point_Destination = get_KartDestination()
    point_Support = Coordinate(point_Destination.getY(),point_Kart.getX())

    hypotenuse = math.sqrt(math.pow(point_Destination.getY() - point_Kart.getY(),2) + math.pow(point_Destination.getX() - point_Kart.getX(),2))
    side = abs(point_Destination.getX() - point_Kart.getX())

    adjacentAngle = math.degrees(math.acos(side/hypotenuse))
    oppositeAngle = 90 - adjacentAngle

    #Quadrant of destination considering point_Kart as origin
    if point_Destination.getX() > point_Kart.getX() and point_Destination.getY() > point_Kart.getY():
        quadrant = 1
    elif point_Destination.getX() < point_Kart.getX() and point_Destination.getY() > point_Kart.getY():
        quadrant = 2
    elif point_Destination.getX() < point_Kart.getX() and point_Destination.getY() < point_Kart.getY():
        quadrant = 3
    elif point_Destination.getX() > point_Kart.getX() and point_Destination.getY() < point_Kart.getY():
        quadrant = 4
    else:
        quadrant = 0

    #Adjust the heading to an angle in a circle starting in 0 degrees
    adjustedAngle = 90 - heading_Kart
    if adjustedAngle < 0:
        adjustedAngle = adjustedAngle + 360

    #print("Heading Kart")
    #print(heading_Kart)
    #print("Full heading")
    #print(adjustedAngle)

    if quadrant == 1:
        fullOpposite = 90 - oppositeAngle
    elif quadrant == 2:
        fullOpposite = 90 + oppositeAngle
    elif quadrant == 3:
        fullOpposite = 270 - oppositeAngle
    elif quadrant == 4:
        fullOpposite = 270 + oppositeAngle
    else:
        fullOpposite = 0

    #print("Full Opposite")
    #print(fullOpposite)

    #Final comparison with heading_Kart to get the new heading to adjust direction
    if adjustedAngle > fullOpposite:
        newHeading_Kart = +(adjustedAngle - fullOpposite)
    else:
        newHeading_Kart = -(fullOpposite - adjustedAngle)

    #print("New heading")
    #print(newHeading_Kart)

    #Optimization of angles for smaller angle
    if newHeading_Kart > 180:
        newHeadingAdjusted_Kart = newHeading_Kart - 360
    elif newHeading_Kart < -180:
        newHeadingAdjusted_Kart = newHeading_Kart + 360
    else:
        newHeadingAdjusted_Kart = newHeading_Kart

    return newHeadingAdjusted_Kart;
    
#- Main code -#
#Interface with the GPS
gps_connection = gps3.GPSDSocket(host='127.0.0.1')
gps_fix = gps3.Fix()

#Get the heading updates from the Arduino
api = Api("carrito")
arduino=serial.Serial('/dev/ttyACM0',baudrate=9600, timeout = 3.0)
arduino.isOpen()
compassHeading = None
api.POSTVel(0)
#api.POSTDir(90)
while True:
    time.sleep(0.1)
    while arduino.inWaiting()>0:
        compassHeading = arduino.readline().decode('UTF-8')
        compassHeading = compassHeading.rstrip()
        print("== Compass ==")
        print(compassHeading)

        newHeadingAdjusted_Kart = get_NewAngle(isFloat(compassHeading))
        HeadingCar = 90 + newHeadingAdjusted_Kart
        print("original: " + str(newHeadingAdjusted_Kart))
        if HeadingCar >130:
            HeadingCar = 130
        elif HeadingCar <50:
            HeadingCar = 50
        #newHeadingAdjusted_Kart = get_NewAngle(0)
        print("== New adjusted heading ==")
        print(HeadingCar)
        
        print()
arduino.close()

 
