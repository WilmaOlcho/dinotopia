import numpy as np
import cv2
import pyautogui
from time import sleep
   
  
image = pyautogui.screenshot()
   
image = cv2.cvtColor(np.array(image),
                     cv2.COLOR_RGB2BGR)

dino = cv2.imread("dino.png")

result = cv2.matchTemplate(image, dino, cv2.TM_CCOEFF_NORMED)


while True:
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(image, dino, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.8)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + 50, pt[1] + 50), (0, 0, 255), 2)
        dinopos = pt[0]
    
    cv2.imshow("test", image)
    if cv2.waitKey(1) == ord("q"):
        break
    sleep(0.1)