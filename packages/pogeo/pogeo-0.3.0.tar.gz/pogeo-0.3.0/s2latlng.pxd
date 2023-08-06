from libcpp cimport bool

from s2 cimport S2Point
from s1angle cimport S1Angle


cdef extern from "geometry/s2/s2latlng.h":
    cdef cppclass S2LatLng:
        @staticmethod
        S2LatLng FromRadians(double lat_radians, double lng_radians)
        @staticmethod
        S2LatLng FromDegrees(double lat_degrees, double lng_degrees)
        @staticmethod
        S1Angle Latitude(S2Point p)
        @staticmethod
        S1Angle Longitude(S2Point p)
        S1Angle lat()
        S1Angle lng()
        bool is_valid()
        S2LatLng Normalized()
        S2Point ToPoint()
        S1Angle GetDistance(S2LatLng o)
