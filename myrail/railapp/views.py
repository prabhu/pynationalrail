from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

def app_default(request):
    """
    Method which handles the default request.
    """
    username = 'Guest'
    return render_to_response('default.html', locals(),
                              context_instance=RequestContext(request))
