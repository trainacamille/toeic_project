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
    print (compteurx)
    print (compteury)
    print (valeurx)
    print (valeury)
    print (posminx)
    print (posminy)

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


'''
*       *
*
*       *
'''
pts = [[0,0], [0,100], [100,0], [100,100], [0,50]]
print (rotationimage(pts, 5))