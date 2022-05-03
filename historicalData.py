import initialization
import Brokers.interactiveBrokers as interactiveBrokers

def getCandles(localSymbol, timeResolution, barSize):
    localSymbol = localSymbol
    secType = "FUT"
    exchange = "GLOBEX"
    currency = "USD"
    contract = interactiveBrokers.contract(localSymbol, secType, exchange, currency)
    initialization.IBClients[0].reqHistoricalData(1, contract, "", timeResolution, barSize, "TRADES", 0, 1, False, [])

def calculateStochastic(candlePosition, marketData):
    stocasticData = []
    position = len(marketData) - 1

    for marketDataRecord in range(position - candlePosition, position - candlePosition - 12, -1):
        stocasticData.append(marketData[marketDataRecord])

    #print("Close:" + str(stocasticData[0]["Close"]))
    #print("Close:" + str(stocasticData[1]["Close"]))
    #print("Close:" + str(stocasticData[2]["Close"]))
    #print("Min:" + str(findMin(stocasticData)))
    #print("Max:" + str(findMax(stocasticData)))
    #print("SMA:" + str((stocasticData[0]["Close"] + stocasticData[1]["Close"] + stocasticData[2]["Close"]) / 3))

    return (((stocasticData[0]["Close"] - findMin(stocasticData)) * 100) / (findMax(stocasticData) - findMin(stocasticData)))

def getStochastic(candlePosition, marketData):
    value = ((calculateStochastic(candlePosition, marketData) + calculateStochastic(candlePosition + 1, marketData) + calculateStochastic(candlePosition + 2, marketData)) / 3)
    return value

def findMax(values):
    numbers = []
    for value in values:
        numbers.append(value["High"])

    return max(numbers)

def findMin(values):
    numbers = []
    for value in values:
        numbers.append(value["Low"])

    return min(numbers)

