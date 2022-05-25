#!/usr/bin/env python3

import threading
from Testing import scenarios
from Support.utils import log
from Support.keepAlive import keepAlive
import Brokers.InteractiveBrokers.IBClient as interactiveBrokers

IBClients = []
IBClientsId = [100, 200]

def testing():
    ''' Testing '''
    log("''' TESTING '''")
    testingPurposesThread = threading.Thread(target=testScenario1, args=(), daemon=True)
    testingPurposesThread.start()
    testingPurposesThread.join()

'''testM_NQM2Strategy'''
def testM_NQM2Strategy():
    global IBClients
    global IBClientsId

    IBClients.append(interactiveBrokers.IBapi())

    keepAliveThread = threading.Thread(target=keepAlive, args=(IBClients[0], IBClientsId[1],), daemon=True)
    keepAliveThread.start()

    scenarios.testM_NQM2Strategy(IBClients[0])

    keepAliveThread.join()
