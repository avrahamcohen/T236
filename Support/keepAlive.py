#!/usr/bin/env python3
import time


def keepAlive(IBClient):
    IBClient.nextorderId = None

    while True:
        if ((IBClient.isConnected() == False) or (IBClient.errorCode == 502)):
            IBClient.connect('127.0.0.1', 4002, IBClient.clientID)
            IBClient.nextorderId = None
            IBClient.run()
            IBClient.disconnect()
    
            time.sleep(1)