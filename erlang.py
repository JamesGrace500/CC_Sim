""" erlang functions in python 
    For first attempt at online planning tool 
"""

import math
import numpy

def agents_req(calls, reporting_period,aht,service_level, service_time):
    """ calculates the minimum agents required to achieve service level

    """
    still_validating = False

    if reporting_period < 5:
        still_validating = True

    if reporting_period > 1500:
        still_validating = True

    if aht < 1:
        still_validating = True

    if aht > 30000:
        still_validating = True

    if service_level < 0.00001:
        still_validating = True

    if service_level > 0.9998:
        still_validating = True

    if service_time < 1:
        still_validating = True

    if service_time > 30000:
        still_validating = True
    
    if still_validating == True:
        return None

    intensity = (calls/(reporting_period * 60)) * aht

    agents = int(intensity)
    #print("agents = " + str(agents))
    
    while servicelevel(calls, reporting_period, aht, service_time, agents) < service_level:
        #print("------")
        #print(" from while loop in Agents_Req function")
        #print("Agents = " + str(agents))
        #print("serviceLevel = " + str(servicelevel(calls, reporting_period, aht, service_time, agents)))
        #print(("Service_level target = " + str(service_level)))
        agents = agents + 1
    
    return agents


def servicelevel(calls, reporting_period, aht, service_time, agents):

    still_validating = False

    if reporting_period < 5:
        still_validating = True
    if reporting_period > 1500:
        still_validating = True
    if aht < 1:
        still_validating = True
    if aht > 30000:
        still_validating = True
    if service_time < 1:
        still_validating = True
    if service_time > 30000:
        still_validating = True
    
    if still_validating == True:
        return None

    intensity = (calls/ (reporting_period * 60)) * aht

    #print("Intensity = " + str(intensity))
    #print("calls = " + str(calls))
    #print(" Reporting Period = " + str(reporting_period))

    #print("------- Service Level calcs -------")
    #print("EXP function - " + str(numpy.exp(-(agents - intensity) * service_time/aht)))
    #print("EXP Functio to go test = || (-("+ str(agents) + " - " + str(intensity) + ") * " + str(service_time) + " / " + str(aht))

    #print("Prob call waits = " + str(prob_calls_waits(calls, reporting_period, aht, agents)))
    servicelevel = 1 - (prob_calls_waits(calls, reporting_period, aht, agents) * numpy.exp(-(agents - intensity) * service_time/aht))


    if servicelevel > 1:
        return 1

    if servicelevel < 0:
        return 0

    return servicelevel


def prob_calls_waits(calls, reporting_period, aht, agents):

    intensity = (calls / (reporting_period * 60)) * aht

    occupancy = intensity / agents

    a_n = 1
    sum_a_k = 0

    #print("sum ak agents = " + str(agents))

    for k in range(agents,1,-1):
        #print("K = " + str(k))
        a_k = a_n * k / intensity
        sum_a_k += + a_k
        a_n = a_k

    #print("Sum a_k = " + str(sum_a_k))
    
    probcallwaits = 1 / (1 + ((1-occupancy) * sum_a_k))

    #print("prob call waits in its function = " + str(probcallwaits))

    if probcallwaits > 1:
       return 1

    if probcallwaits < 0:
        return 0

    return probcallwaits
        

def utilisation(calls, reporting_period, aht, agents):

    intensity = (calls/(reporting_period * 60) * aht)

    util = intensity / agents

    if util < 0:
        return 0
    if util >1:
        return 1
    
    return util