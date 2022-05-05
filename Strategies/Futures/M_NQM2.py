#!/usr/bin/env python3

import time
from Support.utils import *
from Brokers.InteractiveBrokers.dataFarm import *
from Brokers.InteractiveBrokers.marketOrders import *

currentHour = -1
currentMinute = -1

fourHoursBarSizeMarketDataAnalysisResult = "Short"
thirtyMinutesBarSizeMarketDataAnalysisResult = ""

def startStrategy(IBClient):
    global currentHour
    global currentMinute

    while (datetime.datetime.now(tz=EST5EDT()).time().microsecond > 90000):
        pass

    while True:
        if not isTradeTime(datetime.time(17, 00), datetime.time(18, 00)):
            if isinstance(IBClient.nextorderId, int):
                if (((getDay() == "Sunday") and (datetime.datetime.now(tz=EST5EDT()).time().hour >= 18)) or
                        (getDay() == "Monday" or getDay() == "Tuesday" or getDay() == "Wednesday" or getDay() == "Thursday") or
                        ((getDay() == "Friday") and (isTradeTime(datetime.time(00, 00), datetime.time(16, 29))))):

                    if ((datetime.datetime.now(tz=EST5EDT()).time().hour in [2, 6, 10, 14, 18, 22]) and (datetime.datetime.now(tz=EST5EDT()).time().minute == 0)):
                        analyzeFourHoursBarSizeHistoricalData(IBClient)

                    if ((datetime.datetime.now(tz=EST5EDT()).time().minute in [0, 30])):
                        if currentMinute != datetime.datetime.now(tz=EST5EDT()).time().minute:
                            analyzeThirtyMinutesBarSizeHistoricalData(IBClient)
                            stateMachine(IBClient, True)
                            currentMinute = datetime.datetime.now(tz=EST5EDT()).time().minute

                elif ((getDay() == "Friday") and (isTradeTime(datetime.time(16, 29), datetime.time(16, 30)))):
                    log("Close all positions.")
                    IBClient.reqPositions()
            else:
                log("Lost connection.")
            time.sleep(1)

def analyzeHistoricalData(marketData, barSize, DEBUG=False):
    OverSold = 20
    OverBought = 80

    try:
        position = len(marketData) - 1
        openCurrent = 0.5 * (marketData[position - 1]["Open"] + marketData[position - 1]["Close"])
        openOnePrevious = 0.5 * (marketData[position - 2]["Open"] + marketData[position - 2]["Close"])
        closeCurrent = 0.25 * (marketData[position]["Open"] + marketData[position]["High"] + marketData[position]["Low"] + marketData[position]["Close"])
        closeOnePrevious = 0.25 * (marketData[position - 1]["Open"] + marketData[position - 1]["High"] + marketData[position - 1]["Low"] + marketData[position - 1]["Close"])

        if DEBUG:
            log("Stochastic (0):" + (str(getStochastic(0, marketData))) + ".")
            log("Stochastic (1):" + (str(getStochastic(1, marketData))) + ".")
            log("Stochastic (2):" + (str(getStochastic(2, marketData))) + ".")
            log("Stochastic (3):" + (str(getStochastic(3, marketData))) + ".")

        # Long Trade
        if ((closeCurrent > openCurrent) and (closeOnePrevious < openOnePrevious)):
            if ((getStochastic(0, marketData) > OverSold) and (
                    (getStochastic(1, marketData) < OverSold) or
                    (getStochastic(2, marketData) < OverSold) or
                    (getStochastic(3, marketData) < OverSold))):
                if DEBUG:
                    log("Long Trade")
                return "Long"

        # Short Trade
        if ((closeCurrent < openCurrent) and (closeOnePrevious > openOnePrevious)):
            if ((getStochastic(0, marketData) < OverBought) and (
                    (getStochastic(1, marketData) > OverBought) or
                    (getStochastic(2, marketData) > OverBought) or
                    (getStochastic(3, marketData) > OverBought))):
                if DEBUG:
                    log("Short Trade")
                return "Short"
    except Exception as e:
        print(e)
    finally:
        if barSize == 4:
            return fourHoursBarSizeMarketDataAnalysisResult
        return ""

def analyzeFourHoursBarSizeHistoricalData(IBClient):
    global currentHour
    global fourHoursBarSizeMarketDataAnalysisResult

    if currentHour != datetime.datetime.now(tz=EST5EDT()).time().hour:
        fourHoursBarSizeMarketData = []
        log("Analyze Four Hours Market.")
        getCandles(IBClient, "3 D", "4 hours", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))
        while (IBClient.historicalDataEndStatus == False):
            pass
        fourHoursBarSizeMarketData = IBClient.historicalDataArray
        fourHoursBarSizeMarketDataAnalysisResult = analyzeHistoricalData(fourHoursBarSizeMarketData, 4, False)
        IBClient.historicalDataArray = []
        IBClient.historicalDataEndStatus = False
        currentHour = datetime.datetime.now(tz=EST5EDT()).time().hour

def analyzeThirtyMinutesBarSizeHistoricalData(IBClient):
    global currentMinute
    global thirtyMinutesBarSizeMarketDataAnalysisResult

    thirtyMinutesBarSizeMarketData = []
    thirtyMinutesBarSizeMarketDataAnalysisResult = ""

    log("Analyze Thirty Minutes Market.")
    getCandles(IBClient, "1 D", "30 mins", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))
    while (IBClient.historicalDataEndStatus == False):
        pass
    thirtyMinutesBarSizeMarketData = IBClient.historicalDataArray
    thirtyMinutesBarSizeMarketDataAnalysisResult = analyzeHistoricalData(thirtyMinutesBarSizeMarketData, 30, False)
    IBClient.historicalDataArray = []
    IBClient.historicalDataEndStatus = False

def stateMachine(IBClient, DEBUG=False):
    global fourHoursBarSizeMarketDataAnalysisResult
    global thirtyMinutesBarSizeMarketDataAnalysisResult

    if DEBUG:
        log("Place Order: (" +
              str(fourHoursBarSizeMarketDataAnalysisResult if fourHoursBarSizeMarketDataAnalysisResult != "" else "No Entry") + "," +
              str(thirtyMinutesBarSizeMarketDataAnalysisResult if thirtyMinutesBarSizeMarketDataAnalysisResult != "" else "No Entry") + ").")

    if (fourHoursBarSizeMarketDataAnalysisResult == "Long" and thirtyMinutesBarSizeMarketDataAnalysisResult == "Long"):
        executeOrder(IBClient, contract("NQM2", "FUT", "GLOBEX", "USD"), "BUY", 1)
    elif (fourHoursBarSizeMarketDataAnalysisResult == "Long" and thirtyMinutesBarSizeMarketDataAnalysisResult == "Short"):
        executeOrder(IBClient, contract("MNQM2", "FUT", "GLOBEX", "USD"), "SELL", 4)
    elif (fourHoursBarSizeMarketDataAnalysisResult == "Short" and thirtyMinutesBarSizeMarketDataAnalysisResult == "Long"):
        executeOrder(IBClient, contract("MNQM2", "FUT", "GLOBEX", "USD"), "BUY", 4)
    elif (fourHoursBarSizeMarketDataAnalysisResult == "Short" and thirtyMinutesBarSizeMarketDataAnalysisResult == "Short"):
        executeOrder(IBClient, contract("NQM2", "FUT", "GLOBEX", "USD"), "SELL", 1)