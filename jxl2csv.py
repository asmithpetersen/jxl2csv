#!/usr/bin/env python

# Convert JXL XML to CSV

# Copyright (C): 2015 by Vaclav Petras
# License: GNU GPL >2


import sys
import xml.etree.ElementTree as ElementTree

if len(sys.argv) not in (2, 3):
    sys.exit(
        "Usage:\n"
        "    {prg} file.jxl\n"
        "    {prg} file.jxl file.csv\n"
        "    python {prg} file.jxl [file.csv]".format(prg=sys.argv[0]))

e = ElementTree.parse(sys.argv[1]).getroot()

if len(sys.argv) == 3:
    output = open(sys.argv[2], 'w')
else:
    output = sys.stdout

output.write("name,latitude,longitude,height,yaw,pitch,roll\n")

for atype in e.findall('*/PointRecord'):
    name = atype.find('Name').text
    wgs84 = atype.find('WGS84')
    lat = wgs84.find('Latitude').text
    lon = wgs84.find('Longitude').text
    height = wgs84.find('Height').text
    bi_vector = e.find(
        '*/PhotoStationRecord[StationName="%s"]'
        '/DeviceAxisOrientationData/DeviceAxisOrientation'
        '/BiVector' % name)
    xx = bi_vector.find('XX').text
    yy = bi_vector.find('YY').text
    zz = bi_vector.find('ZZ').text

    name = name + '.JPG'

    output.write("{},{},{},{},{},{},{}\n".format(
        name, lat, lon, height, xx, yy, zz))
