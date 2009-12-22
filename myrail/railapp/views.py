from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from nationalrail import nationalrail as nr

def _defaults():
    """
    Method to return default values to templates.
    """
    username = 'Guest'
    d_fromS = 'London Paddington'
    d_toS = ''
    return locals()

def _redirect_home_with_error(msg):
    """
    Method to redirect to home page with error
    """
    error_msg = msg
    args = locals()
    args.update(_defaults())
    return render_to_response('default.html', args,
                      context_instance=RequestContext(request))

def _getCRS(station):
    """
    Method to get the CRS code for the given station name.
    """
    if not station or len(station.strip()) == 0:
        return None
    crs = None
    rail = nr()
    # Assume CRS if the length is less than 3
    if len(station) == 3:
        crslist = rail.retrieveCRS(crs=station)        
    else:
        crslist = rail.retrieveCRS(station_name=station)
    return crslist
    
def app_default(request):
    """
    Method which handles the default request.
    """
    args = _defaults()
    return render_to_response('default.html', args,
                              context_instance=RequestContext(request))
    
def departures(request):
    """
    Method which handles searches for departures.
    """
    if request.POST:
        p = request.POST
        fromS = p.get('fromS', None)
        toS = p.get('toS', None)
        if not fromS:
            error_msg = "Station name or CRS please"
            return _redirect_home_with_error(error_msg)
        if toS and toS.lower() == 'optional':
            toS = None           
        crslist = _getCRS(fromS)
        if not crslist:
            error_msg = "cannot recognise station name"
            return _redirect_home_with_error(error_msg)

        filterCrslist = _getCRS(toS)
        filterCrs = ""
        sn, crs = crslist[0]
        if filterCrslist:
            sn, filterCrs = filterCrslist[0]
        rail = nr()
        deps = rail.departures(crs=crs, filterCrs=filterCrs)
        services = deps.GetDepartureBoardResult.trainServices.service
        # Force a list if the result has just one service
        if type(services) != type(list):
            services = [services]
        dt = deps.GetDepartureBoardResult.generatedAt.split('T')
        dtime = dt[1].split('.')[0]
        asof = dt[0] + " " + dtime
    return render_to_response('dep.html', {'services' : services, 'crs' : crs, 
                              'asof' : asof},
                              context_instance=RequestContext(request))

def arrivals(request):
    """
    Method which handles searches for arrivals.
    """
    return render_to_response('arr.html', locals(),
                              context_instance=RequestContext(request))

def service(request):
    """
    Method which handles service details request.
    """
    return render_to_response('ser.html', locals(),
                              context_instance=RequestContext(request))

