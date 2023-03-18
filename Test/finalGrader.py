
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2
import csv
import os

def export(file_name, options, startValue, numQuestions, outputFileName):
    field_names = ['id', 'last name', 'first name'] 
    for i in range(numQuestions):
        field_names.append(str(startValue+i) + "Q")
        field_names.append(str(startValue+i) + "S")
        field_names.append(str(startValue+i) + "T")
    queues = options 
    img = file_name
    answers:dict = {}

    image = cv2.imread(img)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)


    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None

    if len(cnts) > 0:

        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        for c in cnts:

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                docCnt = approx
                break
    if docCnt is not None:  
        warped = four_point_transform(gray, docCnt.reshape(4, 2))
    else:
        warped = gray

    thresh = cv2.threshold(warped, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    #cv2.imshow('bw', thresh)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []

    for c in cnts:

        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        if w >= 25 and h >= 25 and ar >= 0.9 and ar <= 1.1:
            questionCnts.append(c)

    questionCnts = contours.sort_contours(questionCnts,
        method="top-to-bottom")[0]
    
    if(len(questionCnts)>options*(numQuestions+1)):
        print(len(questionCnts))
        questionCnts=questionCnts[len(questionCnts)-options*(numQuestions+1):len(questionCnts)]

    first = True
    for (q, i) in enumerate(np.arange(0, len(questionCnts), queues)):

        cnts = contours.sort_contours(questionCnts[i:i + queues])[0]
        bubbled = None 
        
        mask2 = np.zeros(thresh.shape, dtype="uint8")
        holder = []
        for (j, c) in enumerate(cnts):

            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            mask2 = cv2.bitwise_or(mask2, mask)
            total = cv2.countNonZero(mask)

            holder.append((total, j))
        if first: holder = sorted(holder, key=lambda x: x[0],reverse=True)[0:2]
        else: holder = sorted(holder, key=lambda x:x[0], reverse = True)[0:4]
        holder = sorted(holder, key=lambda x:x[1])
        
        
        if not first:
            value = holder[0][1] #which question this is 1-3
            choice = holder[1][1]-2 #which choice they made 1 or 2
            studentAnswer = 15 - holder[2][1] #predicted score
            teacherAnswer = 26 - holder[3][1] #actual score
            answers[str(value+startValue)+'Q'] = choice
            answers[str(value+startValue)+'S'] = studentAnswer
            answers[str(value+startValue)+'T'] = teacherAnswer
        
        
        
        
        
        if first:
            first = False
            period = holder[0][1]
            id = holder[1][1]-2
            answers:dict = {"id": id}
            d = {}
            periodSwapper = {0: 5, 1: 7}
            with open("Test/classDirectory" + str(periodSwapper[period]) + ".in") as f:
                for line in f:
                    (key, val) = line.split(maxsplit=1)
                    d[int(key)] = val
            names = d[id].split(',')
            if(len(names)>1):
                lname = names[0]
                fname = names[1]
            else:
                lname = names[0]
                fname = "null"
            answers['first name'] = fname.strip()
            answers['last name'] = lname.strip()


            second = True


    with open(outputFileName, 'a', newline='') as out:
        normWriter = csv.writer(out)
        if os.stat(outputFileName).st_size == 0:
            normWriter.writerow(field_names)

    with open(outputFileName, 'a', newline="") as out:
        writer = csv.DictWriter(out, fieldnames=field_names) 
        writer.writerow(answers)
    print(answers)
