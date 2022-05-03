from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

marketData = []
status = False

class IBapi(EWrapper, EClient):
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
        global marketData
        marketData.append({"Open" : bar.open, "Close" : bar.close, "High" : bar.high, "Low" : bar.low, "Date" : bar.date})
        print("Candels: (Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close,")")

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        global status
        status = True

    def position(self, account: str, contract: Contract, position: float,
                 avgCost: float):
        """
        Callback
        This event returns real-time positions for all accounts in
        response to the reqPositions() method.
        """
        EWrapper.position(self, account, contract, position, avgCost)

        # 1. Big Red Button should be in the active mode (Button pressed)
        # 2. Position should be real (avgCost > 0 and position is not 0)
        # 3. Cumulative account 'All' should be skipped
        if avgCost and position and (account != 'All'):
            order = Order()
            order.orderType = 'MKT'
            order.account = account
            order.totalQuantity = abs(position)
            order.action = ('BUY', 'SELL')[position > 0]
            self.placeOrder(self.nextId, contract, order)

def contract(localSymbol='', secType='', exchange='', currency=''):
    contract = Contract()
    contract.localSymbol = localSymbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract

def executeOrder(IBapp ,localSymbol, action):
    localSymbol = localSymbol
    secType = "FUT"
    exchange = "GLOBEX"
    currency = "USD"
    _contract = contract(localSymbol, secType, exchange, currency)

    order = Order()
    order.action = action
    order.totalQuantity = 1
    order.orderType = 'MKT'
    IBapp.placeOrder(IBapp.nextorderId, contract, order)
    IBapp.nextorderId += 1

