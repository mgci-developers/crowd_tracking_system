# configuration file for the program

ipkeys = {}

# The following lines below need to be edited to configure the system
# -------------------------------------------------

DISPLAY = False #In the case that this program is being monitored by surveillance personell, the value should be set to True
ipkeys["ROOM 244"] = "10.202.41.194" # These are the IP addresses of the cameras, as well as the name of the location (displayed to the users). add more entries for more camears. This is in the case that the system runs with static IPs.


#-----------------------------------------------
# The lines above or below do not require to be edited


def getdisplay(): # functions 
    return DISPLAY

def getipkeys():
    return ipkeys