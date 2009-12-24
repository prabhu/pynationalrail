# File containing all the request xml formats.
ARRIVAL_REQUEST = """
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:typ="http://thalesgroup.com/RTTI/2008-02-20/ldb/types">
   <soap:Header/>
   <soap:Body>
      <typ:GetArrivalBoardRequest>
         <typ:numRows>%(numRows)d</typ:numRows>
         <typ:crs>%(crs)s</typ:crs>
         <typ:filterCrs>%(filterCrs)s</typ:filterCrs>
         <typ:filterType>%(filterType)s</typ:filterType>
         <typ:timeOffset>%(timeOffset)d</typ:timeOffset>
      </typ:GetArrivalBoardRequest>
   </soap:Body>
</soap:Envelope>
"""

ARRIVAL_DEPARTURE_REQUEST = """
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:typ="http://thalesgroup.com/RTTI/2008-02-20/ldb/types">
   <soap:Header/>
   <soap:Body>
      <typ:GetArrivalDepartureBoardRequest>
         <typ:numRows>%(numRows)d</typ:numRows>
         <typ:crs>%(crs)s</typ:crs>
         <typ:filterCrs>%(filterCrs)s</typ:filterCrs>
         <typ:filterType>%(filterType)s</typ:filterType>
         <typ:timeOffset>%(timeOffset)d</typ:timeOffset>
      </typ:GetArrivalDepartureBoardRequest>
   </soap:Body>
</soap:Envelope>
"""

DEPARTURE_REQUEST = """
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:typ="http://thalesgroup.com/RTTI/2008-02-20/ldb/types">
   <soap:Header/>
   <soap:Body>
      <typ:GetDepartureBoardRequest>
         <typ:numRows>%(numRows)d</typ:numRows>
         <typ:crs>%(crs)s</typ:crs>
         <typ:filterCrs>%(filterCrs)s</typ:filterCrs>
         <typ:filterType>%(filterType)s</typ:filterType>
         <typ:timeOffset>%(timeOffset)d</typ:timeOffset>
      </typ:GetDepartureBoardRequest>
   </soap:Body>
</soap:Envelope>
"""

SERVICE_REQUEST = """
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:typ="http://thalesgroup.com/RTTI/2007-10-10/ldb/types">
   <soap:Header/>
   <soap:Body>
      <typ:GetServiceDetailsRequest>
         <typ:serviceID>%(serviceID)s</typ:serviceID>
      </typ:GetServiceDetailsRequest>
   </soap:Body>
</soap:Envelope>
"""

JOURNEY_PLANNER_HTTP_REQUEST = {
    'from.searchTerm' : '%(fromCrs)s',
    'to.searchTerm' : '%(toCrs)s',
    'jpState' : '%(jpstate)s',
    'commandName' : 'journeyPlannerCommand',
    'timeOfOutwardJourney.arrivalOrDeparture' : 'DEPART',
    'timeOfOutwardJourney.monthDay' : '%(ojday)s',
    'timeOfOutwardJourney.hour' : '%(ojhour)s',
    'timeOfOutwardJourney.minute' : '%(ojmin)s',
    'timeOfReturnJourney.arrivalOrDeparture' : 'DEPART',
    'timeOfReturnJourney.monthDay' : '%(rjday)s',
    'timeOfReturnJourney.hour' : '%(rjhour)s',
    'timeOfReturnJourney.minute' : '%(rjmin)s',
    'viaMode' : 'VIA',
    'via.searchTerm' : '%(viaCrs)s',
    'directTrains' : 'false',
    '_directTrains' : 'on',
    'offSetOption' : '0',
    '_reduceTransfers' : 'on',
    'operatorMode' : 'SHOW',
    'operator.code' : '',
    '_lookForSleeper' : 'on',
    '_includeOvertakenTrains' : 'on',
    'buttonPressed' : 'go',
}

# Month ojmonth, rjmonth is specified in full text eg, December.
JOURNEY_PLANNER_IPHONE_REQUEST = {
    'from.searchTerm' : '%(fromCrs)s',
    'to.searchTerm' : '%(toCrs)s',
    'via.searchTerm' : '%(viaCrs)s',
    'timeOfOutwardJourney.day' : '%(ojday)s',
    'timeOfOutwardJourney.month' : '%(ojmonth)s',
    'timeOfOutwardJourney.hour' : '%(ojhour)s',
    'timeOfOutwardJourney.minute' : '%(ojmin)s',
    'timeOfOutwardJourney.arrivalOrDeparture' : 'DEPART',
    'timeOfOutwardJourney.firstOrLast' : 'FIRST',
    'timeOfReturnJourney.day' : '%(rjday)s',
    'timeOfReturnJourney.month' : '%(rjmonth)s',
    'timeOfReturnJourney.hour' : '%(rjhour)s',
    'timeOfReturnJourney.minute' : '%(rjmin)s',
    'timeOfReturnJourney.arrivalOrDeparture' : 'DEPART',
    'timeOfReturnJourney.firstOrLast' : 'FIRST',
    'maxChanges' : 'true',
    'planjourney' : 'SEARCH',
}

JOURNEY_TIME_TYPE = {'DEPART' : 'Leaving',
                     'ARRIVE' : 'Arriving',
                     'FIRST' : 'First Train',
                     'LAST' : 'Last Train'}

VIA_MODES = {'VIA' : 'Travel Via',
             'AVOID' : 'Avoid',
             'CHANGE' : 'Include Interchange',
             'DONT_CHANGE' : 'Exclude Interchange',
            }

# Dict mapping the action and the request
ACTION_REQUEST_MAPPING = {
    "GetArrivalBoardRequest" : ARRIVAL_REQUEST,
    "GetDepartureBoardRequest" : DEPARTURE_REQUEST,
    "GetArrivalDepartureBoardRequest" : ARRIVAL_DEPARTURE_REQUEST,
    "GetServiceDetailsRequest" : SERVICE_REQUEST,
    "journeyPlanner" : '&'.join([k+'='+v for k,v in JOURNEY_PLANNER_HTTP_REQUEST.items()]),
}

