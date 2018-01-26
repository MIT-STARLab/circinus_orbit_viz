#! /usr/bin/env python

##
# Crux example component
# @author Patrick Kage
# 
# This is an example single-file simulation component
# this is using an example version of the crux client library
# Note that the API may change in future!

# import the crux libraries
from crux.client import CruxClient as Crux
from yourcode import Simulation, SimulationException

if __name__ == "__main__":
    # initialize everything
    cc = Crux('crux.json')

    # connect to the crux backend (sends the description files to the backend)
    cc.connect()

    while True:
        # wait for the backend to send some data for processing
        data, config, done = cc.wait()

        if done:
            break

        try:
            # create the simulation from the configuration sent over
            sim = Simulation(**config)

            # do some operation to the data
            output = sim.do_some_simulation(data)

            # output that data back to the backend
            cc.output(output)
        except SimulationException ex:
            # handle an error state gracefully
            cc.fail(ex.message)
        except:
            # hard failure
            cc.fail()
    # do cleanup here if necessary
