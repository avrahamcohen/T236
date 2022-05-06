#!/usr/bin/env python3

import threading
from Testing import test
from Support.utils import log
from Support.keepAlive import keepAlive
import Brokers.InteractiveBrokers.IBClient as interactiveBrokers
from Strategies.Futures.M_NQM2 import startStrategy as M_NQM2startStrategy

IBClients = []
IBClientsId = [100, 200]

def initialization():

    log("Starting the Future Strategy for the NQM2 and MNQM2 assets.")
    startStrategyFuturesNasdaqThread = threading.Thread(target=startStrategyFuturesNasdaq, args=(), daemon=True)
    startStrategyFuturesNasdaqThread.start()

    #print("Starting the Options Strategy for the NQM2 and MNQM2 assets.")
    #startStrategyOptionsNasdaqThread = threading.Thread(target=startStrategyOptionsNasdaq, args=(), daemon=True)
    #startStrategyOptionsNasdaqThread.start()

    #''' Testing '''
    #log("''' TESTING '''")
    #testingPurposesThread = threading.Thread(target=testingPurposes, args=(), daemon=True)
    #testingPurposesThread.start()
    #testingPurposesThread.join()

    #startStrategyOptionsNasdaqThread.join()
    startStrategyFuturesNasdaqThread.join()

def startStrategyFuturesNasdaq():
    global IBClients
    global IBClientsId

    IBClients.append(interactiveBrokers.IBapi())

    keepAliveThread = threading.Thread(target=keepAlive, args=(IBClients[0], IBClientsId[0],), daemon=True)
    keepAliveThread.start()

    M_NQM2startStrategy(IBClients[0])

    keepAliveThread.join()

def startStrategyOptionsNasdaq():
    pass

def testingPurposes():
    global IBClients
    global IBClientsId

    IBClients.append(interactiveBrokers.IBapi())

    keepAliveThread = threading.Thread(target=keepAlive, args=(IBClients[0], IBClientsId[1],), daemon=True)
    keepAliveThread.start()

    test.testHeikinAshi(IBClients[0])

    keepAliveThread.join()
