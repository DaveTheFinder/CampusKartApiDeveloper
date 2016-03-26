#!/usr/bin/python
import math
import serial
import time
import struct
from gps3 import gps3
from evdev import InputDevice, categorize, ecodes, KeyEvent
import sys
sys.path.append('/home/pi/ApiDeveloper/CampusKartApiDeveloper/Compass/quick2wire-python-api')
from i2clibraries import i2c_hmc5883l
from i2clibraries import i2c_adxl345
from api import Api

#Global variables
latitud = 28.673942
longitud = -106.082439
int_actualPoint = 0

#- CLASSES -#
#Coordinates
#Longitud = x, latitud = y
class Coordinate:
    def __init__(self,y,x,z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x;
    def getY(self):
        return self.y;
    def getZ(self):
        return self.z;
    def printCoor(self):      
        print("== Kart GPS Location ==")
        print(self.y,", ",self.x)
    def printFile(self):
        return str(self.y)+","+str(self.x)+"\n"

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
    return Coordinate(latitud,longitud, 0.0);

#Call to get the heading of the compass
def get_KartHeading(hmc5883l):
    (degress, minutes) = hmc5883l.getHeading()
    heading = hmc5883l.getHeadingString()
    degrees = heading.split("°")
    return isFloat(degrees[0])

#Call to get a test kart location
def get_KartLocationTest():
    return Coordinate(28.674793, -106.079706, 0.0)


#Call to get the next location the car must go
def get_KartDestination():
    array_point = [Coordinate(28.674735, -106.076224, 0),
                   Coordinate(28.674771, -106.076305, 0),
                   Coordinate(28.674649, -106.076788, 0)]
                   #Coordinate(28.675005, -106.08248, 0.0),
                   #Coordinate(28.675001667, -106.08245, 0.0),
                   #Coordinate(28.675013333, -106.08244, 0.0),
                   #Coordinate(28.675051667, -106.082433333, 0.0),
                   #Coordinate(28.675083333, -106.082448333, 0.0),
                   #Coordinate(28.675098333, -106.082451667, 0.0),
                   #Coordinate(28.675115, -106.082458333, 0.0),
                   #Coordinate(28.675155, -106.082451667, 0.0),
                   #Coordinate(28.675171667, -106.082431667, 0.0)]
    global int_actualPoint
    if int_actualPoint < 3:
        return array_point[int_actualPoint]
    else:
        return array_point[0]

#Call to know if you are close enough to the actual point
def get_KartNextPoint(point_Destination, point_Kart):
    distance = math.sqrt(math.pow(point_Destination.getY() - point_Kart.getY(),2) + math.pow(point_Destination.getX() - point_Kart.getX(),2))
    #point_Destination.printCoor()
    
    #print(distance)
    if distance < 0.00005:
        print("NEXT POINT")
        global int_actualPoint
        int_actualPoint+=1

#Get the angle adjusted with tilt compensation
def getHeadingComp():
        (aX,aY,aZ) = adxl345.getAxes()
        (mX,mY,mZ) = hmc5883l.getAxes()
        accX = -aY
        accY = -aX
        rollRadians = math.asin(accY)
        pitchRadians = math.asin(accX)

        if(rollRadians > 0.78 or rollRadians < -0.78 or pitchRadians > 0.78 or pitchRadians < -0.78):
                return 0
        cosRoll = math.cos(rollRadians)
        sinRoll = math.sin(rollRadians)
        cosPitch = math.cos(pitchRadians)
        sinPitch = math.sin(pitchRadians)

        Xh = mX*cosPitch+mZ*sinPitch
        Yh = mX*sinRoll*sinPitch+mY*cosRoll-mZ*sinRoll*cosPitch
        heading = math.atan2(Yh,Xh)
        return heading

#Radians to degrees
def RadiansToDegrees(rads):
        if(rads < 0):
                rads = rads+2*math.pi
        if(rads > 2*math.pi):
                rads = rads-2*math.pi

        heading = rads*180/math.pi
        return heading

#Full calculation code, called everytime the compass changes
def get_NewAngle(heading_Kart):
    #Points to draw the triangle
    point_Kart = get_KartLocation()
    point_Destination = get_KartDestination()
    point_Support = Coordinate(point_Destination.getY(),point_Kart.getX(), 0.0)

    #Check if you should go to the next point
    get_KartNextPoint(point_Destination, point_Kart)

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
    adjustedAngle = 90 - (heading_Kart + point_Destination.getZ())
    if adjustedAngle < 0:
        adjustedAngle = adjustedAngle + 360

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

    #Final comparison with heading_Kart to get the new heading to adjust direction
    if adjustedAngle > fullOpposite:
        newHeading_Kart = +(adjustedAngle - fullOpposite)
    else:
        newHeading_Kart = -(fullOpposite - adjustedAngle)

    #Optimization of angles for smaller angle
    if newHeading_Kart > 180:
        newHeadingAdjusted_Kart = newHeading_Kart - 360
    elif newHeading_Kart < -180:
        newHeadingAdjusted_Kart = newHeading_Kart + 360
    else:
        newHeadingAdjusted_Kart = newHeading_Kart

    #return point_Destination.getZ();
    return newHeadingAdjusted_Kart;

    
#- Main code -#

#File to write the data
archivo = open("coordenadas.txt","a")
archivo.write("Inicio\n")

#Interface with the controller
gamepad = InputDevice("/dev/input/event0")
print(gamepad)

#Interface with the GPS
gps_connection = gps3.GPSDSocket(host='127.0.0.1')
gps_fix = gps3.Fix()

#Interface with the Compass
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
hmc5883l.setContinuousMode()
hmc5883l.setDeclination(8,0)

adxl345 = i2c_adxl345.i2c_adxl345(1)

direccionFinal = 1

#Instance of the API
api = Api("carroV1")

compassHeading = None
velocity = 0
manual = True

while True:    
    event = gamepad.read_one()
    x = api.Read()
    if(x == True):
        velocity = 0
        api.POSTVel(velocity)
        print("EMERGENCIA")
    if event != None:
        #print(event)
        if event.code == 17 and event.value == -1:
           
                    
            velocity = velocity + 1
            if velocity >= 10:
                velocity = 10
                    
        if event.code == 17 and event.value == 1:
            velocity = velocity -1
            if(velocity <= 0):
                velocity = 0
        if event.code == 315 and event.value == 1:
            manual = not manual
        if event.code == 305 and event.value == 1:
            velocity = 0
        if event.code == 307 and event.value == 1:
            #compassHeading = get_KartHeading(hmc5883l)
            compassHeading = RadiansToDegrees(getHeadingComp())
            archivo.write(get_KartLocation().printFile())
        api.POSTVel(velocity)
        #print("Velocidad" + str(velocity))
        #time.sleep(.01)
    if(manual):
        if(event != None):
            if (event.code == 3 or event.code == 0) and event.type == 3:
                direccionFinal = int((event.value + 32768)/256)
                #print("DireccionC2 "+ str(direccionFinal))
                api.POSTDir(int(direccionFinal/(255/50)))
                print("DIreccionC2 " + str(int(direccionFinal/(255/50))))
    if(not manual):
        #compassHeading = get_KartHeading(hmc5883l)
        compassHeading = RadiansToDegrees(getHeadingComp())
        #print(compassHeading)
        #newHeadingAdjusted_Kart = get_NewAngle(isFloat(compassHeading))
        newHeadingAdjusted_Kart = get_NewAngle(isFloat(compassHeading))
        #print("== New adjusted heading ==")
        #print(newHeadingAdjusted_Kart)
        sentAngle = newHeadingAdjusted_Kart
        #sentAngle = newHeadingAdjusted_Kart
        #print(sentAngle)
        if sentAngle > 50:
            sentAngle = 50
        elif sentAngle < 0:
            sentAngle = 0

        sentAngle = int(sentAngle)
        #if(direccionFinal != sentAngle):
        if(abs(direccionFinal - sentAngle)>20):
            api.POSTDir(sentAngle)
            direccionFinal = sentAngle
            #print(direccionFinal)
        #print(sentAngle)
                
    #asciiuino.close()
    #except:
        #pass
    #else:
        #break
    #print("reiniciando")
    #time.sleep(5)
    #archivo.close()
 
