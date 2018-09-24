# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 11:34:49 2016

@author: Radovan
"""
import math
import numpy


def GPSDistance(lat1_deg,long1_deg,lat2_deg,long2_deg):
# given latitude and longidude of two points return distance between them.
    R=6.371*math.pow(10,6)          #earth radius
    lat1_=lat1_deg*math.pi/180      #convert degrees into radians
    lat2_=lat2_deg*math.pi/180
    long1_=long1_deg*math.pi/180
    long2_=long2_deg*math.pi/180
    distance=R*math.sqrt(2-2*math.cos(lat1_)*math.cos(lat2_)*math.cos(long1_-long2_)-2*math.sin(lat1_)*math.sin(lat2_))
    return distance

# converts GPS coordinates into cartesian coordinate system 
# such that X-Y plane is tangent to P1 and Y points to the NORTH and
# X points to the EAST and assuming P1 is at the origin (x1,y1)=(0,0)
# North
#   ^
#   |
#   Y
#   |
#  0,0---X--->East
# inputs lat1, long1, lat2, long2
# output x y b-heading
    
def XfromGPS(lat1_deg,long1_deg,lat2_deg,long2_deg):
    R=6.371*math.pow(10,6)          #earth radius
    lat1_ =lat1_deg*math.pi/180     #convert degrees into radians
    lat2_ =lat2_deg*math.pi/180
    long1_ =long1_deg*math.pi/180
    long2_ =long2_deg*math.pi/180
    x = numpy.array(R*(long2_-long1_)*numpy.cos(lat1_))
    return x

def YfromGPS(lat1_deg,long1_deg,lat2_deg,long2_deg):
    R=6.371*math.pow(10,6)           #earth radius
    lat1_ =lat1_deg*math.pi/180      #convert degrees into radians
    lat2_ =lat2_deg*math.pi/180
    long1_ =long1_deg*math.pi/180
    long2_ =long2_deg*math.pi/180
    y = numpy.array(R*(lat2_-lat1_))
    return y

def BfromGPS(lat1_deg,long1_deg,lat2_deg,long2_deg):
    R=6.371*math.pow(10,6)           #earth radius
    lat1_ =lat1_deg*math.pi/180      #convert degrees into radians
    lat2_ =lat2_deg*math.pi/180
    long1_ =long1_deg*math.pi/180
    long2_ =long2_deg*math.pi/180
    y = numpy.array(R*(lat2_-lat1_))
    x = numpy.array(R*(long2_-long1_)*numpy.cos(lat1_))
    b = numpy.array(numpy.arctan2(x,y)*180/math.pi)
    return b

def BfromXY(x,y):
    b = numpy.array(numpy.arctan2(x,y)*180/math.pi)
    return b    