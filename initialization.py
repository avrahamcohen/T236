#!/usr/bin/env python3

import time
import threading
from Support.utils import log
from Support.keepAlive import keepAlive
import Brokers.InteractiveBrokers.IBClient as interactiveBrokers
from Strategies.Futures.M_NQM2 import startStrategy as M_NQM2startStrategy

IBClients = []
IBClientsId = [100, 200]

def initialization():

    log("Starting the Future Strategy for the NQM2 and MNQM2 assets.")
    time.sleep(1)
    startStrategyFuturesNasdaqThread = threading.Thread(target=startStrategyFuturesNasdaq, args=(), daemon=True)
    startStrategyFuturesNasdaqThread.start()
    startStrategyFuturesNasdaqThread.join()

def startStrategyFuturesNasdaq():
    global IBClients
    global IBClientsId

    IBClients.append(interactiveBrokers.IBapi())
    IBClients[0].clientID = IBClientsId[0]

    keepAliveThread = threading.Thread(target=keepAlive, args=(IBClients[0],), daemon=True)
    keepAliveThread.start()
    M_NQM2startStrategy(IBClients[0])
    keepAliveThread.join()

def startStrategyOptionsNasdaq():
    pass