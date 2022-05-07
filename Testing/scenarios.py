#!/usr/bin/env python3

from Brokers.InteractiveBrokers.dataFarm import *
from Brokers.InteractiveBrokers.marketOrders import *

def testM_NQM2Strategy(IBClient):
    OverSold = 20
    OverBought = 80

    while not isinstance(IBClient.nextorderId, int):
        pass

    getCandles(IBClient, "3 D", "30 mins", "TRADES", contract("NQM2", "FUT", "GLOBEX", "USD"))

    while (IBClient.historicalDataEndStatus == False):
        pass

    heikinAshiData = getHeikinAshi(IBClient.historicalDataArray, False, True)

    for i in range(4, len(heikinAshiData)):
        isTrade = False
        try:
            openCurrent = heikinAshiData[i]["HAOpen"]
            openOnePrevious = heikinAshiData[i - 1]["HAOpen"]
            closeCurrent = heikinAshiData[i]["HAClose"]
            closeOnePrevious = heikinAshiData[i - 1]["HAClose"]

            # Long Trade
            if ((closeCurrent > openCurrent) and (closeOnePrevious < openOnePrevious)):
                if ((heikinAshiData[i]["Stochastic"] > OverSold) and (
                        (heikinAshiData[i-1]["Stochastic"] < OverSold) or
                        (heikinAshiData[i-2]["Stochastic"] < OverSold) or
                        (heikinAshiData[i-3]["Stochastic"] < OverSold) or
                        (heikinAshiData[i-4]["Stochastic"] < OverSold))):
                    print(str(heikinAshiData[i]) + " -> Order: Long Trade")
                    isTrade = True

            # Short Trade
            if ((closeCurrent < openCurrent) and (closeOnePrevious > openOnePrevious)):
                if ((heikinAshiData[i]["Stochastic"] < OverBought) and (
                        (heikinAshiData[i-1]["Stochastic"] > OverBought) or
                        (heikinAshiData[i-2]["Stochastic"] > OverBought) or
                        (heikinAshiData[i-3]["Stochastic"] > OverBought) or
                        (heikinAshiData[i-4]["Stochastic"] > OverBought))):
                    print(str(heikinAshiData[i]) + " -> Order: Short Trade")
                    isTrade = True

            # No Trade
            if isTrade == False:
                print(str(heikinAshiData[i]) + " -> Order: No Trade")

        except Exception as e:
            print(e)