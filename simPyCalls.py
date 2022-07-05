import numpy as np 
import pandas as pd
import simpy
import random 
from datetime import datetime
import erlang

df1 = pd.read_excel('profiles.xlsx','intraday',index_col=0)
df2 = pd.read_excel('profiles.xlsx','intraweek')
df3 = pd.read_excel('profiles.xlsx','weeklyForecast', index_col = 0)

# CORE METRICS TO BE ACHIVED 
PCA = 0.9
SERVICE_TIME = 20
SLA = 0.8
OCCTARGET = 0.85
SHRINK = 0.25

# creating a blank DataFrame but organised to what I want to make happen
dfWeek = pd.DataFrame(columns=('interval','monday','tuesday','wednesday','thursday','friday'))


print('weekly calls looks like:')
for index, row in df3.iterrows():
    week = index.date()
    callFcast = row['calls_offered']
    mondayVol = row['calls_offered'] * df2.iloc[0]['Monday']
    tuesdayVol = row['calls_offered'] * df2.iloc[0]['Tuesday']
    wednesdayVol = row['calls_offered'] * df2.iloc[0]['Wednesday']
    thursdayVol = row['calls_offered'] * df2.iloc[0]['Thursday']
    fridaVol = row['calls_offered'] * df2.iloc[0]['Friday']
    ahtFcast = row['calls_AHT']
    

    for index, row in df1.iterrows():
        new_row = {
            'week':week,
            'interval' : index, 
            'monday':mondayVol * df1.loc[index]['Monday'],
            'tuesday':tuesdayVol * df1.loc[index]['Tuesday'],
            'wednesday':wednesdayVol * df1.loc[index]['Wednesday'],
            'thursday':thursdayVol * df1.loc[index]['Thursday'],
            'friday':fridaVol * df1.loc[index]['Friday'],
            'aht':ahtFcast,
            'monErlang':erlang.agents_req(mondayVol * df1.loc[index]['Monday'],15,ahtFcast,SLA,SERVICE_TIME),
            'tueErlang':erlang.agents_req(tuesdayVol * df1.loc[index]['Tuesday'],15,ahtFcast,SLA,SERVICE_TIME),
            'wedErlang':erlang.agents_req(wednesdayVol * df1.loc[index]['Wednesday'],15,ahtFcast,SLA,SERVICE_TIME),
            'thuErlang':erlang.agents_req(thursdayVol * df1.loc[index]['Thursday'],15,ahtFcast,SLA,SERVICE_TIME),
            'friErlang':erlang.agents_req(fridaVol * df1.loc[index]['Friday'],15,ahtFcast,SLA,SERVICE_TIME)
        }

    dfNewRow = pd.DataFrame.from_records([new_row])
    dfWeek = pd.concat([dfWeek, dfNewRow])
    dfWeek.set_index('interval')
    
    print ('week:%s || calls: %d || aht:  %r' % (week, callFcast, ahtFcast))


# here is where we will try the sequence process

# needs simple df with interval and call volume, then the seconds avail in an interval
def convertToSeconds(df, seconds):
    baseList = dict()
    intCount = 1
    x = 0
    for interval in df['interval'].unique():
        baseSecond = (seconds * intCount) - seconds
        maxSecond = (seconds * intCount) -1
      
        maxCalls = int(round(float(df['day'][df['interval'] == interval] +1)))
        for call in range(1,maxCalls):
            secondRec = random.randrange(baseSecond, maxSecond)
            if secondRec in baseList:
                baseList[secondRec] = baseList[secondRec] + 1
            else:
                baseList[secondRec] = 1

                
                

    return dict(sorted(baseList.items()))
        

# This is composed of three elements 
# A call is received at a certain second in a day, in block of 15 minutes as the common forecasting interval 
# A call is then placed in the queue, where it will either wait or abandon until it is answered
# An agent will deal with the call but  they may also go do strange things, close calls early, go on break or toilet etc

# *** THIS CONVERTS IT TO REAL TIME SINCE THERE IS HUMAN INTERACTION ***

from functools import partial, wraps

def patch_resource(resource, pre=None, post=None):
     """Patch *resource* so that it calls the callable *pre* before each
     put/get/request/release operation and the callable *post* after each
     operation.  The only argument to these functions is the resource
     instance.
     """
     def get_wrapper(func):
         # Generate a wrapper for put/get/request/release
         @wraps(func)
         def wrapper(*args, **kwargs):
             # This is the actual wrapper
             # Call "pre" callback
             if pre:
                 pre(resource)

             # Perform actual operation
             ret = func(*args, **kwargs)

             # Call "post" callback
             if post:
                 post(resource)

             return ret
         return wrapper

     # Replace the original operations with our wrapper
     for name in ['put', 'get', 'request', 'release']:
         if hasattr(resource, name):
             setattr(resource, name, get_wrapper(getattr(resource, name)))

def monitor(data, resource):
    """This is our monitoring callback."""
    item = (
        resource._env.now,  # The current simulation time
        resource.count,  # The number of users
        len(resource.queue),  # The number of queued processes
    )
    data.append(item)



def Call(env, callID, agents, arrival_time, call_duration):    
  

    yield env.timeout(arrival_time)

    with agents.request() as req:
        yield req

        yield env.timeout(call_duration)

        
        
        
        

env = simpy.Environment() # This is the sim enviroment that will be live
agents = simpy.Resource(env, capacity=500) # specify the resource, this will be agent

#I need to order the calls of the day into the correct order of arrival and then feed them through in sequential order

#Since car is call, then the i will be number of calls that happen instantly, this will be random over the interval period?

data = []
monitor = partial(monitor, data)
patch_resource(agents, post=monitor) # patches (only) this resource instance


DAYS_OF_WEEK = ['monday','tuesday','wednesday','thursday','friday']
for week in dfWeek['week'].unique():
    for day in DAYS_OF_WEEK:        
        dfSample =  dfWeek[['interval',day]][dfWeek['week'] == week]
        dfSample.rename(columns={ dfSample.columns[1]: "day" }, inplace = True)
        print(dfSample.sum())
        sample = convertToSeconds(dfSample, 900)

        for key,value in sample.items(): 
            callID = 0
            for call in range(value):
                arrival_time = key
                callID = callID + 1
                callAHT = int(450 * (1-random.randrange(-10,10)/100))
                env.process(Call(env, callID, agents, arrival_time, callAHT))

        # this will kick off the process
        env.run()
        print(week)
        print(day)
        print(data)
        print('Total calls:  {b1}'.format(b1 = dfSample['day'].sum()))
        data = []
