import threading
from keepAlive import keepAlive
from marketOrders import startTrade
import Brokers.interactiveBrokers as interactiveBrokers

'''
A socket connection between the API client application and TWS is established with the IBApi.EClientSocket.eConnect function. 
TWS acts as a server to receive requests from the API application (the client) and responds by taking appropriate actions. 
The first step is for the API client to initiate a connection to TWS on a socket port where TWS is already listening. 
It is possible to have multiple TWS instances running on the same computer if each is configured with a different API socket port number. 
Also, each TWS session can receive up to 32 different client applications simultaneously. 
The client ID field specified in the API connection is used to distinguish different API clients.
'''

IBClients = []

def initialization():
    global IBClients

    print("Starting the T236 Application.")

    IBClients.append(interactiveBrokers.IBapi())

    mainClientThread = threading.Thread(target=keepAlive, args=(IBClients[0], 126,), daemon=True)
    mainClientThread.start()

    startTrade("NQM2")

    mainClientThread.join()

