import numpy as np
import cv2
import keyboard
from PIL import ImageGrab
from time import sleep

dinoposx = 0
dinoposy = 0
dino = cv2.imread("dino.png")
dino2 = cv2.imread("dino2.png")
while True:
    image = ImageGrab.grab(bbox = None)
    image = np.array(image)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(image, dino, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.6)
    for pt in zip(*loc[::-1]):
        dinoposx = pt[0]
        dinoposy = pt[1]
    if dinoposx != 0:
        break
isjumping = False
gamescreen = (dinoposx, dinoposy-140, dinoposx+600, dinoposy+50)
obstacles = np.array([])
obstacleposx = 0
obstaclewidth = 0
obstacleposy = 0
obstacleheight = 0
dinodown = False
while True:
    obstacleposx = 0
    obstaclewidth = 0
    obstacleposy = 0
    obstacleheight = 0
    image = ImageGrab.grab(bbox = gamescreen)
    image = np.array(image)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    if dinodown:
        result = cv2.matchTemplate(image, dino2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.6)
        for pt in zip(*loc[::-1]):
            dinoposx  = pt[0]
            dinoposy = pt[1]
        obstacleposy = dinoposy-20
        obstacleposx = dinoposx+80
        obstaclewidth = 60
        obstacleheight = 40
    else:
        result = cv2.matchTemplate(image, dino, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.6)
        for pt in zip(*loc[::-1]):
            dinoposx = pt[0]
            dinoposy  = pt[1]
        obstacleposy = dinoposy
        obstacleposx = dinoposx+60
        obstaclewidth = 60
        obstacleheight = 40
    obstacles = image[obstacleposx:obstacleposx+obstaclewidth, obstacleposy:obstacleposy+obstacleheight]
    if obstacles.size != 0:
        obstacles = cv2.cvtColor(obstacles, cv2.COLOR_BGR2GRAY)
        obstacles = cv2.threshold(obstacles, 200, 255, cv2.THRESH_BINARY)[1]
        if np.any(obstacles==0):
            keyboard.release("down")
            keyboard.press_and_release("space")
            dinodown = False
            sleep(0.2)
            keyboard.press("down")
            sleep(0.1)
        else:
            keyboard.press("down")
            dinodown = True
        
        cv2.rectangle(image, (obstacleposx, obstacleposy), (obstacleposx+obstaclewidth, obstacleposy+obstacleheight), (0, 255, 0), 1)
        obstacles = cv2.cvtColor(obstacles, cv2.COLOR_RGB2BGR)
        image[obstacleheight:obstacleheight+obstaclewidth, obstacleposy:obstacleposy+obstacleheight] = obstacles
        cv2.imshow("obstacles", image) 
        cv2.waitKey(1)
 