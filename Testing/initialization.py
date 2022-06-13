#!/usr/bin/env python3

import time
import threading
from Support.utils import log
from Support.keepAlive import keepAlive
from Testing.scenarios import testM_NQM2Strategy
import Brokers.InteractiveBrokers.IBClient as interactiveBrokers

IBClients = []
IBClientsId = [100, 200]

def testing():
    global IBClients
    global IBClientsId

    log("Testing")
    time.sleep(1)

    IBClients.append(interactiveBrokers.IBapi())
    IBClients[0].clientID = IBClientsId[0]

    testingPurposesThread = threading.Thread(target=testM_NQM2Strategy, args=(IBClients[0],), daemon=True)
    keepAliveThread = threading.Thread(target=keepAlive, args=(IBClients[0],), daemon=True)

    keepAliveThread.start()
    testingPurposesThread.start()
    testingPurposesThread.join()
    keepAliveThread.join()






    ()


