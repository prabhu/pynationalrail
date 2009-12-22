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
    d_viaS = ''
    return locals()

def _redirect_home_with_error(request, msg):
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
        viaS = p.get('viaS', None)
        if not fromS or fromS.strip() == "":
            error_msg = "Station name or CRS please"
            return _redirect_home_with_error(request, error_msg)
        if viaS and viaS.lower() == 'optional':
            viaS = None           
        crslist = _getCRS(fromS)
        if not crslist:
            error_msg = "cannot recognise station name"
            return _redirect_home_with_error(request, error_msg)
        filterCrslist = _getCRS(viaS)
        
        # If multiple CRS are returned, then redirect to the
        # modified search page that shows list
        if len(crslist) > 1 or (filterCrslist and len(filterCrslist)) > 1:
            return render_to_response('multi.html', {'crslist' : crslist,
                                                    'filterCrslist' : filterCrslist,
                                                    },
                                                    context_instance=RequestContext(request))
        
        filterCrs = ""
        sn, crs = crslist[0]
        if filterCrslist:
            sn, filterCrs = filterCrslist[0]
        rail = nr()
        deps = rail.departures(crs=crs, filterCrs=filterCrs)
        services = deps.GetDepartureBoardResult.trainServices.service
        # Force a list if the result has just one service
        if not isinstance(services, list):
            services = [services]
        dt = deps.GetDepartureBoardResult.generatedAt.split('T')
        dtime = dt[1].split('.')[0]
        asof = dt[0] + " " + dtime
    return render_to_response('dep.html', {'services' : services,
                              'location' : deps.GetDepartureBoardResult.locationName,
                              'crs' : crs, 
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

