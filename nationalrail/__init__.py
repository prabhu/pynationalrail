#!/usr/bin/env python
# encoding: utf-8
"""
Python implementation for National Rail api (UK).

Author: Prabhu Subramanian
"""

import sys
import urllib2
from cookielib import CookieJar
import xml.dom.minidom
from xml2dict import fromstring

from settings import *
from requests import *
from crs import *

__VERSION__ = "1.0"

def _doPOST(action=None, extra_headers=None, args=None, url=API_URL, host=HOST):
    body = ACTION_REQUEST_MAPPING.get(action, None)
    if not body:
        print "Unable to find the request data for the action %s" %action
        sys.exit(1)
    body = body % args
    
    headers={
        'Host' : host,
        'Accept-Encoding' : 'deflate',
        'Content-Length' : len(body),
        'User-Agent' : '"Mozilla/5.0 (Windows; U; Windows NT 6.1; pl; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)',
    }
    if extra_headers:
        headers.update(extra_headers)
    
    request = urllib2.Request(url, body, headers)
    response = urllib2.urlopen(request)
    cookies = CookieJar()
    cookies.extract_cookies(response, request)
    cookie_handler= urllib2.HTTPCookieProcessor( cookies )
    redirect_handler= urllib2.HTTPRedirectHandler()
    opener = urllib2.build_opener(redirect_handler, cookie_handler)
    try:
        resp = opener.open(request)
    except urllib2.HTTPError, e:
        print "National Rail servers having some trouble - ", e
    return resp.read()

def doSoapCall(soapAction, args):
    """
    Method to make soap call given the url and proper xml.
    Have to do this, since unfortunately all python soap libs sucks.
    Looked at suds, soappy :(
    @param soapAction: Soap Action to use.
    @param args: Dict to be used for substituting values.
    """
    extra_headers = {
        'Content-Type' : 'application/soap+xml;charset=UTF-8;',
        'SOAPAction' : '"%s/%s"' %(SOAPACTION_URL_PREFIX, soapAction),
    }
    data = _doPOST(action=soapAction, extra_headers=extra_headers, args=args)
    return parseXml(data, soapAction.replace("Request", "Result"))

def doFormSubmit(action=None, args=None):
    """
    Method to submit a form using POST method.
    
    @param action: Action to be used to lookup the request.
    @param args: Dict to be used while constructing values.
    """
    extra_headers = {
        'Content-Type' : 'application/x-www-form-urlencoded',
    }
    data = _doPOST(action=action, extra_headers=extra_headers,
                   args=args, url=args['url'], host=args['host'])
    return data

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
            filterCrs = kwargs.get('filterCrs', None)
            if filterCrs:
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
    
    def journeyPlanner(self, fromCrs=None, toCrs=None,
                       viaCrs='', out_time=None, ret_time=''):
        """
        Method to plan your journey for a different date and time.
        @param fromCrs: From station CRS
        @param toCrs: To station CRS
        @param viaCrs: Via station CRS
        @param out_time: Outward journey time as datetime object.
        @param ret_time: Optional Return journey as datetime object.
        """
        # Outward journey
        ojday = '24/12/2009'
        ojmonth = 'December'
        ojhour = '18'
        ojmin = '00'
        
        # Return journey
        rjday = ''
        rjmonth = ''
        rjhour = ''
        rjmin = ''
        url = JOURNEY_PLANNER_HTTP_URL
        host = JOURNEY_PLANNER_HOST
        response = doFormSubmit("journeyPlanner", locals())
        dep_options, ret_options = _parseJPData(response)
        
def _parseJPData(response):
    """
    Ugly method which parses journey planner html
    and tries to extract useful information. Who said scraping is easy.
    """
    soup = BeautifulSoup(response)
    dep_options = []
    ret_options = []
    soup = soup.find('tr', {"class" : "first"}).parent
    for row in soup.findAll('tr', recursive=False):
        service = {}
        row = row.findNext('td', {'class' : 'leaving'})
        service['leaving'] = row.contents[0].strip()
        service['origin'] = row.findNext('td', {'class' : 'origin'}).contents[0].replace('[', '').strip()
        service['destination'] = row.findNext('td', {'class' : 'destination'}).find('span', {'class' : 'arrow'}).contents[0].replace('[', '').strip()
        row = row.findNext('td', {'class' : 'arriving'})
        service['arriving'] = row.contents[0].replace('[', '').strip()
        row = row.findNext('td')
        service['total_time'] = row.contents[0].strip()
        row = row.findNext('td')
        service['changes_count'] = row.contents[0].strip()
        if service['changes_count'] == '':
            # Changes are involved in this service
            row1 = row.findNext('a')
            service['changes_count'] = row1.contents[0].strip()
            row1 = row1.findNext('tbody')
            changes = []
            for c in row1.findAll('tr', recursive=False):
                row1 = c.findNext('td')
                change = {}
                row1 = row1.findNext('td')
                change['leaving'] = row1.contents[0].strip()
                row1 = row1.findNext('td', {'class' : 'origin'})
                change['origin'] = row1.contents[0].replace('[', '').strip()
                row1 = row1.findNext('td', {'class' : 'destination'}).find('span', {'class' : 'arrow'})
                change['destination'] = row1.contents[0].replace('[', '').strip()
                row1 = row1.findNext('td')
                change['arriving'] = row1.contents[0].strip()
                changes.append(change)
            service['changes'] = changes    
        row = row.findNext('td') # Skip the alert icon
        row = row.findNext('td')
        service['platform'] = row.contents[0].replace('-', '').strip()
        dep_options.append(service)
        print service
    return dep_options, ret_options

def main():
    rail = nationalrail()
    """
    print rail.departures(crs="PAD", filterCrs="STL")
    print rail.arrivals(crs="HAY")
    print rail.arrivalsAndDeparture(crs="PAD")
    print rail.retrieveCRS(station_name="reading")
    """
    rail.journeyPlanner(fromCrs='PAD', toCrs='HAY', viaCrs='STL')

if __name__ == '__main__':
    main()
