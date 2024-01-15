import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3
cap=cv2.VideoCapture(0)
cap.set(3,1280) #image width
cap.set(4,1080) #image height
detector=HandDetector(detectionCon=0.8,maxHands=1)
Equation=''
Counter=0
class Button:
    def __init__(self,pos,width,height,value):
        self.pos=pos      #constructor parameter convert into class member
        self.width=width
        self.height=height
        self.value=value
    def draw(self,img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (125, 125, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70),
                    cv2.FONT_HERSHEY_PLAIN,2, (50, 50, 50), 2)

    def Click(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80),
                        cv2.FONT_HERSHEY_PLAIN,5, (0, 0, 0), 5)
            return True
        else:
            return False
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("please wait! the virtual calculator is starting")
engine.runAndWait()

buttons = [['7', '8', '9', 'C'],
           ['4', '5', '6', '*'],
           ['1', '2', '3', '+'],
           ['0', '-', '/', '='],
           ['(', ')', '.', 'del']]
buttonList = []
for x in range(4):
    for y in range(5):
        xpos = x * 100 + 700
        ypos = y * 100 + 100
        buttonList.append(Button((xpos, ypos), 100, 100, buttons[y][x]))
#button=Button((700,100),100,100,'5') #button object

while True:
    #get image from webcam
    # read operation return two values 1.Image capture(True) or not(False) 2.Image
    sucess,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    for i in buttonList:
        i.draw(img)
    # Check for Hand
    if hands:
        # Find distance between fingers
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
        print(length)
        x, y = lmList[8][0:2]
        # If clicked check which button and perform action
        if length<=50 and Counter==0:
            for i, button in enumerate(buttonList):
                if button.Click(x, y):
                    myvalue = buttons[int(i % 5)][int(i / 5)] #get a number
                    engine.say(myvalue)
                    engine.runAndWait()
                    if myvalue == '=':
                        try:
                            Equation = str(eval(Equation))
                            engine.say(Equation)
                            engine.runAndWait()
                        except SyntaxError:
                            print("Syntax Error")
                            engine.say("Syntax Error")
                            engine.runAndWait()
                            Equation='Syntax Error'
                    elif myvalue == 'C':
                        Equation = ''
                    elif myvalue=='del':
                        Equation = Equation[:-1]
                    else:
                        Equation += myvalue #Equation=Equation+myvalue

                    Counter=1
    # to avoid multiple clicks
    if Counter != 0:
        Counter += 1
        if Counter > 10:
            Counter = 0

    # Final answer
    cv2.rectangle(img, (700, 20), (1100, 100),(175, 125, 155), cv2.FILLED)
    cv2.rectangle(img, (700, 20), (1100, 100), (50, 50, 50), 3)
    cv2.putText(img, Equation, (710, 80), cv2.FONT_HERSHEY_PLAIN,3, (0, 0, 0), 3)

    cv2.imshow('Image',img)
    key = cv2.waitKey(1)
    if key != ord('q'):
        continue
    break
