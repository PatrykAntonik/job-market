from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, views
from rest_framework.decorators import api_view
from rest_framework.response import Response

from JobApp.models import JobOffer
from JobApp.pagination import OptionalPagination
from JobApp.serializers import (
    ContractTypeSerializer,
    JobOfferSerializer,
    RemotenessLevelSerializer,
    SenioritySerializer,
    SkillSerializer,
)


class JobOfferChoicesView(views.APIView):
    """
    Retrieve the available choices for job offer fields.
    """

    def get(self, request):
        return Response(
            {
                "seniority": JobOffer.Seniority.choices,
                "contract": JobOffer.ContractType.choices,
                "remoteness": JobOffer.RemotenessLevel.choices,
            }
        )


# @api_view(["GET"])
# def getSkills(request):
#     skills = Skill.objects.all()
#     serializer = SkillSerializer(skills, many=True)
#     return Response(serializer.data)
#
#
# @api_view(["GET"])
# def getContractTypes(request):
#     contract_types = ContractType.objects.all()
#     serializer = ContractTypeSerializer(contract_types, many=True)
#     return Response(serializer.data)
#
#
# @api_view(["GET"])
# def getRemotenessLevels(request):
#     remoteness_levels = RemotenessLevel.objects.all()
#     serializer = RemotenessLevelSerializer(remoteness_levels, many=True)
#     return Response(serializer.data)
#
#
# @api_view(["GET"])
# def getSeniority(request):
#     seniority = Seniority.objects.all()
#     serializer = SenioritySerializer(seniority, many=True)
#     return Response(serializer.data)
#
#
# @api_view(["GET"])
# def getJobOffers(request):
#     job_offers = JobOffer.objects.all()
#     serializer = JobOfferSerializer(job_offers, many=True)
#     return Response(serializer.data)
#
#
# class JobOfferList(generics.ListCreateAPIView):
#     queryset = JobOffer.objects.all()
#     serializer_class = JobOfferSerializer
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     ]
#     filterset_fields = [
#         "contract_type",
#         "remoteness_level",
#         "seniority",
#         "skills",
#         "wage",
#         "position",
#     ]
#     search_fields = ["title", "description", ""]
#     ordering_fields = ["created_at"]
#     pagination_class = OptionalPagination
#
#
# @api_view(["GET"])
# def getJobOffer(request, pk):
#     try:
#         job_offer = JobOffer.objects.get(id=pk)
#         serializer = JobOfferSerializer(job_offer, many=False)
#         return Response(serializer.data)
#     except JobOffer.DoesNotExist:
#         return Response({"message": "Job offer not found"}, status=404)
#
#
# @api_view(["GET"])
# def getEmployerJobOffers(request, pk):
#     if not Employer.objects.filter(id=pk).exists():
#         return Response({"message": "Employer not found"}, status=404)
#     job_offers = JobOffer.objects.filter(employer_id=pk)
#     if job_offers.exists():
#         serializer = JobOfferSerializer(job_offers, many=True)
#         return Response(serializer.data)
#     else:
#         return Response(
#             {"message": "Job offers not found for this employer"}, status=404
#         )
# @api_view(["GET"])
# def getIndustries(request):
#     industries = Industry.objects.all()
#     serializer = IndustrySerializer(industries, many=True)
#     return Response(serializer.data)
#
# @api_view(["GET"])
# def getIndustry(.request, pk):
#     try:
#         industry = Industry.objects.get(id=pk)
#         serializer = IndustrySerializer(industry, many=False)
#         return Response(serializer.data)
#     except Industry.DoesNotExist:
#         return Response({"message": "Industry not found"}, status=404)

# TODO- Add benefit list view
