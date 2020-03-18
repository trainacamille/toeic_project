import numpy as np
import cv2

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

def grab_contours(cnts):
    # if the length the contours tuple returned by cv2.findContours
    # is '2' then we are using either OpenCV v2.4, v4-beta, or
    # v4-official
    if len(cnts) == 2:
        cnts = cnts[0]

    # if the length of the contours tuple is '3' then we are using
    # either OpenCV v3, v4-pre, or v4-alpha
    elif len(cnts) == 3:
        cnts = cnts[1]

    # otherwise OpenCV has changed their cv2.findContours return
    # signature yet again and I have no idea WTH is going on
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
            "otherwise OpenCV changed their cv2.findContours return "
            "signature yet again. Refer to OpenCV's documentation "
            "in that case"))

    # return the actual contours array
    return cnts


def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)


def rotationimage(pts, ecart):
    compteurx = [0,0,0]
    compteury = [0,0,0]
    valeurx = [-1,-1,-1]
    valeury = [-1,-1,-1]
    posminx = -1
    posminy = -1

    for i in range(0,5):
        if posminx == -1:
            posminx = pts[i][0]
        if valeurx[0] == -1:
            valeurx[0] = pts[i][0]
        if pts[i][0] < valeurx[0]+ecart and pts[i][0] > valeurx[0]-ecart:
            compteurx[0] += 1
            if posminx > pts[i][0]:
                posminx = 0
        else:
            if valeurx[1] == -1:
                valeurx[1] = pts[i][0]
            if pts[i][0] < valeurx[1]+ecart and pts[i][0] > valeurx[1]-ecart:
                compteurx[1] += 1
                if posminx > pts[i][0]:
                    posminx = 1
            else:
                if valeurx[2] == -1:
                    valeurx[2] = pts[i][0]
                compteurx[2] += 1
                if posminx > pts[i][0]:
                    posminx = 2
    
    for i in range(0,5):
        if posminy == -1:
            posminy = pts[i][1]
        if valeury[0] == -1:
            valeury[0] = pts[i][1]
        if pts[i][1] < valeury[0] + ecart and pts[i][1] > valeury[0]-ecart:
            compteury[0] += 1
            if posminy > pts[i][1]:
                posminy = 0
        else:
            if valeury[1] == -1:
                valeury[1] = pts[i][1]
            if pts[i][1] < valeury[1]+ecart and pts[i][1] > valeury[1]-ecart:
                compteury[1] += 1
                if posminy > pts[i][1]:
                    posminy = 1
            else:
                if valeury[2] == -1:
                    valeury[2] = pts[i][1]
                compteury[2] += 1
                if posminy > pts[i][1]:
                    posminy = 2

    print (pts)

    if compteurx[2]==0:
        if compteurx[posminx]==3:
            return 90
        else:
            return -90
    else:
        if compteury[posminy]==3:
            return 180
        else:
            return 0

