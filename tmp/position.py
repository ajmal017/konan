# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 17:31:39 2017

@author: Ray
"""


# ------------------------------
# Position container
# ------------------------------

class position_(object):
    
    def __init__ (self, expiry=0, ID="", age=-1, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=0):

        self.open_date =open_date
        self.wealth = wealth
        self.trade_type = trade_type  # long/ short
        self.entry_price = entry_price
        self.age = -1 # When this reaches 5 it is a signal to close all positions.
        self.expiration = expiry
        self.ID = ID

        self.today_price = 0 
        self.prev_price = 0 
        self.today_PL = 0
                

        if( num_units == 0 and self.wealth!=0):
            self.num_units = self.trade_type * self.wealth /  self.entry_price        
                
        if( num_units !=0 and self.wealth==0 ):
            self.wealth  = self.trade_type * self.num_units* self.entry_price
            
        if( num_units !=0 and self.wealth!=0 ):
            raise "Specify either the number of units or investment value"

      
    def updatePosition( self, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=np.nan ):
        
        self.open_date =open_date
        self.wealth = wealth
        self.trade_type = trade_type  # long/ short
        self.entry_price = entry_price
        
        if(num_units!= np.nan):
            self.num_units = num_units        

        
    def setExpiration(self, T):
        self.expiration=T
        
        
    def setTodayPrice(self, today_price):
        self.today_price = today_price        
        
    def setTodayPL(self, today_PL):
        self.today_PL = today_PL
        

# ------------------------------
# Position container for stock
# ------------------------------
class positionStk(position_):
    
    def __init__(self, expiry=0, ID="", age=-1, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=np.nan):
        
        position_.__init__ (self, 
                            expiry=expiry, 
                            age=age, 
                            wealth=wealth, 
                            entry_price=entry_price, 
                            open_date=open_date,  
                            trade_type=trade_type,                            
                            ID = ID
                            )


# ------------------------------
# Position container for futures
# ------------------------------
class positionFutures(position_):
    
    def __init__(self, expiry=0, ID="", age=-1, wealth=1, entry_price=1, open_date=None, trade_type=1, num_units=np.nan, mult=1 ):
        
        position_.__init__ (self, 
                            expiry=expiry, 
                            age=age, 
                            wealth=wealth, 
                            entry_price=entry_price, 
                            open_date=open_date,  
                            trade_type=trade_type,    
                            ID = ID,
                            num_units=num_units
                            )
        
        self.cont_multiplier = mult
                            
        
    def setMultiplier(self, mult):
        self.cont_multiplier = mult
        


        
