from ibapi.order import *
from ibapi.contract import Contract

def contract(localSymbol, secType, exchange, currency):
    contract = Contract()
    contract.localSymbol = localSymbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract

def executeOrder(IBapp ,contract, action, totalQuantity):
    order = Order()
    order.action = action
    order.totalQuantity = totalQuantity
    order.orderType = 'MKT'
    IBapp.placeOrder(IBapp.nextorderId, contract, order)
    IBapp.nextorderId += 1