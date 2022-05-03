def keepAlive(IBClient, clientId):
    IBClient.nextorderId = None

    while True:
        IBClient.connect('127.0.0.1', 4002, clientId)
        IBClient.nextorderId = None
        IBClient.run()

        while (IBClient.isConnected() == True): pass
