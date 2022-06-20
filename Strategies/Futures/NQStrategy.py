#!/usr/bin/env python3

import time
from Support.utils import *
from Brokers.InteractiveBrokers.dataFarm import *
from Brokers.InteractiveBrokers.marketOrders import *

currentHour = -1
currentMinute = -1

class Trend:
    SHORT = "Short"
    LONG = "Long"
    NA = "None"

fourHoursBarSizeMarketDataAnalysisResult = Trend.NA
thirtyMinutesBarSizeMarketDataAnalysisResult = Trend.NA

miniContract = "NQU2"
microContract = "MNQU2"

def clockInit():
    while (datetime.datetime.now(tz=EST5EDT()).time().microsecond > 90000):
        pass
    log("Clock initialization.")

def startStrategy(IBClient):
    global currentHour
    global currentMinute
    global fourHoursBarSizeMarketDataAnalysisResult

    fourHoursBarSizeMarketDataAnalysisResult = fourHoursBarSizeMarketDataAnalysisResultInitialization(IBClient)

    if (fourHoursBarSizeMarketDataAnalysisResult == "None"):
        log("Could not identified 4 hours bar size trend. Exiting.")
        exit(0)
    log("4 Hour bar size trend set to: " + str(fourHoursBarSizeMarketDataAnalysisResult))

    clockInit()

    while True:
        try:
            if not isTradeTime(datetime.time(17, 00), datetime.time(18, 00)):
                if isinstance(IBClient.nextorderId, int):
                    if (((getDay() == "Sunday") and (datetime.datetime.now(tz=EST5EDT()).time().hour >= 18)) or
                            (getDay() == "Monday" or getDay() == "Tuesday" or getDay() == "Wednesday" or getDay() == "Thursday") or
                            ((getDay() == "Friday") and (isTradeTime(datetime.time(00, 00), datetime.time(16, 29))))):

                        if ((datetime.datetime.now(tz=EST5EDT()).time().hour in [2, 6, 10, 14, 18, 22]) and (datetime.datetime.now(tz=EST5EDT()).time().minute == 0)):
                            #time.sleep(1)
                            analyzeFourHoursBarSizeHistoricalData(IBClient)

                        if ((datetime.datetime.now(tz=EST5EDT()).time().minute in [0, 30])):
                            if currentMinute != datetime.datetime.now(tz=EST5EDT()).time().minute:
                                #time.sleep(1)
                                analyzeThirtyMinutesBarSizeHistoricalData(IBClient)
                                stateMachine(IBClient, True)
                                currentMinute = datetime.datetime.now(tz=EST5EDT()).time().minute

                    elif ((getDay() == "Friday") and (isTradeTime(datetime.time(16, 29), datetime.time(16, 30)))):
                        log("Close all positions.")
                        IBClient.reqPositions()
                        closeAllPositions(IBClient)
                        time.sleep(60)
                        clockInit()
                else:
                    log("Lost connection.")
                time.sleep(1)
        except:
            pass

def closeAllPositions(IBClient):
    while (IBClient.openPositionDataEndStatus == False):
        pass
    for position in IBClient.openPositionDataArray:
        if position["avgCost"] and position["position"]:
            position["contract"].exchange = "GLOBEX"
            executeOrder(IBClient, position["contract"], ('BUY', 'SELL')[position["position"] > 0], abs(position["position"]), "MKT")

    IBClient.openPositionDataArray = []
    IBClient.openPositionDataEndStatus = False

def analyzeHistoricalData(marketData, barSize, DEBUG=False):
    global fourHoursBarSizeMarketDataAnalysisResult
    OverSold = 20
    OverBought = 80

    try:
        heikinAshiData = getHeikinAshi(marketData, False, True)
        position = len(heikinAshiData) - 1
        openCurrent = heikinAshiData[position]["HAOpen"]
        openOnePrevious = heikinAshiData[position - 1]["HAOpen"]
        closeCurrent = heikinAshiData[position]["HAClose"]
        closeOnePrevious = heikinAshiData[position - 1]["HAClose"]

        if DEBUG:
            log("Open: " + str(marketData[position]["Open"]) + " Close: " + str(marketData[position]["Close"]) +
                " HAOpen: " + str(openCurrent) + " HAClose: " + str(closeCurrent) +
                " PHAOpen: " + str(openOnePrevious) + " PHAClose: " + str(closeOnePrevious) +" Stochastic: " + (
                    str(getStochastic(0, marketData))) + " : Bar Close Values", True)

        # Long Trade
        if ((closeCurrent > openCurrent) and (closeOnePrevious < openOnePrevious)):
            if ((getStochastic(0, marketData) > OverSold) and (
                    (getStochastic(1, marketData) < OverSold) or
                    (getStochastic(2, marketData) < OverSold) or
                    (getStochastic(3, marketData) < OverSold) or
                    (getStochastic(4, marketData) < OverSold))):
                return Trend.LONG

        # Short Trade
        if ((closeCurrent < openCurrent) and (closeOnePrevious > openOnePrevious)):
            if ((getStochastic(0, marketData) < OverBought) and (
                    (getStochastic(1, marketData) > OverBought) or
                    (getStochastic(2, marketData) > OverBought) or
                    (getStochastic(3, marketData) > OverBought) or
                    (getStochastic(4, marketData) > OverBought))):
                return Trend.SHORT

        if barSize == 4:
            return fourHoursBarSizeMarketDataAnalysisResult

        return Trend.NA
    
    except Exception as e:
        print(e)

def analyzeFourHoursBarSizeHistoricalData(IBClient):
    global miniContract
    global currentHour
    global fourHoursBarSizeMarketDataAnalysisResult

    if currentHour != datetime.datetime.now(tz=EST5EDT()).time().hour:
        fourHoursBarSizeMarketData = []
        getCandles(IBClient, "5 D", "4 hours", "TRADES", contract(miniContract, "FUT", "GLOBEX", "USD"))
        while (IBClient.historicalDataEndStatus == False):
            pass
        fourHoursBarSizeMarketData = IBClient.historicalDataArray
        fourHoursBarSizeMarketDataAnalysisResult = analyzeHistoricalData(fourHoursBarSizeMarketData, 4, True)
        IBClient.historicalDataArray = []
        IBClient.historicalDataEndStatus = False
        currentHour = datetime.datetime.now(tz=EST5EDT()).time().hour

def analyzeThirtyMinutesBarSizeHistoricalData(IBClient):
    global miniContract
    global currentMinute
    global thirtyMinutesBarSizeMarketDataAnalysisResult

    thirtyMinutesBarSizeMarketData = []
    thirtyMinutesBarSizeMarketDataAnalysisResult = Trend.NA
    getCandles(IBClient, "3 D", "30 mins", "TRADES", contract(miniContract, "FUT", "GLOBEX", "USD"))
    while (IBClient.historicalDataEndStatus == False):
        pass
    thirtyMinutesBarSizeMarketData = IBClient.historicalDataArray
    thirtyMinutesBarSizeMarketDataAnalysisResult = analyzeHistoricalData(thirtyMinutesBarSizeMarketData, 30, True)
    IBClient.historicalDataArray = []
    IBClient.historicalDataEndStatus = False

def stateMachine(IBClient, DEBUG=False):
    global miniContract
    global microContract
    global fourHoursBarSizeMarketDataAnalysisResult
    global thirtyMinutesBarSizeMarketDataAnalysisResult

    try:
        with open('orders.txt', 'a') as orders:
            orders.write(str(datetime.datetime.now(tz=EST5EDT()).date()) + " " + str(datetime.datetime.now(tz=EST5EDT()).time()) + ": " + "Place Order: (" + 
                    str(fourHoursBarSizeMarketDataAnalysisResult) + " , " + str(thirtyMinutesBarSizeMarketDataAnalysisResult) + ").\n")

    except:
        log("Log Error (StateMachine)")
        pass

    log("Placing Order: " + str(fourHoursBarSizeMarketDataAnalysisResult) + ", " + str(thirtyMinutesBarSizeMarketDataAnalysisResult))
    if (fourHoursBarSizeMarketDataAnalysisResult == Trend.LONG and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.LONG):
        log("Place Order: (Long, Long)", True)
        executeOrder(IBClient, contract(miniContract, "FUT", "GLOBEX", "USD"), "BUY", 1, "MKT")
        executeOrder(IBClient, contract(miniContract, "FUT", "GLOBEX", "USD"), "SELL", 1, "TRAIL", 20)
    elif (fourHoursBarSizeMarketDataAnalysisResult == Trend.LONG and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.SHORT):
        log("Place Order: (Long, Short)", True)
        executeOrder(IBClient, contract(microContract, "FUT", "GLOBEX", "USD"), "SELL", 4, "MKT")
        executeOrder(IBClient, contract(microContract, "FUT", "GLOBEX", "USD"), "BUY", 4, "TRAIL", 20)
    elif (fourHoursBarSizeMarketDataAnalysisResult == Trend.SHORT and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.LONG):
        log("Place Order: (Short, Long)", True)
        executeOrder(IBClient, contract(microContract, "FUT", "GLOBEX", "USD"), "BUY", 4, "MKT")
        executeOrder(IBClient, contract(microContract, "FUT", "GLOBEX", "USD"), "SELL", 4, "TRAIL", 20)
    elif (fourHoursBarSizeMarketDataAnalysisResult == Trend.SHORT and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.SHORT):
        log("Place Order: (Short, Short)", True)
        executeOrder(IBClient, contract(miniContract, "FUT", "GLOBEX", "USD"), "SELL", 1, "MKT")
        executeOrder(IBClient, contract(miniContract, "FUT", "GLOBEX", "USD"), "BUY", 1, "TRAIL", 20)

def fourHoursBarSizeMarketDataAnalysisResultInitialization(IBClient):
    global miniContract
    OverSold = 20
    OverBought = 80
    isTrade = False

    while not isinstance(IBClient.nextorderId, int):
        pass

    getCandles(IBClient, "5 D", "4 hours", "TRADES", contract(miniContract, "FUT", "GLOBEX", "USD"))

    while (IBClient.historicalDataEndStatus == False):
        pass

    heikinAshiData = getHeikinAshi(IBClient.historicalDataArray, False, True)

    for i in range(4, len(heikinAshiData)):
        try:
            openCurrent = heikinAshiData[i]["HAOpen"]
            openOnePrevious = heikinAshiData[i - 1]["HAOpen"]
            closeCurrent = heikinAshiData[i]["HAClose"]
            closeOnePrevious = heikinAshiData[i - 1]["HAClose"]

            # Long Trade
            if ((closeCurrent > openCurrent) and (closeOnePrevious < openOnePrevious)):
                if ((heikinAshiData[i]["Stochastic"] > OverSold) and (
                        (heikinAshiData[i - 1]["Stochastic"] < OverSold) or
                        (heikinAshiData[i - 2]["Stochastic"] < OverSold) or
                        (heikinAshiData[i - 3]["Stochastic"] < OverSold) or
                        (heikinAshiData[i - 4]["Stochastic"] < OverSold))):
                    isTrade = Trend.LONG

            # Short Trade
            if ((closeCurrent < openCurrent) and (closeOnePrevious > openOnePrevious)):
                if ((heikinAshiData[i]["Stochastic"] < OverBought) and (
                        (heikinAshiData[i - 1]["Stochastic"] > OverBought) or
                        (heikinAshiData[i - 2]["Stochastic"] > OverBought) or
                        (heikinAshiData[i - 3]["Stochastic"] > OverBought) or
                        (heikinAshiData[i - 4]["Stochastic"] > OverBought))):
                    isTrade = Trend.SHORT

        except Exception as e:
            print(e)

    IBClient.historicalDataArray = []
    IBClient.historicalDataEndStatus = False
    return isTrade