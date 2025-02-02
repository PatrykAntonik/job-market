from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from JobApp.serializers import *


@api_view(['GET'])
def getCountries(request):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getIndustries(request):
    industries = Industry.objects.all()
    serializer = IndustrySerializer(industries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getIndustry(request, pk):
    try:
        industry = Industry.objects.get(id=pk)
        serializer = IndustrySerializer(industry, many=False)
        return Response(serializer.data)
    except Industry.DoesNotExist:
        return Response({'message': 'Industry not found'}, status=404)


@api_view(['GET'])
def getEmployers(request):
    employers = Employer.objects.all()
    serializer = EmployerSerializer(employers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getEmployer(request, pk):
    try:
        employer = Employer.objects.get(id=pk)
        serializer = EmployerSerializer(employer, many=False)
        return Response(serializer.data)
    except Employer.DoesNotExist:
        return Response({'message': 'Employer not found'}, status=404)


@api_view(['GET'])
def getEmployerBenefit(request, pk):
    if not Employer.objects.filter(id=pk).exists():
        return Response({'message': 'Employer not found.'}, status=404)
    employer_benefit = EmployerBenefit.objects.filter(employer_id=pk)
    if employer_benefit.exists():
        serializer = EmployerBenefitSerializer(employer_benefit, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Employer benefits not found'}, status=404)


@api_view(['GET'])
def getEmployerLocation(request, pk):
    if not Employer.objects.filter(id=pk).exists():
        return Response({'message': 'Employer not found.'}, status=404)
    employer_locations = EmployerLocation.objects.filter(employer_id=pk)
    if employer_locations.exists():
        serializer = EmployerLocationSerializer(employer_locations, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'No locations found for this employer'}, status=404)
