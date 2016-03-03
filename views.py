from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.core import serializers

from datetime import datetime
import json

from .models import ASN, Congestion, Forwarding

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            # return o.isoformat()
            return o.strftime("%Y-%m-%d %H:%M:%S")

        return json.JSONEncoder.default(self, o)

def index(request):
    monitoredAsn = ASN.objects.order_by("number")
    context = {"monitoredAsn": monitoredAsn[:5], "nbMonitoredAsn": len(monitoredAsn)-5}
    return render(request, "reports/index.html", context)

def search(request):
    req = request.GET["asn"]
    reqNumber = -1 
    try:
        if req.startswith("asn"):
            reqNumber = int(req[3:].partition(" ")[0]) 
        elif req.startswith("as"):
            reqNumber = int(req[2:].partition(" ")[0]) 
        else:
            reqNumber = int(req.partition(" ")[0])
    except ValueError:
        return HttpResponseRedirect(reverse("reports:index"))
    
    asn = get_object_or_404(ASN, number=reqNumber)
    return HttpResponseRedirect(reverse("reports:asnDetail", args=(asn.number,)))

def congestionData(request):
    asn = get_object_or_404(ASN, number=request.GET["asn"])
    data = Congestion.objects.filter(asn=asn.number)
    formatedData = {
            "x": list(data.values_list("timeBin", flat=True)),
            "y": list(data.values_list("magnitude", flat=True))
            }
    return JsonResponse(formatedData, encoder=DateTimeEncoder) 

def forwardingData(request):
    asn = get_object_or_404(ASN, number=request.GET["asn"])
    data = Forwarding.objects.filter(asn=asn.number) 
    formatedData = {
            "x": list(data.values_list("timeBin", flat=True)),
            "y": list(data.values_list("magnitude", flat=True))
            }
    return JsonResponse(formatedData, encoder=DateTimeEncoder) 


class ASNDetail(generic.DetailView):
    model = ASN
    # template_name = "reports/asn_detail.html"


class ASNList(generic.ListView):
    model = ASN
    # template_name = "reports/asn_detail.html"


