#!/usr/bin/env python
# encoding: utf-8
"""
nationalrail.py

Python implementation for National Rail api (UK).
Author: Prabhu Subramanian
"""

import sys
import httplib, urllib
import xml.dom.minidom
from xml2dict import fromstring

from settings import *
from requests import *
from crs import *

def doSoapCall(soapAction, args):
    """
    Method to make soap call given the url and proper xml.
    Have to do this, since unfortunately all python soap libs sucks.
    Looked at suds, soappy :(
    @param soapAction: Soap Action to use.
    @param host: National rail server host.
    @param url: URL to use for this soap action.
    @param xml: Request xml to be sent to the server.
    """
    hc = httplib.HTTPConnection(HOST)
    xml = SOAPACTION_REQUEST_MAPPING.get(soapAction, None)
    if not xml:
        print "Unable to find the request xml for the action %s" %soapAction
        sys.exit(1)
    xml = xml % args
    headers={
        'Host' : HOST,
        'Accept-Encoding' : 'gzip,deflate',
        'Content-Type' : 'application/soap+xml;charset=UTF-8;',
        'Content-Length' : len(xml),
        'User-Agent' : 'Python National Rail - How are you?',
        'SOAPAction' : '"%s/%s"' %(SOAPACTION_URL_PREFIX, soapAction),
    }
    hc.request ('POST', API_URL, body=xml, headers=headers)
    resp = hc.getresponse()
    data = resp.read()
    if resp.status != 200:
        print "National rail servers having some trouble - ", resp.status, resp.reason
        raise ValueError('Unable to receive expected data : %s, %s' % (resp.status, resp.reason))
    return parseXml(data, soapAction.replace("Request", "Result"))
        
def parseXml(ixml, tagName):
    """
    Method to parse the given xml for the given id and return the result as object
    minidom is used here.
    @param xml: Xml to parse
    @param tagName: Tag name to look for in the xml
    """
    doc = xml.dom.minidom.parseString(ixml)
    response = doc.getElementsByTagName(tagName)[0].toxml()
    return fromstring(response)
    
class nationalrail:

    # Decorators
    def mandatory(api):
        """
        Decorator to check for mandatory parameters
        """
        def func(*args, **kwargs):
            crs = kwargs.get('crs', None)
            if not crs or len(crs) != 3:
                print "CRS is mandatory for %s call" %api.__name__
                sys.exit(1)
            # Capitalise CRS.
            kwargs['crs'] = crs.upper()
            kwargs['filterCrs'] = kwargs['filterCrs'].upper() 
            return api(*args, **kwargs)
        return func
        
    def __init__(self):
        """
        Constructor.
        """
        pass
        
    @mandatory
    def departures(self, numRows=5, crs="", filterCrs="", filterType="to", timeOffset=0):
        """
        Method to retrieve the departure details from a station specified by crs.
        @param numRows: Number of rows to be returned
        @param crs: CRS code of the station.
        @param filterCrs: CRS code of an intermediate station to filter the result.
        @param filterType: To indicate if the filterCrs is a from or to station. Default to.
        @param timeOffset: Time offset in mins. Max 90 I guess.
        
        @return JSON response.
        """
        return doSoapCall("GetDepartureBoardRequest", locals())

    @mandatory
    def arrivals(self, numRows=5, crs="", filterCrs="", filterType="to", timeOffset=0):
        """
        Method to retrieve the arrival details to a station specified by crs.
        @param numRows: Number of rows to be returned
        @param crs: CRS code of the station.
        @param filterCrs: CRS code of an intermediate station to filter the result.
        @param filterType: To indicate if the filterCrs is a from or to station. Default to.
        @param timeOffset: Time offset in mins.
        
        @return JSON response.
        """
        return doSoapCall("GetArrivalBoardRequest", locals())

    @mandatory
    def arrivalsAndDeparture(self, numRows=5, crs="", filterCrs="", filterType="to", timeOffset=0):
        """
        Method to retrieve the arrival and departure details of a station specified by crs.
        @param numRows: Number of rows to be returned
        @param crs: CRS code of the station.
        @param filterCrs: CRS code of an intermediate station to filter the result.
        @param filterType: To indicate if the filterCrs is a from or to station. Default to.
        @param timeOffset: Time offset in mins.
        
        @return JSON response.
        """
        return doSoapCall("GetArrivalDepartureBoardRequest", locals())
    
    def serviceDetails(self, serviceID):
        """
        Method to retrieve details about a particular service.
        @param serviceID: Service ID (Identifier representing a train service) obtained from other api.
        
        @return JSON response.
        """
        return doSoapCall("GetServiceDetailsRequest", locals())
    
    def retrieveCRS(self, station_name=None, crs=None):
        """
        Method to retrieve CRS for a station name.
        @param station_name: Station Name to be used.
        """
        res = getCRS(station_name=station_name, crs=crs)
        return [(sc.capitalize(), crs) for (sc,crs) in res]
        
def main():
    rail = nationalrail()
    print rail.departures(crs="PAD", filterCrs="STL")
    print rail.arrivals(crs="HAY")
    print rail.arrivalsAndDeparture(crs="PAD")
    print rail.retrieveCRS(station_name="reading")
    
if __name__ == '__main__':
    main()
