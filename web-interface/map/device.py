import math
from .point import Point
from .router import DEFAULT_ACCESS_POINTS, R1, R2

class Device(object):
    """docstring for Device"""
    
    def __init__(self, unique_id):
        self.id = unique_id
        self.coordinate = Point(0, 0)
        self.signal_strengths = {}

    # lifted from wikipedia
    # link - https://en.wikipedia.org/wiki/True_range_multilateration
    def compute_coordinate(self):
        # considering 2D plane
        distances = {}
        for key, value in self.signal_strengths.items():

            if DEFAULT_ACCESS_POINTS.get(key, None) is not None:
                access_point = DEFAULT_ACCESS_POINTS[key]
                distances[key] = access_point.distance_from_signal(value)

        distance_apart = R2.coordinate.xcord - R1.coordinate.xcord
        xcord = (distances[R1.SSID]**2 - distances[R2.SSID]**2 + distance_apart**2)/(2*distance_apart)
        ycord=math.sqrt(distance_apart**2 + xcord**2)
        self.coordinate.xcord = xcord + distances[R1.SSID] 
        self.coordinate.ycord = ycord + distances[R1.SSID]