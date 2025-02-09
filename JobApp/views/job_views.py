from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from JobApp.serializers import *


@api_view(['GET'])
def getSkills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getContractTypes(request):
    contract_types = ContractType.objects.all()
    serializer = ContractTypeSerializer(contract_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRemotenessLevels(request):
    remoteness_levels = RemotenessLevel.objects.all()
    serializer = RemotenessLevelSerializer(remoteness_levels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSeniority(request):
    seniority = Seniority.objects.all()
    serializer = SenioritySerializer(seniority, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getJobOffers(request):
    job_offers = JobOffer.objects.all()
    serializer = JobOfferSerializer(job_offers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getJobOffer(request, pk):
    try:
        job_offer = JobOffer.objects.get(id=pk)
        serializer = JobOfferSerializer(job_offer, many=False)
        return Response(serializer.data)
    except JobOffer.DoesNotExist:
        return Response({'message': 'Job offer not found'}, status=404)


@api_view(['GET'])
def getEmployerJobOffers(request, pk):
    if not Employer.objects.filter(id=pk).exists():
        return Response({'message': 'Employer not found'}, status=404)
    job_offers = JobOffer.objects.filter(employer_id=pk)
    if job_offers.exists():
        serializer = JobOfferSerializer(job_offers, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Job offers not found for this employer'}, status=404)