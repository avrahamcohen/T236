#!/usr/bin/env python3

from ibapi.order import *
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class IBapi(EWrapper, EClient):
    historicalDataArray = []
    historicalDataEndStatus = False

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining,
              'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def historicalData(self, reqId, bar):
        self.historicalDataArray.append({"Open" : bar.open, "Close" : bar.close, "High" : bar.high, "Low" : bar.low, "Date" : bar.date})
        #print("Candels: Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.historicalDataEndStatus = True

    def error(self, reqId, errorCode, errorString):
        super().error(reqId, errorCode, errorString)

        print("(Avi)Error. Id:", reqId, "Code:", errorCode, "Msg:", errorString)

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        EWrapper.position(self, account, contract, position, avgCost)

        print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:",
        contract.secType, "Currency:", contract.currency, "Position:", position, "Avg cost:", avgCost)

        contract.exchange = "GLOBEX"

        if avgCost and position:
            order = Order()
            order.orderType = 'MKT'
            order.totalQuantity = abs(position)
            order.action = ('BUY', 'SELL')[position > 0]
            self.placeOrder(self.nextorderId, contract, order)
            self.nextorderId += 1
