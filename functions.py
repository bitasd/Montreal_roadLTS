from dataclasses import dataclass, field
import math
import numpy as np
from shapely.geometry import Point, LineString, MultiLineString


# @dataclass
# class _Node:
#     _id: str
#     lon: float
#     lat: float
#     incident_segments: List = field(default_factory=list)
#     cc_ordered_incident_segments: List = field(default_factory=list)
#
#
# @dataclass
# class _Segment:
#     _id: int
#     _nodes: List[_Node]
#     _attributes: Dict

class DigitalDirection:

    def calc_bearing(self, geom):

        v1 = geom[0].coords[0]
        v2 = geom[0].coords[-1]
        dLon = v2[0] - v1[0]
        dLat = v2[1] - v1[1]
        rad = math.atan2(dLon, dLat)
        deg = np.rad2deg(rad)
        return deg

    # check if protected lane is in the digitized direction
    def localisati_true(self, bear_deg, localisati):

        if -180 < bear_deg < -90:
            if localisati == 'NORD':
                digital_dir = 1
            elif localisati == 'SUD':
                digital_dir = -1
            else:
                digital_dir = -7777

        elif -90 <= bear_deg < 0:
            if localisati == 'EST':
                digital_dir = 1
            elif localisati == 'OUEST':
                digital_dir = -1
            else:
                digital_dir = -7777

        elif 0 <= bear_deg < 90:
            if localisati == 'SUD':
                digital_dir = 1
            elif localisati == 'NORD':
                digital_dir = -1

        elif 90 <= bear_deg <= 180:
            if localisati == 'OUEST':
                digital_dir = 1
            elif localisati == 'EST':
                digital_dir = -1

        print(bear_deg, localisati)
        return digital_dir
