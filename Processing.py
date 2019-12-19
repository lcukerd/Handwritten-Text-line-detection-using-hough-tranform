from sympy import Point, Polygon
import numpy as np
import math
import cv2 as cv

from GeometryProcessing import *

def divide(centroids, stats, ah):
    centroids1 = [];
    centroids2 = [];
    centroids3 = [];

    stats1 = [];
    stats2 = [];
    stats3 = [];

    for i in range(len(centroids)):
        centroid = centroids[i];
        stat = stats[i];
        h = stat[cv.CC_STAT_HEIGHT];
        w = stat[cv.CC_STAT_WIDTH]

        if (h < 3 * ah and h >= 0.5 * ah and 0.5 * ah <= w):
            centroids1.append(centroid);
            stats1.append(stat);
        elif (h >= 3 * ah):
            centroids2.append(centroid);
            stats2.append(stat);
        elif ((h < 3 * ah and 0.5 * ah > w) or (h < 0.5 * ah and 0.5 * ah < w)):
            centroids3.append(centroid);
            stats3.append(stat);

    print ('Found ' + str(len(centroids1)) + " in subset 1, " + str(len(centroids2)) + " in subset 2, and " + str(len(centroids3)) + " in subset 3");

    return ((centroids1, stats1), (centroids2, stats2), (centroids3, stats3));

def partitionCC(stats, aw):
    centroids = [];
    mapP = [];
    for pos in range(len(stats)):
        stat = stats[pos];
        l = stat[cv.CC_STAT_LEFT];
        t = stat[cv.CC_STAT_TOP];
        h = stat[cv.CC_STAT_HEIGHT];
        for i in range(1, int(math.ceil (stat[cv.CC_STAT_WIDTH] / aw)) + 1):
            end = i*aw if i*aw < stat[cv.CC_STAT_WIDTH] else stat[cv.CC_STAT_WIDTH];
            polyCen = Polygon ((l, t), (l + end, t), (l + end, t + h), (l, t + h)).centroid;
            centroids.append((polyCen.x, polyCen.y));
            mapP.append(pos);
    return centroids, mapP;

def findPrimaryCell(lines, centroids):
    n = 0
    lineP = (0,0);
    pos = 0;
    for i in range(len(lines)):
        print ("Checking for line " + str(i + 1) + " of " + str(len(lines)), end = '\r');
        line = lines[i][0]
        ntemp = findValueofcell(line, centroids, i)
        if (ntemp > n):
            lineP = line
            n = ntemp
            pos = i;
    return lineP, pos, n
