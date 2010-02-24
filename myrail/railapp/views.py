from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import re
from common.utils import create_user, debugger
from nationalrail import nationalrail as nr
from models import Favorite
from common.middleware import get_current_user

LAST_SEARCH_COOKIE = "lastSearch"
DEPARTURES = 'Departures'

def _defaults(request):
    """
    Method to return default values to templates.
    """
    loggedIn = _checkLoggedIn(request)
    username = 'Guest'
    favs = None
    if loggedIn:
        user = request.user
        username = request.user.username
        favs = Favorite.objects.filter(user=user)[:6]
    d_fromS = 'Paddington'
    d_viaS = ''
    if LAST_SEARCH_COOKIE in request.COOKIES:
        if request.COOKIES[LAST_SEARCH_COOKIE]:
            d_fromS, d_viaS = request.COOKIES[LAST_SEARCH_COOKIE].split("|")
    return locals()

def _checkLoggedIn(request):
    """
    Method to determine if the user is logged in.
    """
    loggedIn = False
    if getattr(request, 'user'):
        user = request.user
        if not user.is_anonymous():
            loggedIn = True
    return loggedIn

def _redirect_home_with_msg(request, msg):
    """
    Method to redirect to home page with error
    """
    error_msg = msg
    args = locals()
    args.update(_defaults(request))
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
        station = _expandCommon(station)
        crslist = rail.retrieveCRS(station_name=station)
    return crslist

def _expandCommon(station):
    """
    Method to expand common acronyms like north, south
    """
    REP = {
        '[Nn]' : 'north',
        '[Ss]' : 'south',
        '[Ee]' : 'east',
        '[Ww]' : 'west',
    }
    for k,v in REP.items():
        station = re.sub('^' + k + '\s', v + ' ', station)
        station = re.sub('\s' + k + '$', ' ' + v, station)
    return station

@debugger
def app_default(request):
    """
    Method which handles the default request.
    """
    args = _defaults(request)
    return render_to_response('default.html', args,
                              context_instance=RequestContext(request))

@debugger
def departures(request):
    """
    Method which handles searches for departures
        - supports both GET and POST
    """
    if request.POST:
        p = request.POST
    if request.GET:
        p = request.GET
    fromS = p.get('fromS', None)
    viaS = p.get('viaS', None)
    return _handleDepartures(request, fromS=fromS, viaS=viaS)

def _handleDepartures(request, fromS=None, viaS=None, favId=None):
    """
    Re-usable method which handles departure requests.
    This can be invoked from other places like favorites.
    """
    if not fromS or fromS.strip() == "":
        error_msg = "Station name or CRS please"
        return _redirect_home_with_msg(request, error_msg)
    if viaS and viaS.lower() == 'optional':
        viaS = None
    crslist = _getCRS(fromS)
    if not crslist:
        error_msg = "cannot recognise station name"
        return _redirect_home_with_msg(request, error_msg)
    filterCrslist = _getCRS(viaS)
    
    # If multiple CRS are returned, then redirect to the
    # modified search page that shows list
    if len(crslist) > 1 or (filterCrslist and len(filterCrslist)) > 1:
        args = {'crslist' : crslist,
                'filterCrslist' : filterCrslist,
                }
        args.update(_defaults(request))
        return render_to_response('multi.html', args,
                                 context_instance=RequestContext(request))
    filterCrs = ""
    fsn, crs = crslist[0]
    vsn = ''
    if filterCrslist:
        vsn, filterCrs = filterCrslist[0]
    rail = nr()
    deps = rail.departures(crs=crs, filterCrs=filterCrs)
    
    services = None
    # Are there any services running?
    if deps.GetDepartureBoardResult.get('trainServices'):
        services = deps.GetDepartureBoardResult.trainServices.get('service', None)
    platformAvailable = deps.GetDepartureBoardResult.get('platformAvailable', None)
    # Force a list if the result has just one service
    if services and not isinstance(services, list):
        services = [services]
    dt = deps.GetDepartureBoardResult.generatedAt.split('T')
    dtime = dt[1].split('.')[0]
    asof = dt[0] + " " + dtime
    location = deps.GetDepartureBoardResult.locationName
    # Build next service dict
    nextService = {}
    prevService = None
    if services:
        for service in services:
            if prevService:
                nextService[prevService] = service.serviceID
            prevService = service.serviceID        
    response = render_to_response('dep.html', {'services' : services,
                          'nextService' : nextService,
                          'location' : location,
                          'crs' : crs,
                          'filterCrs' : filterCrs,
                          'platformAvailable' : platformAvailable,
                          'favId' : favId,
                          'asof' : asof},
                          context_instance=RequestContext(request))
    response.set_cookie(LAST_SEARCH_COOKIE, fsn + "|" + vsn)
    return response

def arrivals(request):
    """
    Method which handles searches for arrivals.
    """
    return render_to_response('arr.html', locals(),
                              context_instance=RequestContext(request))

@debugger
def service(request):
    """
    Method which handles service details request.
    """
    if request.GET:
        p = request.GET
        sid = p.get('id', None)
        crs = p.get('crs', None)
        nid = p.get('nid', None)
        if not sid:
            error_msg = "Invalid train details. Start again"
            return _redirect_home_with_msg(request, error_msg)
        rail = nr()
        resp = rail.serviceDetails(sid)
        if not resp:
            return render_to_response('ser.html', {'error' : true}, context_instance=RequestContext(request))
            
        sdetails = resp.GetServiceDetailsResult
        dt = sdetails.generatedAt.split('T')
        dtime = dt[1].split('.')[0]
        asof = dt[0] + " " + dtime
        plat = sdetails.get('platform', None)
        isCancelled = sdetails.get('isCancelled', None)
        disruptionReason = sdetails.get('disruptionReason', None)
        eta = sdetails.get('eta', None)
        etd = sdetails.get('etd', None)
        return render_to_response('ser.html', {'sdetails' : sdetails,
                              'asof' : asof,
                              'plat' : plat,
                              'isCancelled' : isCancelled,
                              'disruptionReason' : disruptionReason,
                              'eta' : eta,
                              'etd' : etd,
                              'id' : sid,
                              'crs' : crs,
                              'nid' : nid,
                              },
                              context_instance=RequestContext(request))

@debugger
def favorites(request):
    """
    Method which handles favorites request
    """
    if request.GET:
        g = request.GET
        action = g.get('a', None)
        fromS = g.get('fromS', None)
        viaS = g.get('viaS', None)
        ftype = g.get('type', DEPARTURES)
        
        # Check if we are trying to delete an existing favorite
        if action == 'd':
            id = g.get('id', None)
            if not id:
                return _redirect_home_with_msg(request, "ID missing. Cannot delete favorite.")
            try:
                fav = Favorite.objects.get(id=id, user=request.user)
                fav.delete()
                return _redirect_home_with_msg(request, "Favorite removed successfully.")
            except Favorite.DoesNotExist:
                return _redirect_home_with_msg(request, "Invalid favorite id.")
        
        if not fromS:
            return _redirect_home_with_msg(request, "location missing. cannot save favorite!")
        
        crslist = _getCRS(fromS)
        filterCrslist = _getCRS(viaS)
        if not crslist:
            return _redirect_home_with_msg(request, "Invalid station name")
        if len(crslist) > 1 or (filterCrslist and len(filterCrslist) > 1):
            return _redirect_home_with_msg(request, "Multiple station names retrieved.")
        
        fsn, crs = crslist[0]
        vsn = filterCrs = None
        if filterCrslist:
            vsn, filterCrs = filterCrslist[0]
        
        # Construct a good favorite name
        fname = fsn + ' ' + ftype
        desc = ''
        if vsn:
            desc = 'Via ' + vsn
        
        # See if the user is logged in.
        loggedIn = _checkLoggedIn(request)
        return render_to_response('fav.html', {'fname' : fname,
                                'fromS' : fromS,
                                'viaS' : viaS,
                                'ftype' : ftype,
                                'desc' : desc,
                                'loggedIn' : loggedIn,
                                },
                                context_instance=RequestContext(request))
    
    if request.POST:
        p = request.POST
        fromS = p.get('fromS', None)
        viaS = p.get('viaS', None)
        ftype = p.get('type', 'Departures')
        fname = p.get('fname', None)
        desc = p.get('desc', '')
        if not fname or not fromS:
            return _redirect_home_with_msg(request, "Missing values. Favorite not saved.")
        
        # Retrieve or create the user.
        username = p.get('username', None)
        password = p.get('password', None)
        loggedIn = _checkLoggedIn(request)
        
        if not loggedIn:
            if not username or not password or username.strip() == '' or password.strip() == '':
                return _redirect_home_with_msg(request, "Cannot save favorite without registering.")
        
        user = None
        if getattr(request, 'user'):
            user = request.user
        if not user or user.is_anonymous():
            try:
                user = User.objects.get(username=username, password=password)
            except User.DoesNotExist:
                # Create the user and login
                user = create_user(request, username, password)
                user = authenticate(username=username, password=password)
                login(request, user)
        
        # Go ahead and save the favorite
        fav = Favorite(user=user, fname=fname, desc=desc,
                       ftype=ftype, fromS=fromS, viaS=viaS)
        fav.save()
        return _redirect_home_with_msg(request, "Favorite saved.")

def recent(request):
    """
    Method which handles recent search requests.
    """
    pass

def favorites_search(request):
    """
    Method which handles favorite search.
    """
    if request.GET:
        g = request.GET
        id = g.get('id', None)
        user = request.user
        if not id:
            return _redirect_home_with_msg(request, "Invalid favorite chosen")
        if not user or user.is_anonymous():
            return _redirect_home_with_msg(request, "You need to login first!")
        try:
            fav = Favorite.objects.get(user=user, id=id)
        except Favorite.DoesNotExist:
            return _redirect_home_with_msg(request, "Invalid favorite chosen")
        ftype, fromS, viaS = fav.ftype, fav.fromS, fav.viaS
        if ftype == DEPARTURES:
            return _handleDepartures(request, fromS=fromS, viaS=viaS, favId=id)

def loginAction(request):
    """
    Method to handle login/register request.
    """
    if request.POST:
        p = request.POST
        # Retrieve or create the user.
        username = p.get('username', None)
        password = p.get('password', None)
        if not username or not password:
            return _redirect_home_with_msg(request, "Need username and password.")
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            # Create the user and login
            user = create_user(request, username, password)
        user = authenticate(username=username, password=password)
        login(request, user)
        return _redirect_home_with_msg(request, "Welcome back!")

def journeyPlanner(request):
    """
    Method to handle journey planner requests. Advanced button in home page.
    """
    pass
    