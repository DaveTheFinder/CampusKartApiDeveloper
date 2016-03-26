import time
import sys
sys.path.append('/home/pi/ApiDeveloper/CampusKartApiDeveloper/Compass/quick2wire-python-api')
from i2clibraries import i2c_hmc5883l
from i2clibraries import i2c_adxl345

adxl345 = i2c_adxl345.i2c_adxl345(1)
 
while True:
        print(adxl345)
        time.sleep(0.1)        
