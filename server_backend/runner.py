'''
 CrowdTrack(TM) backend system by Visiontech Computer Vision Systems inc. (R)
 Devleoped by Bala Venkataraman, June 2023 

 FUNCTIONALITY

 server side AI image analysis program for tracking crowds and delivering statistics
 functions: recieves an image stream from each camera, uses the pretrained YOLO neural network to calculate the number of people
 uploads the number of people in each point of interest to a separate program, which handles API integrations
 
 In the case that this program is being monitored by surveillance personell, the variable DISPLAY in the configurations file can be edited
 
 SECURITY
 This system tracks cameras based on their IP addresses (this is given that the computers will all be given static IPs). Due to the static IP, that particular camera will be the only device to ever be assigned that IP address (assuming the integrity of the network itself is uncompromised).
 In the case that the network uses DHCP based IP address assignment instead of static IPs for the camera systems, the code can be configured to use a client key stored on the camera
 Websockets can also be encrypted if extra security is required (encryption is required in the DHCP case if the client key is transmitted)
'''
import asyncio # imports required libraries
from websockets.server import serve
import base64
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
from configs import getipkeys, getdisplay

DISPLAY = getdisplay() # load models, configurations, and declare variables
model = YOLO('yolov8s.pt')
ipkeys = getipkeys()
roomcrowds = {}
movingaverages = {}
movingaveragetimes = {}
numframes = 0

for i in ipkeys.values(): # define all dictionary elements for population and moving average dictionaries
    roomcrowds[i] = 0
for i in roomcrowds.keys():
    movingaverages[i] = 0
    movingaveragetimes[i] = 0

async def sockanal(websocket): # Analyzes websocket data
    global numframes
    global ipkeys
    global roomcrowds

    remote_ip = websocket.remote_address[0] 

    async for fmessage in websocket:       
        receievedhead = fmessage[:30] # gets header from websocket data

        if receievedhead == "A" * 30: # image transmission data

            message = fmessage[31:]
            nparr = np.frombuffer(base64.b64decode(message), np.uint8) # decodes base64 image to Numpy matrix
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # converts matrix to opencv format image

            results = model.predict(source=img) # passes image into AI model
            a = (results[0].boxes.cls).tolist() # gets results
            
            numpeople = 0
            for i in a: # calculates number of people
                if i == 0:
                    numpeople += 1

            roomcrowds[remote_ip] = numpeople # updates statistics
            movingaverages[remote_ip] = (movingaverages[remote_ip]*movingaveragetimes[remote_ip] + numpeople)/(movingaveragetimes[remote_ip] + 1)
            movingaveragetimes[remote_ip] += 1

            if movingaveragetimes[remote_ip] >= 100: # resets average after 100 frames
                f = open(f"logs_{remote_ip}.txt", "a")
                f.write("\n" + str(movingaverages[remote_ip]) + "   " +  str(datetime.now().timestamp()))
                f.close()
                movingaveragetimes[remote_ip] = 0
                movingaverages[remote_ip] = 0   
            
            if DISPLAY: # displays video streams in the case of human surveillance
                cv2.imshow(str(remote_ip), img) 
            if DISPLAY and cv2.waitKey(1) & 0xFF == ord('q'):
                break        
            
            numframes += 1
            print("transmitted frames = " + str(numframes)) # prints out number of transmitted frames
            
            
            await websocket.send("image transfered successfully") # returns success message
        elif receievedhead == "B" * 30: # data request header
            message = fmessage[30:]
            await websocket.send(str(roomcrowds[message])) # sends number of people in correspondig room


async def main():
    async with serve(sockanal, "0.0.0.0", 8765): # serves socket with input sent to the analysis function
        print("the websocket server has started")
        await asyncio.Future()  # run forever

asyncio.run(main()) # runs main function asynchronously

if DISPLAY: # closes all video stream windows on program close
    cv2.destroyAllWindows()