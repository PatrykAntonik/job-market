from rest_framework.decorators import api_view
from rest_framework.response import Response

from JobApp.serializers import *


@api_view(["GET"])
def getEmployers(request):
    employers = Employer.objects.all()
    serializer = EmployerSerializer(employers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getEmployer(request, pk):
    try:
        employer = Employer.objects.get(id=pk)
        serializer = EmployerSerializer(employer, many=False)
        return Response(serializer.data)
    except Employer.DoesNotExist:
        return Response({"message": "Employer not found"}, status=404)


@api_view(["GET"])
def getEmployerLocation(request, pk):
    if not Employer.objects.filter(id=pk).exists():
        return Response({"message": "Employer not found."}, status=404)
    employer_locations = EmployerLocation.objects.filter(employer_id=pk)
    if employer_locations.exists():
        serializer = EmployerLocationSerializer(employer_locations, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "No locations found for this employer"}, status=404)
