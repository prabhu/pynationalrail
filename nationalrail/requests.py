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

# Dict mapping the soap action and the request
SOAPACTION_REQUEST_MAPPING = {
    "GetArrivalBoardRequest" : ARRIVAL_REQUEST,
    "GetDepartureBoardRequest" : DEPARTURE_REQUEST,
    "GetArrivalDepartureBoardRequest" : ARRIVAL_DEPARTURE_REQUEST,
    "GetServiceDetailsRequest" : SERVICE_REQUEST,
}