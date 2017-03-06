# -*- coding: utf-8 -*-

import konan.api.system as system
import konan.api.broker as broker
import testStrategy
import datetime

class system_papar252( system.System ):    
    def run(self):        
        #print( "here")        
        for name, strat in self.strategies.iteritems():            
            print " Executing: ", name, " strategy"
            
            strat.execute()
            



           
papar252 = system_papar252()

papar252.broker = broker.IBBrokerTotal()

if( not papar252.broker.connected() ):
    papar252.broker.connect()


out = papar252.broker.getPositions()


strategies = {'Deltix': testStrategy.deltixStrategy( papar252.broker, 
                                                    papar252.broker) }
papar252.strategies = strategies


date=datetime.date.today()

''' Execution run through '''

# LOAD DATA
WSHdata = papar252.strategies['Deltix'].decision_algorithm.getData(dataType='WSH', date=date)        
earningsCal = papar252.strategies['Deltix'].decision_algorithm.getData(dataType='WSHEarningsCalendar', date=date)        
cutoffCal = papar252.strategies['Deltix'].decision_algorithm.getData(dataType='WSHCutoffCalendar', date=date)

# UPDATE DATA
papar252.strategies['Deltix'].decision_algorithm.constructEarningsCalendar(WSHdata, date)        

test = papar252.strategies['Deltix'].decision_algorithm.earningsCalendar

papar252.strategies['Deltix'].decision_algorithm.generatePositionsForClose(WSHdata, date)

papar252.strategies['Deltix'].decision_algorithm.bulls
papar252.strategies['Deltix'].decision_algorithm.bears = {}

papar252.strategies['Deltix'].decision_algorithm.bulls = {'C': (1,1), 'JPM': (1,1)}
papar252.strategies['Deltix'].decision_algorithm.bears = {'AAPL': (1,1)}

papar252.strategies['Deltix'].enterNewPositions()

papar252.strategies['Deltix'].momentumGuard()

DTtoday = datetime.datetime.combine(date, datetime.time(15,55))

papar252.strategies['Deltix'].hedgePositions(data_time = DTtoday)
        

papar252.broker.disconnect()

''' ------------------ '''
''' Market CLOSE EVENT '''
''' ------------------ '''        

papar252.hedgePositions()
        
papar252.run()

papar252.strategies['Deltix'].momentumGuard()
papar252.strategies['Deltix'].decision_algorithm.bulls
A = papar252.strategies['Deltix'].decision_algorithm.earningsCalendar

papar252.strategies['Deltix'].hedgePositions()


papar252.broker.callback.order_Status
#papar252.exec_broker = broker.IBExecutionBroker()














    
    


