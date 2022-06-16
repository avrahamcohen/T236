#!/usr/bin/env python3

import time
import threading
from Support.utils import log
from Support.keepAlive import keepAlive
import Brokers.InteractiveBrokers.IBClient as interactiveBrokers
from Strategies.Futures.NQStrategy import startStrategy as M_NQM2startStrategy

IBClients = []
IBClientsId = [100, 200]

def initialization():
    global IBClients
    global IBClientsId

    log("Starting the NQ Future Strategy.")
    time.sleep(1)

    IBClients.append(interactiveBrokers.IBapi())
    IBClients[0].clientID = IBClientsId[0]

    startStrategyFuturesNasdaqThread = threading.Thread(target=M_NQM2startStrategy, args=(IBClients[0],), daemon=True)
    keepAliveThread = threading.Thread(target=keepAlive, args=(IBClients[0],), daemon=True)

    keepAliveThread.start()
    startStrategyFuturesNasdaqThread.start()
    startStrategyFuturesNasdaqThread.join()
    keepAliveThread.join()