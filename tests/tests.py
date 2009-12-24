#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

Unit tests for national rail api.

Author: Prabhu Subramanian
"""

from nationalrail import nationalrail as nr
import unittest
from datetime import datetime

class tests(unittest.TestCase):
    
    def setUp(self):
        """
        Setup is used for creating a new instance of nationalrail.
        """
        self.rail = nr()
    
    def tearDown(self):
        """
        Make the object None for easy garbage collection.
        """
        self.rail = None
    
    def testRetrieveCRS(self):
        """ Test if we are able to retrieve CRS """
        self.assert_(self.rail.retrieveCRS(station_name="paddington"))
    
    def testDeparture(self):
        """ Test if we are able to retrieve live departures """
        self.assert_(self.rail.departures(crs="PAD", filterCrs="STL"))
    
    def testArrivals(self):
        """ Test if we are able to retrieve live arrivals """
        self.assert_(self.rail.arrivals(crs="STL", filterCrs="HAY"))
    
    def testArrivalsDepartures(self):
        """ Test if we are able to retrieve live arrivals and departures """
        self.assert_(self.rail.arrivalsAndDeparture(crs="PAD"))
    
    def testServiceDetails(self):
        """ Test if we are able to retrieve details about a service """
        data = self.rail.arrivalsAndDeparture(crs="PAD")
        self.assert_(data)
        for service in data.GetArrivalDepartureBoardResult.trainServices.service:
            self.assert_(self.rail.serviceDetails(service.serviceID))
    
    def testJourneyPlanner(self):
        """ Test if journey planner works """
        import random
        dt = datetime.now()
        dt = dt.replace(day=dt.date().day + 2, hour=random.randint(1, 23), minute=0)
        dt1 = dt.replace(day=dt.date().day + 1, hour=random.randint(1, 23), minute=0)
        self.assert_(self.rail.journeyPlanner(fromCrs='PAD', toCrs='HAY', viaCrs='', out_time=dt, ret_time=None))
        self.assert_(self.rail.journeyPlanner(fromCrs='STL', toCrs='RDG', viaCrs='', out_time=dt, ret_time=dt1))
        self.assert_(self.rail.journeyPlanner(fromCrs='PAD', toCrs='SWA', viaCrs='STL', out_time=dt, ret_time=dt1))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
