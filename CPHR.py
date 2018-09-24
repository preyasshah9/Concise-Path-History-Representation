from datetime import datetime
from datetime import timedelta
from gps_pkg.gps import *
import csv
import sys
import os
import math

#Calibration Parameters
REarthMeridian = 6378000
K_PHDISTANCE_M = 300.0
K_PH_CHORDLENGTHTHRESHOLD = 310.0
K_PHALLOWABLEERROR_M = 1
K_PHSMALLDELTAPHI_R = 0.02
K_PH_MAXESTIMATEDRADIUS = hex(0x7FFFFF)
TIME_START = "2013-01-14T21:05:01Z" # To Enable the slider in google earth, This is the reference point when measurements started
TIME_INIT = datetime.strptime(TIME_START,"%Y-%m-%dT%H:%M:%SZ")

timeStamp = []
latitude = []
longitude = []
count = 0

def calculatePH(count):
    PHPoints = []
    totalDist = 0.0
    incrementDist = 0.0
    # First Point is also the starting point
    Pstart = 0
    # Initialize the Pprev and Pnext Points
    Pprev = 1
    Pnext = 2
    # Add the first point in the PH Concise Representation
    PHPoints.append(Pstart)
    for i in range(2,count-1):
        # Some Variables to calculate the PH_ActualCordLength
        long1Radians = longitude[Pstart] * math.pi / 180
        long2Radians = longitude[Pnext] * math.pi / 180
        lat1Radians  = latitude[Pstart] * math.pi / 180
        lat2Radians  = latitude[Pnext] * math.pi / 180
        PH_ActualError = 0.0
        PH_ActualCordLength = REarthMeridian * math.acos(
                                               math.cos(lat1Radians) * 
                                               math.cos(lat2Radians) *
                                               math.cos(long1Radians - long2Radians) +
                                               math.sin(lat1Radians) *
                                               math.sin(lat2Radians))
        # If Actual Cord Length is greater than certain threshold, then Set
        # Error greater than threshold, this point will be added to the Concise PH
        # Buffer
        if(PH_ActualCordLength > K_PH_CHORDLENGTHTHRESHOLD):
            PH_ActualError = K_PHALLOWABLEERROR_M + 1
        else:
            # Now get the headings of the Starting and Next Points
            H1 = BfromGPS(latitude[Pnext], longitude[Pnext], latitude[Pnext + 1], longitude[Pnext + 1])
            H2 = BfromGPS(latitude[Pstart], longitude[Pstart], latitude[Pstart + 1], longitude[Pstart + 1])
            
            #Calculation of the approximated angle between the headings
            deltaPhi    = abs((H2 - H1) * math.pi / 180)
            
            #If Angle between the headings is really small, set EstimatedR to the 
            #arbitrary large values and actualError to be 0.
            if(deltaPhi < K_PHSMALLDELTAPHI_R):
                PH_ActualError = 0
                PH_EstimatedR = K_PH_MAXESTIMATEDRADIUS
            else:
                #EstimatedR is still greater than threshold, Calculate the 
                #PH_ActualError and EstimatedR
                PH_EstimatedR = PH_ActualCordLength /  ( 2 * math.sin(deltaPhi/2))
                d = PH_EstimatedR * math.cos(deltaPhi/2)
                PH_ActualError = PH_EstimatedR - d
        
        if(PH_ActualError > K_PHALLOWABLEERROR_M):
            PHPoints.append(Pprev)
            Pstart = i - 1
            if(i < count - 1):
                Pnext  = i + 1
            Pprev = i
            incrementDist = GPSDistance(latitude[PHPoints[-1]], longitude[PHPoints[-1]], latitude[PHPoints[-2]], longitude[PHPoints[-2]])
            totalDist = totalDist + incrementDist
            # We don't want to include the points that are > 300 m away based on the path history representation
            while(totalDist > K_PHDISTANCE_M):
                totalDist = totalDist - GPSDistance(latitude[PHPoints[0]], longitude[PHPoints[0]], latitude[PHPoints[1]], longitude[PHPoints[1]])
                PHPoints.pop(0)
                Pstart = PHPoints[0]
        else:
            if(i < count - 1):
                Pnext  = i + 1
            Pprev = i
    # PHPoints.append(count - 1) # Add the last point to the list
    # incrementDist = GPSDistance(latitude[PHPoints[-1]], longitude[PHPoints[-1]], latitude[PHPoints[-2]], longitude[PHPoints[-2]])
    # totalDist = totalDist + incrementDist
    # while(totalDist > K_PHDISTANCE_M):
        # totalDist = totalDist - GPSDistance(latitude[PHPoints[0]], longitude[PHPoints[0]], latitude[PHPoints[1]], longitude[PHPoints[1]])
        # PHPoints.pop(0)
    return PHPoints    
inputFileName = sys.argv[1]
main_name,extention=inputFileName.split('.')
#print 'main_name:',main_name
#print 'extention:',extention
out_kml_name=main_name+'.kml'
with open(inputFileName, "r") as csvFile:
    csvHandler = csv.reader(csvFile)
    for row in csvHandler:
        # Time is in floating point notation,
        # Append the longitude and latitude to the list
        timeStamp.append(float(row[0]))
        longitude.append(float(row[2]))
        latitude.append(float(row[1]))
        count = count + 1
with  open(out_kml_name, 'w') as kml_file:
    kml_file.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
<!-- 

TimeStamp is recommended for Point.

Each Point represents a sample from a GPS.

-->

  <Document>
    <name>Points with TimeStamps</name>
        <Style id="s_ylw-pushpin_hl">
        <IconStyle>
            <scale>1.3</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <LabelStyle>
            <color>ffff0000</color>
        </LabelStyle>
    </Style>
    <Style id="s_ylw-pushpin">
        <IconStyle>
            <scale>1.1</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <LabelStyle>
            <color>ffff0000</color>
        </LabelStyle>
    </Style>
    <StyleMap id="m_ylw-pushpin">
        <Pair>
            <key>normal</key>
            <styleUrl>#s_ylw-pushpin</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#s_ylw-pushpin_hl</styleUrl>
        </Pair>
    </StyleMap>
    <Style id="sn_cabs2">
        <IconStyle>
            <color>ffff0000</color>
            <scale>0.7</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
        </IconStyle>
        <ListStyle>
        </ListStyle>
    </Style>
    <Style id="sh_cabs2">
        <IconStyle>
            <color>ffff0000</color>
            <scale>0.816667</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
        </IconStyle>
        <ListStyle>
        </ListStyle>
    </Style>
    <StyleMap id="msn_cabs2">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_cabs2</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sh_cabs2</styleUrl>
        </Pair>
    </StyleMap>

    <StyleMap id="msn_cabs1">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_cabs1</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sh_cabs1</styleUrl>
        </Pair>
    </StyleMap>
    <Style id="sh_cabs1">
        <IconStyle>
            <color>ff00ff00</color>
            <scale>0.7</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
        </IconStyle>
        <ListStyle>
        </ListStyle>
    </Style>
    <Style id="sn_cabs1">
        <IconStyle>
            <color>ff00ff00</color>
            <scale>0.7</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
            </Icon>
            <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
        </IconStyle>
        <ListStyle>
        </ListStyle>
    </Style>''')
    kml_file.write('\n')
    for i in range(0, count):
        timeDelta = timedelta(seconds = timeStamp[i])
        time_fin = timeDelta + TIME_INIT
        PHPoints = []
        PHPoints = calculatePH(i)
        for j in range(0, len(PHPoints)):
            kml_file.write('\t<Placemark><TimeStamp><when>'+time_fin.strftime("%Y-%m-%dT%H:%M:%SZ")+'</when></TimeStamp><styleUrl>#msn_cabs1</styleUrl><Point><coordinates>'+str(longitude[PHPoints[j]])+','+str(latitude[PHPoints[j]])+',0</coordinates></Point></Placemark>\n')
        #kml_file.write('\t<Placemark><TimeStamp><when>'+time_fin.strftime("%Y-%m-%dT%H:%M:%SZ")+'</when></TimeStamp><styleUrl>#msn_cabs1</styleUrl><Point><coordinates>'+str(longitude[i])+','+str(latitude[i])+',0</coordinates></Point></Placemark>\n')
    kml_file.write('\n')
    kml_file.write('''\t</Document>                                                                                                           
</kml>''')