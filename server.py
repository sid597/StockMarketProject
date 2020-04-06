from concurrent import futures
import logging
import grpc
import stock_exchange_pb2
import stock_exchange_pb2_grpc
from pprint import pprint
from collections import OrderedDict 

class trader:

    def __init__(self,oid,purchaseType,stockQty,stockPrice,creationTime,stock,name):
        self.oid = oid
        self.purchaseType = purchaseType
        self.stockQty = stockQty
        self.stockPrice = stockPrice
        self.creationTime = creationTime
        self.matching = []
        self.active = True
        self.stock = stock
        self.name = name
        self.withWhom = set()
        self.initialStockQty = stockQty
  
class StockExchange(stock_exchange_pb2_grpc.StockExchangeServicer):
    market = {'allOrders':{}}
    oid = 1    #Unique id
    userOrders = {}

    def checkIfTraderCanBuy(self,trader):
        sellersForTradersStock = self.market[trader.stock]['sellers']
        # print 'Here to Buy'
        res = 'N'
        if len(sellersForTradersStock) == 0:
            self.market[trader.stock]['buyers'][trader.oid] = {'stockPrice':trader.stockPrice, 'stockQty':trader.stockQty} 
        else:
            for pid in sellersForTradersStock:
                
                Id = sellersForTradersStock[pid]
                
                
                if (trader.stockPrice >= Id['stockPrice']) and (trader.stockQty >0):
                    
                    if Id['stockQty'] > trader.stockQty :
                        '''
                        Mark trader inactive
                        update Id stock qty
                        add to their matching  
                    self.market['allOrders'][trader.oid]    '''
                        # print 'Greater'
                        # add with whom this transaction made 
                        self.market['allOrders'][trader.oid]['withWhom'].add(pid)
                        self.market['allOrders'][pid]['withWhom'].add(trader.oid)


                         
                        self.market['allOrders'][trader.oid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=trader.stockQty,price=Id['stockPrice'],created_at=trader.creationTime))
                        self.market['allOrders'][pid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=trader.stockQty,price=Id['stockPrice'],created_at=trader.creationTime))

                        remaining = Id['stockQty'] - trader.stockQty
                        self.market['allOrders'][trader.oid]['active'] = False
                        
                        
                        # print trader.stockQty*Id['stockPrice']
                        self.market[trader.stock]['volume']+= trader.stockQty
                        self.market[trader.stock]['allStockPrice']+= trader.stockQty*Id['stockPrice']
                        Id['stockQty'] = remaining
                        self.market['allOrders'][trader.oid]['stockQty'] = 0
                        res = 'Y'
                        # print self.market[trader.stock]['sellers']




                    elif Id['stockQty'] == trader.stockQty:
                        '''
                        Mark BOTH of them inactive
                        Remove id from sellers list
                        add to their matching to OrderMatch
                        update volume of the stock purchase
                        update all stocks value for this stock
                        '''
                        # print 'Equal'
                        # add with whom this transaction made 
                        self.market['allOrders'][trader.oid]['withWhom'].add(pid)
                        self.market['allOrders'][pid]['withWhom'].add(trader.oid)

                        self.market['allOrders'][trader.oid]['active'] = False
                        self.market['allOrders'][trader.oid]['active'] = False
                        


                        self.market['allOrders'][pid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=0,price=Id['stockPrice'],created_at=trader.creationTime))
                        self.market['allOrders'][trader.oid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=trader.stockQty,price=Id['stockPrice'],created_at=trader.creationTime))
                        
                        
                        
                        self.market[trader.stock]['volume']+= trader.stockQty
                        self.market[trader.stock]['allStockPrice']+= trader.stockQty*trader.stockPrice
                        Id['stockQty'] = 0
                        self.market['allOrders'][trader.oid]['stockQty'] = 0
                        self.market[trader.stock]['sellers'].pop(pid)
                        # print self.market[trader.stock]['sellers']
                        res = 'Y'

                    else:
                        '''
                        Mark Id one Inactive and mark qty 0 
                        remove id from sellers list
                        update traders stock qty
                        add to their matching to OrderMatch
                        update volume of the stock purchase
                        update all stocks value for this stock
                        '''
                        # print 'LessThan'
                        # add with whom this transaction made 
                        self.market['allOrders'][trader.oid]['withWhom'].add(pid)
                        self.market['allOrders'][pid]['withWhom'].add(trader.oid)

                        remaining =  trader.stockQty-Id['stockQty'] 
                        
                        self.market['allOrders'][trader.oid]['active'] = False

                        self.market['allOrders'][pid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=Id['stockQty'],price=Id['stockPrice'],created_at=trader.creationTime))
                        self.market['allOrders'][trader.oid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=Id['stockQty'],price=Id['stockPrice'],created_at=trader.creationTime))
                       
                        self.market[trader.stock]['volume']+= Id['stockQty']
                        self.market[trader.stock]['allStockPrice']+= Id['stockQty'] * Id['stockPrice']

                        Id['stockQty'] = 0
                        self.market['allOrders'][trader.oid]['stockQty'] = 0
                        
                       # print remaining
                        self.market['allOrders'][trader.oid]['stockQty'] = remaining
                        trader.stockQty = remaining
                        self.market[trader.stock]['sellers'].pop(pid)
                        # print self.market[trader.stock]['sellers']
                        res = 'Y'
        if res =='N':
            self.market[trader.stock]['buyers'][trader.oid] = {'stockPrice':trader.stockPrice, 'stockQty':trader.stockQty} 
               
        return res 
            

    def checkIfTraderCanSell(self,trader):
        
        buyersForTradersStock = self.market[trader.stock]['buyers']
        # print 'Here to sell'
        res = 'N'
        if len(buyersForTradersStock) == 0:
            self.market[trader.stock]['sellers'][trader.oid] = {'stockPrice':trader.stockPrice, 'stockQty':trader.stockQty}
             
        else:
            for pid in buyersForTradersStock:
                
                Id = buyersForTradersStock[pid]

                if (trader.stockPrice <= Id['stockPrice']) and (trader.stockQty >0 and pid != trader.oid):
                    # print 'Selling',pid,trader.oid,trader.stockPrice , Id['stockPrice'],trader.stockPrice == Id['stockPrice']
                    if Id['stockQty'] > trader.stockQty :
                        '''
                        Mark trader inactive
                        update Id stock qty
                        add to their matching  
                        update volume of the stock purchase
                        update all stocks value for this stock
                        '''
                        # print 'Greater'
                        # add with whom this transaction made 
                        self.market['allOrders'][trader.oid]['withWhom'].add(pid)
                        self.market['allOrders'][pid]['withWhom'].add(trader.oid)
                         
                        self.market['allOrders'][trader.oid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=trader.stockQty,price=Id['stockPrice'],created_at=trader.creationTime))
                        self.market['allOrders'][pid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=trader.stockQty,price=Id['stockPrice'],created_at=trader.creationTime))

                        remaining = Id['stockQty'] - trader.stockQty
                        self.market['allOrders'][trader.oid]['active'] = False
                        
                        
                        # print trader.stockQty*Id['stockPrice']
                        self.market[trader.stock]['volume']+= trader.stockQty
                        self.market[trader.stock]['allStockPrice']+= trader.stockQty*Id['stockPrice']
                        Id['stockQty'] = remaining
                        self.market['allOrders'][trader.oid]['stockQty'] = 0
                        res='Y'


                    elif Id['stockQty'] == trader.stockQty:
                        '''
                        Mark BOTH of them inactive
                        Remove id from buyers list
                        add to their matching to OrderMatch
                        update volume of the stock purchase
                        update all stocks value for this stock
                        '''
                        # print 'Equal'
                        # add with whom this transaction made 
                        self.market['allOrders'][trader.oid]['withWhom'].add(pid)
                        self.market['allOrders'][pid]['withWhom'].add(trader.oid)
                         
                        self.market['allOrders'][trader.oid]['active'] = False
                        self.market['allOrders'][trader.oid]['active'] = False
                        


                        self.market['allOrders'][pid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=0,price=Id['stockPrice'],created_at=trader.creationTime))
                        self.market['allOrders'][trader.oid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=trader.stockQty,price=Id['stockPrice'],created_at=trader.creationTime))
                        
                        
                        
                        self.market[trader.stock]['volume']+= trader.stockQty
                        self.market[trader.stock]['allStockPrice']+= trader.stockQty*Id['stockPrice']
                        Id['stockQty'] = 0
                        self.market['allOrders'][trader.oid]['stockQty'] = 0
                        self.market[trader.stock]['buyers'].pop(pid)
                        res='Y'
                        # print self.market[trader.stock]['buyers']

                    else:
                        '''
                        Mark Id one Inactive and mark qty 0 
                        remove id from buyers list
                        update traders stock qty
                        add to their matching to OrderMatch
                        update volume of the stock purchase
                        update all stocks value for this stock
                        '''
                        # print 'LessThan'
                        # add with whom this transaction made 
                        self.market['allOrders'][trader.oid]['withWhom'].add(pid)
                        self.market['allOrders'][pid]['withWhom'].add(trader.oid)
                         
                        remaining =  trader.stockQty-Id['stockQty'] 
                        
                        self.market['allOrders'][trader.oid]['active'] = False

                        self.market['allOrders'][pid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=Id['stockQty'],price=Id['stockPrice'],created_at=trader.creationTime))
                        self.market['allOrders'][trader.oid]['matching'].append(stock_exchange_pb2.OrderMatch(quantity=Id['stockQty'],price=Id['stockPrice'],created_at=trader.creationTime))
                       
                        self.market[trader.stock]['volume']+= Id['stockQty']
                        self.market[trader.stock]['allStockPrice']+= Id['stockQty'] * Id['stockPrice']

                        Id['stockQty'] = 0
                        self.market['allOrders'][trader.oid]['stockQty'] = 0
                        
                       # print remaining
                        self.market['allOrders'][trader.oid]['stockQty'] = remaining
                        trader.stockQty = remaining
                        self.market[trader.stock]['buyers'].pop(pid)
                        res='Y'
        if res == 'N':
            self.market[trader.stock]['sellers'][trader.oid] = {'stockPrice':trader.stockPrice, 'stockQty':trader.stockQty}
               
        return res 




    
    def addTraderToMarketForTheirStock(self,trader):
        
        self.market['allOrders'][trader.oid] = vars(trader)
        self.market[trader.stock]['allOrders'][trader.oid] = vars(trader)
        # print trader.purchaseType
        if trader.purchaseType == 'buyer':
            self.checkIfTraderCanBuy(trader)
             
 
                
                # pprint (self.market)
        else:
            self.checkIfTraderCanSell(trader)
            # pprint (self.market)
            
                

        return self.market


    def addNewStockToMarket(self,trader):
        self.market[trader.stock] = {
            'sellers':OrderedDict(),
            'buyers':OrderedDict(),
            'allOrders':{},
            'volume':0,
            'allStockPrice':0
        }
        self.addTraderToMarketForTheirStock(trader)
        return self.market
        
        

    def OrderCreate(self, request, context):
        # print '---------------------------------------------------------------------------'
        coid = self.oid
        rq = request.order
        tr = trader

        # Is the trader seller or buyer 
        if rq.buy:
            newTrader = tr(coid,'buyer',rq.quantity,rq.price,rq.created_at,rq.stock,rq.user)
        else:
            newTrader = tr(coid,'seller',rq.quantity,rq.price,rq.created_at,rq.stock,rq.user)
        

        # Add the trader to userOrder list to kepp track of all the orders made by this user
        if newTrader.name not in self.userOrders:
            self.userOrders[newTrader.name]={newTrader.creationTime : vars(newTrader)}
        else:
            self.userOrders[newTrader.name][newTrader.creationTime] = vars(newTrader)
        

        # Add the trader to market 
        if newTrader.stock not in self.market:
            self.addNewStockToMarket(newTrader)
        else:
            self.addTraderToMarketForTheirStock(newTrader)

        # pprint(self.market)
        newTrader = self.market['allOrders'][newTrader.oid]
        # print newTrader['oid'],newTrader['active'],newTrader['matching']
        self.oid+=1
         

        return stock_exchange_pb2.OrderStatusResponse(order_id=newTrader['oid'],active=newTrader['active'],matches=newTrader['matching'] )
    

    def OrderStatus(self, request, context):  # Complexity O(1)
        trader= self.market['allOrders'][request.order_id]
        return stock_exchange_pb2.OrderStatusResponse(order_id=trader['oid'],active=trader['active'],matches=trader['matching'] )
        
    

    def OrderCancel(self, request, context):  # Complexity  o(1)
        Id = request.order_id
        trader = self.market['allOrders'][Id]
         
        sellersList = self.market[trader['stock']]['sellers']
        buyersList = self.market[trader['stock']]['buyers']
        if Id in sellersList :
            self.market[trader['stock']]['sellers'].pop(Id)
        elif Id in buyersList:
            self.market[trader['stock']]['buyers'].pop(Id)

        return stock_exchange_pb2.OrderStatusResponse(order_id=trader['oid'],active=trader['active'],matches=trader['matching'] )

    def UserOrders(self, request, context): # Complexity O(n)
        user = request.user
        start = request.start_time
        end = request.end_time
        listOfOrders = []
        for order in self.userOrders[user]:
            if order >=start and order<=end:
                trader = self.userOrders[user][order]
                
                listOfOrders.append(stock_exchange_pb2.OrderStatusResponse(order_id=trader['oid'],active=trader['active'],matches=trader['matching'] ))




        return stock_exchange_pb2.MultiOrderStatusResponse(orders=listOfOrders)

    def StockPrice1h(self, request, context):  # Complexity  O(1)
         
        vol = self.market[request.stock]['volume']
        prices = self.market[request.stock]['allStockPrice']
        return stock_exchange_pb2.PriceResponse(price=prices/vol)


    def StockVolume1h(self, request, context):  # Complexity  O(1)
        vol = self.market[request.stock]['volume']
        # pprint (self.market )
        return stock_exchange_pb2.VolumeResponse(volume=vol)


    def OHLC(self, request, context):  #Complexity O(n)
        stock = request.stock
        start = request.start_time
        end = request.end_time
        transactionsMadeWith = set()
        creationTime=[]
        lohi = []
        for order in self.market[stock]['allOrders']:
            order = self.market[stock]['allOrders'][order]
            if len(order['withWhom'])==1:
                        
                        for i in order['withWhom']:
                            if i not in transactionsMadeWith and order['oid'] not in transactionsMadeWith:
                                transactionsMadeWith.add(i)
                                creationTime.append(self.market[stock]['allOrders'][i]['creationTime'])
                        
        # print transactionsMadeWith,creationTime

        # openTime=self.market[stock]['allOrders']['transactionsMadeWith']
        # closeTime=self.market[stock]['allOrders']['transactionsMadeWith']
        open=0
        close=0
        for Id in transactionsMadeWith:
             
            # pprint (self.market[stock]['allOrders'][Id])
            if len(self.market[stock]['allOrders'][Id]['matching']) ==1:
                # print '--,', self.market[stock]['allOrders'][Id]['matching'][0].price
                 lohi.append(self.market[stock]['allOrders'][Id]['matching'][0].price)
            else:
                for match in self.market[stock]['allOrders'][Id]['matching']:
                    lohi.append(match.price)
        
        # print lohi

        creationTime.sort() 

        for ids in self.market['allOrders']:
            # print creationTime[0],creationTime[0] == self.market['allOrders'][ids]['creationTime']
            # print self.market['allOrders'][ids],creationTime[0]
            if creationTime[0] == self.market['allOrders'][ids]['creationTime']:
                open=self.market['allOrders'][ids]['matching'][0].price
            if creationTime[1] == self.market['allOrders'][ids]['creationTime']:
                close=self.market['allOrders'][ids]['matching'][-1].price
        # print open,close



        vol = sum([self.market[stock]['allOrders'][i]['initialStockQty'] for i in  transactionsMadeWith])
      


        # print vol

        return stock_exchange_pb2.OHLCResponse(open=open,high=max(lohi),low=min(lohi),close=close,volume=vol)


    




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stock_exchange_pb2_grpc.add_StockExchangeServicer_to_server(StockExchange(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()