# bring in the imports 
import simpy 
import random



# This the car, in the new model it will be a call
def car(env, name, bcs, driving_time, charge_duration):
    #Simulate driving to the station
    yield env.timeout(driving_time)

    print('%s arriving at %d' % (name, env.now))
    with bcs.request() as req:
        yield req

        #charge the battery 
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))



env = simpy.Environment() # This is the sim enviroment that will be live
agents = simpy.Resource(env, capacity=500) # specify the resource, this will be agent


#Since car is call, then the i will be number of calls that happen instantly, this will be random over the interval period?
for i in range(1000):
    timeEntered = random.randrange(0,900)
    print('random range %s' % (timeEntered))
    env.process(car(env, 'Car %d' % i, agents, timeEntered, 450))

# this will kick off the process
env.run()
