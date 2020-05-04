import math
from .point import Point

class Router:
    """ docstring for Router"""
    
    def __init__(self, ssid, position, freq=2.4):
        self.SSID = ssid 
        self.coordinate = position
        self.frequency = freq

    def distance_from_signal(self, signal):
        result=(27.55-(20*math.log10(self.frequency)+signal))/20
        return (10**result)/(1000)        



DISTANCE_APART = 200
R1 = Router('Beesafe', Point(200, 200))
R2 = Router('Guest_Router', Point(R1.coordinate.xcord+DISTANCE_APART,R1.coordinate.ycord))


DEFAULT_ACCESS_POINTS = {
    f'{R1.SSID}': R1,
    f'{R2.SSID}': R2
} 
