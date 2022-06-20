#!/usr/bin/env python3
import time
from Support.utils import log

def keepAlive(IBClient):
    IBClient.nextorderId = None

    while True:
        if (IBClient.errorCode == 2105):
            log("2105: A historical data farm is disconnected.", True)

        if ((IBClient.isConnected() == False) or (IBClient.errorCode == 502)):
            IBClient.connect('127.0.0.1', 4002, IBClient.clientID)
            IBClient.nextorderId = None
            IBClient.run()
            IBClient.disconnect()

            time.sleep(3)
            #IBClient.clientID = IBClient.clientID + 1
            #if (IBClient.clientID > 998):
            #    IBClient.clientID = 100
            #log("Reconnecting... " + str(IBClient.clientID), True)
