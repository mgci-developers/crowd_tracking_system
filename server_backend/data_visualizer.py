# Data visualizer for log files

import os
import matplotlib.pyplot as plt # graph visualiation library

for name in os.listdir("."): # reads through all files and checks if it is a text file
    if name.split(".")[-1] == "txt":
        with open(name) as file:
            times = []
            pplavgs = []
            a = file.readlines() # scans the file
            print(a)
            for k in a:
                try: # checks if the line is not the header
                    s = k.split()
                    print(s)
                    times.append(float(s[1])) 
                    pplavgs.append(float(s[0]))
                except:
                    pass  
            try:                  
                m = min(times)
                print(m)                    
                for s in range(len(times)): # converts time from unix timestamp format to hours after start of log
                    ns = times[s] 
                    ns -= m
                    times[s] = ns
                            

                plt.plot(times, pplavgs) # creates graph in matplotlib
                print(times)
                print(pplavgs)
                plt.title(name)
                plt.ylabel('Number of people in the room')
                plt.xlabel('time in hours after start of log')
                plt.show() # displays graph
            except:
                pass
