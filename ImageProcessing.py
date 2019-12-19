import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt


def findComponents(image):
    edgyImg = cv.Canny(image, 50, 200, None, 3)
    edgyColor = cv.cvtColor(edgyImg, cv.COLOR_GRAY2BGR)
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(edgyImg);

    avg_height = 0;
    for stat in stats:
        avg_height += stat[cv.CC_STAT_HEIGHT]
    avg_height /= num_labels
    print ("Found " + str(num_labels) + " components with height " + str(avg_height) + " in image")

    return (labels, avg_height, centroids, stats)


def findHoughLines(centroidImg, outputImg, height, Threshold, n, m):
    dst = cv.Canny(centroidImg, 50, 200, None, 3)
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)

    lines = cv.HoughLines(dst, int(0.2  * height), np.pi / 180, Threshold, None, n, m)

    nlines = [];

    if lines is not None:
        print ("Calculated " + str(len(lines)) + " lines")
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            if math.degrees(theta) < 95 and math.degrees(theta) > 85:
                nlines.append(lines);
            else:
                continue;
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            if (outputImg is None):
                cv.line(centroidImg, pt1, pt2, (255,255,255), 3, cv.LINE_AA)
            else:
                cv.line(outputImg, pt1, pt2, (255,255,255), 3, cv.LINE_AA)

    if (outputImg is None):
        plt.imshow(centroidImg)
    else:
        plt.imshow(outputImg)
    plt.show()
    return lines;


def houghDomainValidation(lines, centroids, avg_height):
    (rho_, theta_) = findPrimaryCell(lines, centroids)

    f_clus = findClustersize(theta_, avg_height)
    print (f_clus)

    x0 = rho_ - f_clus
    x1 = rho_ + f_clus
    z0 = theta_ - math.radians(3)
    z1 = theta_ + math.radians(3)

    clusCells = findcells(x0, x1, z0, z1, lines)
    print (len(clusCells))
    showLines(clusCells, DemoImg)
    n0 = findValueofcell([(rho_, theta_)], centroids)
    print (n0)

    ntemp = 0
    rho1, theta1 = 0,0
    for i in clusCells:
        if (i[0][0] == rho_ and i[0][1] == theta_):
            continue
        temp = findValueofcell(i, centroids)
        if (temp > ntemp):
            ntemp = temp
            rho1 = i[0][0]
            theta1 = i[0][1]
    # showLines([[(rho_, theta_)]], DemoImg)
    return compareValueinStruct([(rho_, theta_)], [(rho1, theta1)], centroids, x0, x1, z0, z1, n0, ntemp)