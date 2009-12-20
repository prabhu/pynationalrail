#!/usr/bin/env python
# encoding: utf-8
"""
nationalrail.py

Python implementation for National Rail api (UK).
Author: Prabhu Subramanian
"""
__VERSION__ = "1.0"

import sys
import httplib, urllib

from settings import *
from requests import *

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
        'SOAPAction' : '"%s/%s"' %(ACTION_URL_PREFIX, soapAction),
    }
    hc.request ('POST', API_URL, body=xml, headers=headers)
    resp = hc.getresponse()
    data = resp.read()
    if resp.status != 200:
        raise ValueError('Unable to receive expected data : %s, %s' % (resp.status, resp.reason))
    return data
        
class nationalrail:

    # Decorators
    def mandatory(api):
        """
        Decorator to check for mandatory parameters
        """
        def func(*args, **kwargs):
            print kwargs
            api(*args, **kwargs)
        return func
        
    def __init__(self):
        """
        Constructor. Initialises required values like the host, api url.
        """
        pass
        
    #@mandatory
    #@valid_crs
    def departures(self, numRows=5, crs="", filterCrs="", filterType="to", timeOffset=0):
        """
        Method to retrieve the departure details from a station specified by crs.
        @param numRows: Number of rows to be returned
        @param crs: CRS code of the station.
        @param filterCrs: CRS code of an intermediate station to filter the result.
        @param filterType: To indicate if the filterCrs is a from or to station. Default to.
        @param timeOffset: Time offset in 
        """
        result = doSoapCall("GetDepartureBoardRequest", locals()) 
        print result
            
def main():
    rail = nationalrail()
    rail.departures(crs="STL")
    
if __name__ == '__main__':
    main()
