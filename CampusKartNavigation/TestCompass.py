from gps3 import gps3

gps_connection = gps3.GPSDSocket(host='127.0.0.1')
gps_fix = gps3.Fix()
for new_data in gps_connection:
    if new_data:
        gps_fix.refresh(new_data)
        print('Altitude = ',gps_fix.TPV['alt'])
        print('Latitude = ',gps_fix.TPV['lat'])
