import time
from utils import *
import initialization
from historicalData import *
import Brokers.interactiveBrokers as interactiveBrokers

def startTrade(asset):
    FourHoursBarSizeMarketData = []
    ThirtyMinutesBarSizeMarketData = []

    FourHoursBarSizeMarketDataAnalysis = ""
    ThirtyMinutesBarSizeMarketDataAnalysis = ""

    currentHour = -1
    currentMinute = -1

    #TODO To check if it is possible to start the logic at 0000000 microsecond mark (1 second = 1000000 microseconds)
    while (datetime.datetime.now(tz=EST5EDT()).time().microsecond > 90000):
        pass

    #TODO Stock Exchange Stops at Friday 16:30 at and Opens at Sunday at 18:00
    while True:
        if not isTradeTime(datetime.time(17, 00), datetime.time(18, 00)):
            if isinstance(initialization.IBClients[0].nextorderId, int):
                if (((getDay() == "Sunday") and (datetime.datetime.now(tz=EST5EDT()).time().hour >= 18)) or
                        (getDay() == "Monday" or getDay() == "Tuesday" or getDay() == "Wednesday" or getDay() == "Thursday") or
                        ((getDay() == "Friday") and (isTradeTime(datetime.time(00, 00), datetime.time(16, 29))))):

                    if ((datetime.datetime.now(tz=EST5EDT()).time().hour in [2, 6, 10, 14, 18, 22]) and (datetime.datetime.now(tz=EST5EDT()).time().minute == 0)):
                        if currentHour != datetime.datetime.now(tz=EST5EDT()).time().hour:
                            print("Analyze Four Hours Market: " + str(datetime.datetime.now(tz=EST5EDT()).date()) + " , " + str(datetime.datetime.now(tz=EST5EDT()).time()))
                            getCandles(localSymbol=asset, timeResolution="3 D", barSize="4 hours")
                            while (interactiveBrokers.status == False):
                                pass
                            FourHoursBarSizeMarketData = interactiveBrokers.marketData
                            FourHoursBarSizeMarketDataAnalysis = analyzeMarketData(FourHoursBarSizeMarketData)
                            interactiveBrokers.marketData = []
                            interactiveBrokers.status = False
                            currentHour = datetime.datetime.now(tz=EST5EDT()).time().hour

                    if ((datetime.datetime.now(tz=EST5EDT()).time().minute in [0, 30])):
                        if currentMinute != datetime.datetime.now(tz=EST5EDT()).time().minute:
                            print("Analyze Thirty Minutes Market: " + str(datetime.datetime.now(tz=EST5EDT()).date()) + " , " + str(datetime.datetime.now(tz=EST5EDT()).time()))
                            getCandles(localSymbol=asset, timeResolution="1 D", barSize="30 mins")
                            while (interactiveBrokers.status == False):
                                pass
                            ThirtyMinutesBarSizeMarketData = interactiveBrokers.marketData
                            ThirtyMinutesBarSizeMarketDataAnalysis = analyzeMarketData(ThirtyMinutesBarSizeMarketData)
                            interactiveBrokers.marketData = []
                            interactiveBrokers.status = False
                            currentMinute = datetime.datetime.now(tz=EST5EDT()).time().minute

                    if (FourHoursBarSizeMarketDataAnalysis == "Long" and ThirtyMinutesBarSizeMarketDataAnalysis == "Long"):
                        print("Place Order: " + "Long + Long")
                        interactiveBrokers.executeOrder(initialization.IBClients[0] ,asset, "BUY")
                    elif (FourHoursBarSizeMarketDataAnalysis == "Long" and ThirtyMinutesBarSizeMarketDataAnalysis == "Short"):
                        print("Place Order: " + "Long + Short")
                        interactiveBrokers.executeOrder(initialization.IBClients[0] ,str("M" + asset), "SELL")
                    elif (FourHoursBarSizeMarketDataAnalysis == "Short" and ThirtyMinutesBarSizeMarketDataAnalysis == "Long"):
                        print("Place Order: " + "Short + Long")
                        interactiveBrokers.executeOrder(initialization.IBClients[0] ,str("M" + asset), "BUY")
                    elif (FourHoursBarSizeMarketDataAnalysis == "Short" and ThirtyMinutesBarSizeMarketDataAnalysis == "Short"):
                        print("Place Order: " + "Short + Short")
                        interactiveBrokers.executeOrder(initialization.IBClients[0] ,asset, "SELL")
                elif ((getDay() == "Friday") and (isTradeTime(datetime.time(16, 29), datetime.time(16, 30)))):
                    print("Close all positions! " + str(datetime.datetime.now(tz=EST5EDT()).date()) + " , " + str(datetime.datetime.now(tz=EST5EDT()).time()) + " , ")
                    initialization.IBClients[0].reqPositions()
            else:
                pass
                print("Lost connection.")
            time.sleep(1)

def analyzeMarketData(marketData):
    OverSold = 20
    OverBought = 80

    try:
        position = len(marketData) - 1
        print("Current candle is:" + str(marketData[position - 1]))
        openCurrent = 0.5 * (marketData[position - 1]["Open"] + marketData[position - 1]["Close"])
        openOnePrevious = 0.5 * (marketData[position - 2]["Open"] + marketData[position - 2]["Close"])
        closeCurrent = 0.25 * (marketData[position]["Open"] + marketData[position]["High"] + marketData[position]["Low"] + marketData[position]["Close"])
        closeOnePrevious = 0.25 * (marketData[position - 1]["Open"] + marketData[position - 1]["High"] + marketData[position - 1]["Low"] + marketData[position - 1]["Close"])

        print("Stochastic (-0):" + (str(getStochastic(0, marketData))))
        print("Stochastic (-1):" + (str(getStochastic(1, marketData))))
        print("Stochastic (-2):" + (str(getStochastic(2, marketData))))
        print("Stochastic (-3):" + (str(getStochastic(3, marketData))))

        # Long Trade
        if ((closeCurrent > openCurrent) and (closeOnePrevious < openOnePrevious)):
            if ((getStochastic(0, marketData) > OverSold) and (
                    (getStochastic(1, marketData) < OverSold) or
                    (getStochastic(2, marketData) < OverSold) or
                    (getStochastic(3, marketData) < OverSold))):
                print("Long Trade")
                return "Long"

        # Short Trade
        if ((closeCurrent < openCurrent) and (closeOnePrevious > openOnePrevious)):
            if ((getStochastic(0, marketData) < OverBought) and (
                    (getStochastic(1, marketData) > OverBought) or
                    (getStochastic(2, marketData) > OverBought) or
                    (getStochastic(3, marketData) > OverBought))):
                print("Short Trade")
                return "Short"
    except Exception as e:
        print(e)
        return ""

    return ""

