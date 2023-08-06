from libcpp cimport bool

from s2 cimport S2Point
from s1angle cimport S1Angle
from s2region cimport S2Region


cdef extern from "geometry/s2/s2cap.h":
    cdef cppclass S2Cap(S2Region):
        @staticmethod
        S2Cap FromAxisHeight(S2Point axis, double height)
        @staticmethod
        S2Cap FromAxisAngle(S2Point axis, S1Angle angle)
        @staticmethod
        S2Cap FromAxisArea(S2Point axis, double area)
        S2Point axis()
        double height()
        double area()
        S1Angle angle()
        bool is_valid()
        bool is_empty()
        bool is_full()
        S2Cap Complement()
        bool Contains(S2Cap other)
        bool Intersects(S2Cap other)
        bool InteriorIntersects(S2Cap other)
        bool InteriorContains(S2Cap other)
        void AddPoint(S2Point p)
        void AddCap(S2Cap other)
        S2Cap Expanded(S1Angle distance)
