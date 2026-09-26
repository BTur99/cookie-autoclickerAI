import pyautogui
import cv2
import numpy as np
from ultralytics import YOLO
import time

CONFIDENCE_THRESHOLD = 0.6
LOOP_DELAY = 0.5
CLICKS_PER_DETECTION = 1

model = YOLO("weights/best.pt")
print("Модель подгружена, жду пять секунд")
time.sleep(5)

def click():
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    result = model(frame, verbose=False)
    
    found = False
    for r in result:
        for box in r.boxes:
            conf = float(box.conf[0])
            if conf < CONFIDENCE_THRESHOLD:
                continue
            
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
            
            for i in range(CLICKS_PER_DETECTION):
                pyautogui.click(cx, cy)
            
            print(f"\Клик по коордам: ({cx}, {cy}), уверенность: {round(conf, 2)}")
            found = True
            
    return found

while True:
    if click():
        time.sleep(LOOP_DELAY)
        
    else:
        print(f"На экране маловероятное печенье либо его нет")
        time.sleep(0.5)
    