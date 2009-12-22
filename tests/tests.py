#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

Unit tests for national rail api.

Author: Prabhu Subramanian
"""

from nationalrail import nationalrail as nr
import unittest

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
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
