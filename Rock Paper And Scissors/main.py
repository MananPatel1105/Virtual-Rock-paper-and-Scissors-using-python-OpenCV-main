import cv2 as cv
import HandTrackingModule as htm
import time
import random
import cvzone as cvz

######################################################################################
#Capturing Video

video = cv.VideoCapture(0)
video.set(3,640)
video.set(4,480)

######################################################################################
#detecting Hands Using An HandTrackingModule

detector = htm.HandDetector()

######################################################################################

#Assigning Variables for Game and Scores

timer = 0
StateResult = False
StartGame = False
Scores = [0,0]

######################################################################################
#Loop Starts

while True:
    success, frame = video.read()

    #Fliping Image and Inserting an background image with cropping the video onto the Image

    image = cv.flip(frame,1)
    imageBG = cv.imread("C:/Users/DELL/Desktop/PPSU/Projects/Virtual-Rock-paper-and-Scissors-using-python-OpenCV-main/Rock Paper And Scissors/Images_Project/BG.png")
    imageScaled = cv.resize(image, (0,0), None, 0.875,0.875)
    imageScaled = imageScaled[:,80:480]

    #This Pixels of BackgroundImage will have the Video Part

    imageBG[234:654,795:1195] = imageScaled

    #Getting the HandLandMarks and List of there Positions

    imageBG = detector.FindHands(imageBG)
    lmlist = detector.FindPosition(imageBG, draw=False)

    #Starting Game

    if StartGame == True:
        if StateResult == False:
            timer = time.time() - intialTime    #Counting Timer
            cv.putText(imageBG, str(int(timer)),(605,435),cv.FONT_HERSHEY_PLAIN,6,(10,255,247),4)

        #If time Exceds 3 Seconds and Displaying the result and Stopping the Timer

        if timer>3:
            StateResult = True
            timer = 0

            #Checking for How many Fingers are Up for counting as Rock Paper and Scissors

            if (len(lmlist) != 0):
                    fingers = detector.fingersup()
                    if fingers == [0,0,0,0,0] or fingers == [1,0,0,0,0]:
                        PlayerMove = 1                      #For Rock
                    elif fingers == [1,1,1,1,1]:
                        PlayerMove = 2                      #For Paper
                    elif fingers == [0,1,1,0,0]:
                        PlayerMove = 3                      #For Scissors
                    
                    RandomNumber = random.randint(1,3)      #Generating an Random Number for AI to Decide
                    imgAI = cv.imread(f'C:/Users/DELL/Desktop/PPSU/Projects/Virtual-Rock-paper-and-Scissors-using-python-OpenCV-main/Rock Paper And Scissors/{RandomNumber}.png',cv.IMREAD_UNCHANGED)     #Displaying that number picture 
                    imageBG = cvz.overlayPNG(imageBG,imgAI, (149, 310))        #Overlapping the background and number image

                    #Player Wins
                    if (PlayerMove == 1 and RandomNumber == 3) or \
                        (PlayerMove == 2 and RandomNumber == 1) or \
                        (PlayerMove == 3 and RandomNumber == 2):
                        Scores[1] +=1
                    
                    #AI Wins
                    if (PlayerMove == 1 and RandomNumber == 2) or \
                        (PlayerMove == 2 and RandomNumber == 3) or \
                        (PlayerMove == 3 and RandomNumber == 1):
                        Scores[0] +=1

                    print(fingers)
    

    #Same For Displaying the Image for Long Time (AI Image)
    if StateResult == True:
        imageBG = cvz.overlayPNG(imageBG,imgAI, (149, 310))

    #Putting the Scores After Every Round

    cv.putText(imageBG, str(Scores[0]),(410,215),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    cv.putText(imageBG, str(Scores[1]),(1112,215),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),6)

    #Starting the Round If User Presses 's' Key

    if (cv.waitKey(1) == ord('s')):
        StateResult = False
        StartGame = True
        intialTime = time.time() 

    cv.imshow("BACKGROUND",imageBG)

######################################################################################s