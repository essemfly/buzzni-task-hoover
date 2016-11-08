from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from hoover.models import Hoover, Review
from hoover.serializers import HooverSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def hoover_list(request):
    """
    List all code hoovers, or create a new hoover.
    """
    if request.method == 'GET':
        hoovers = Hoover.objects.all()
        serializer = HooverSerializer(hoovers, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HooverSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def hoover_detail(request, pk):
    """
    Retrieve, update or delete a code hoover.
    """
    try:
        hoover = Hoover.objects.get(pk=pk)
    except Hoover.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HooverSerializer(hoover)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HooverSerializer(hoover, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        hoover.delete()
        return HttpResponse(status=204)
