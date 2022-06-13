#!/usr/bin/env python3

import time
from Support.utils import *
from Brokers.InteractiveBrokers.dataFarm import *
from Brokers.InteractiveBrokers.marketOrders import *

currentHour = -1
currentMinute = -1

class Trend:
    SHORT = 1
    LONG = 2
    NA = 3

fourHoursBarSizeMarketDataAnalysisResult = Trend.NA
thirtyMinutesBarSizeMarketDataAnalysisResult = Trend.NA

def clockInit():
    #TODO Improve this.
    while (datetime.datetime.now(tz=EST5EDT()).time().microsecond > 90000):
        pass

def startStrategy(IBClient):
    global currentHour
    global currentMinute

    fourHoursBarSizeMarketDataAnalysisResult = fourHoursBarSizeMarketDataAnalysisResultInitialization(IBClient)

    if (fourHoursBarSizeMarketDataAnalysisResult == Trend.NA):
        log("Could not identified 4 hours bar size trend. Exiting.")
        exit(0)
    log("4 Hour bar size trend set to: " + str("Long" if fourHoursBarSizeMarketDataAnalysisResult == Trend.LONG else ("Short" if fourHoursBarSizeMarketDataAnalysisResult == Trend.SHORT else "Error")) + ".\n")

    clockInit()

    while True:
        try:
            if not isTradeTime(datetime.time(17, 00), datetime.time(18, 00)):
                if isinstance(IBClient.nextorderId, int):
                    if (((getDay() == "Sunday") and (datetime.datetime.now(tz=EST5EDT()).time().hour >= 18)) or
                            (getDay() == "Monday" or getDay() == "Tuesday" or getDay() == "Wednesday" or getDay() == "Thursday") or
                            ((getDay() == "Friday") and (isTradeTime(datetime.time(00, 00), datetime.time(16, 29))))):

                        if ((datetime.datetime.now(tz=EST5EDT()).time().hour in [2, 6, 10, 14, 18, 22]) and (datetime.datetime.now(tz=EST5EDT()).time().minute == 0)):
                            time.sleep(1)
                            analyzeFourHoursBarSizeHistoricalData(IBClient)

                        if ((datetime.datetime.now(tz=EST5EDT()).time().minute in [0, 30])):
                            if currentMinute != datetime.datetime.now(tz=EST5EDT()).time().minute:
                                time.sleep(1)
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
    OverSold = 20
    OverBought = 80

    try:
        heikinAshiData = getHeikinAshi(marketData, False, False)
        position = len(heikinAshiData) - 1
        openCurrent = heikinAshiData[position]["HAOpen"]
        openOnePrevious = heikinAshiData[position - 1]["HAOpen"]
        closeCurrent = heikinAshiData[position]["HAClose"]
        closeOnePrevious = heikinAshiData[position - 1]["HAClose"]

        if DEBUG:
            log(" HAOpen:" + str(openCurrent) + " , HAClose:" + str(closeCurrent) + " , Stochastic:" + (str(getStochastic(0, marketData))) + ".")

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
    global currentHour
    global fourHoursBarSizeMarketDataAnalysisResult

    if currentHour != datetime.datetime.now(tz=EST5EDT()).time().hour:
        fourHoursBarSizeMarketData = []
        log("Analyze Four Hours Market.")
        getCandles(IBClient, "5 D", "4 hours", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))
        while (IBClient.historicalDataEndStatus == False):
            pass
        fourHoursBarSizeMarketData = IBClient.historicalDataArray
        fourHoursBarSizeMarketDataAnalysisResult = analyzeHistoricalData(fourHoursBarSizeMarketData, 4, True)
        IBClient.historicalDataArray = []
        IBClient.historicalDataEndStatus = False
        currentHour = datetime.datetime.now(tz=EST5EDT()).time().hour
        log("Analyze Four Hours Market End.")

def analyzeThirtyMinutesBarSizeHistoricalData(IBClient):
    global currentMinute
    global thirtyMinutesBarSizeMarketDataAnalysisResult

    thirtyMinutesBarSizeMarketData = []
    thirtyMinutesBarSizeMarketDataAnalysisResult = Trend.NA
    log("Analyze Thirty Minutes Market.")
    getCandles(IBClient, "3 D", "30 mins", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))
    while (IBClient.historicalDataEndStatus == False):
        pass
    thirtyMinutesBarSizeMarketData = IBClient.historicalDataArray
    thirtyMinutesBarSizeMarketDataAnalysisResult = analyzeHistoricalData(thirtyMinutesBarSizeMarketData, 30, True)
    IBClient.historicalDataArray = []
    IBClient.historicalDataEndStatus = False
    log("Analyze Thirty Minutes Market End.")

def stateMachine(IBClient, DEBUG=False):
    global fourHoursBarSizeMarketDataAnalysisResult
    global thirtyMinutesBarSizeMarketDataAnalysisResult

    try:
        with open('orders.txt', 'a') as orders:
            orders.write(str(datetime.datetime.now(tz=EST5EDT()).date()) + " " + str(datetime.datetime.now(tz=EST5EDT()).time()) + ": " + "Place Order: (" + 
                    str("Long" if fourHoursBarSizeMarketDataAnalysisResult == Trend.LONG else "Short") + " , " + 
                    str("Long" if thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.LONG else ("Short" if thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.SHORT else "No Entry")) + ").\n")

    except:
        log("Log Error (StateMachine)")
        pass

    if (fourHoursBarSizeMarketDataAnalysisResult == Trend.LONG and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.LONG):
        log("Place Order: (Long, Long)", True)
        executeOrder(IBClient, contract("NQM2", "FUT", "GLOBEX", "USD"), "BUY", 1, "MKT")
        executeOrder(IBClient, contract("NQM2", "FUT", "GLOBEX", "USD"), "SELL", 1, "TRAIL", 20)
    elif (fourHoursBarSizeMarketDataAnalysisResult == Trend.LONG and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.SHORT):
        log("Place Order: (Long, Short)", True)
        executeOrder(IBClient, contract("MNQM2", "FUT", "GLOBEX", "USD"), "SELL", 4, "MKT")
        executeOrder(IBClient, contract("MNQM2", "FUT", "GLOBEX", "USD"), "BUY", 4, "TRAIL", 20)
    elif (fourHoursBarSizeMarketDataAnalysisResult == Trend.SHORT and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.LONG):
        log("Place Order: (Short, Long)", True)
        executeOrder(IBClient, contract("MNQM2", "FUT", "GLOBEX", "USD"), "BUY", 4, "MKT")
        executeOrder(IBClient, contract("MNQM2", "FUT", "GLOBEX", "USD"), "SELL", 4, "TRAIL", 20)
    elif (fourHoursBarSizeMarketDataAnalysisResult == Trend.SHORT and thirtyMinutesBarSizeMarketDataAnalysisResult == Trend.SHORT):
        log("Place Order: (Short, Short)", True)
        executeOrder(IBClient, contract("NQM2", "FUT", "GLOBEX", "USD"), "SELL", 1, "MKT")
        executeOrder(IBClient, contract("NQM2", "FUT", "GLOBEX", "USD"), "BUY", 1, "TRAIL", 20)

def fourHoursBarSizeMarketDataAnalysisResultInitialization(IBClient):
    OverSold = 20
    OverBought = 80
    isTrade = False

    while not isinstance(IBClient.nextorderId, int):
        pass

    getCandles(IBClient, "5 D", "4 hours", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))

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

    return isTrade