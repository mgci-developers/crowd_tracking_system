# Video streaming backend hosted on device with camera

import cv2 # imports required libraries
from websockets.sync.client import connect
import time
from time import time_ns
import base64

NS_TO_MS: int = 1000000 # defines configurations
FPS = 30
SERVER_ADDRESS = "ws://localhost:8765"

vid = cv2.VideoCapture(0) # opens camera
numframes = 0 # keeps count of frames transmitted

while(True):
    with connect(SERVER_ADDRESS) as websocket: # connects to websocket server
        numframes += 1
        start_time = time_ns() // NS_TO_MS # keeps time for constant transmission frame rate
        ret, frame = vid.read() # 
        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        header = "A" * 30
        websocket.send(header + str(jpg_as_text)) # sends captured image with transmission header

        message = websocket.recv()
        if message != "image transfered successfully":
            print(f"The image did not transfer to the server, skipping frame") # displays error message to camera's terminal
        
        
        end_time = time_ns() // NS_TO_MS
        print(f"{str(min(FPS, 1000/(end_time - start_time)))} FPS") # displays frame rate
        next_tick = (1000/FPS) - (end_time - start_time)
        if next_tick < 0:
            next_tick = 0
        time.sleep(next_tick / 1000)    # keeps frame rate constant

