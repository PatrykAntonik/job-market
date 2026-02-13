from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from JobApp.filters import JobOfferFilter
from JobApp.models import Candidate, Employer, Industry, JobOffer, OfferResponse, Skill
from JobApp.pagination import OptionalPagination
from JobApp.permissions import IsCandidate, IsEmployer
from JobApp.serializers import (
    ChoiceSerializer,
    IndustrySerializer,
    JobOfferCreateSerializer,
    JobOfferSerializer,
    JobOfferUpdateSerializer,
    OfferResponseSerializer,
    SkillSerializer,
)
from docs.job_docs import (
    apply_to_job_offer_docs,
    contract_type_list_docs,
    employer_job_offer_list_docs,
    industry_list_docs,
    job_offer_applicants_docs,
    job_offer_detail_docs,
    job_offer_list_docs,
    job_offer_list_profile_docs,
    job_offer_profile_detail_docs,
    remoteness_level_list_docs,
    seniority_list_docs,
    skill_list_docs,
)


@skill_list_docs
class SkillListView(generics.ListAPIView):
    """
    Retrieve a list of all skills.
    """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    pagination_class = OptionalPagination
    search_fields = ["name"]
    ordering = ["name"]


@industry_list_docs
class IndustryListView(generics.ListAPIView):
    """
    Retrieve a list of all industries.
    """

    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [AllowAny]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    pagination_class = OptionalPagination
    search_fields = ["name"]
    ordering = ["name"]


@job_offer_list_docs
class JobOfferListView(generics.ListAPIView):
    """
    Retrieve a list of job offers with optional filtering, searching, and ordering.
    """

    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]
    pagination_class = OptionalPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = JobOfferFilter
    search_fields = [
        "position",
        "description",
        "skills__name",
        "employer__company_name",
        "location__city__name",
        "employer__industry__name",
    ]
    ordering = ["-created_at"]
    ordering_fields = ["created_at", "wage"]


@seniority_list_docs
class SeniorityListView(generics.ListAPIView):
    """
    Retrieve a list of all seniority levels.
    """

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return [
            {"value": value, "display": display}
            for value, display in JobOffer.Seniority.choices
        ]


@contract_type_list_docs
class ContractTypeListView(generics.ListAPIView):
    """
    Retrieve a list of all contract types.
    """

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return [
            {"value": value, "display": display}
            for value, display in JobOffer.ContractType.choices
        ]


@remoteness_level_list_docs
class RemotenessLevelListView(generics.ListAPIView):
    """
    Retrieve a list of all remoteness levels.
    """

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return [
            {"value": value, "display": display}
            for value, display in JobOffer.RemotenessLevel.choices
        ]


@job_offer_detail_docs
class JobOfferDetailView(generics.RetrieveAPIView):
    """
    Retrieve a job offer's details.
    """

    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]


@job_offer_list_profile_docs
class JobOfferListProfileView(generics.ListCreateAPIView):
    """
    Retrieve a list of job offers for the authenticated employer.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = OptionalPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "position",
    ]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return JobOfferCreateSerializer
        return JobOfferSerializer

    def get_queryset(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        return JobOffer.objects.filter(employer=employer).order_by("-created_at")

    def perform_create(self, serializer):
        employer = get_object_or_404(Employer, user=self.request.user)
        serializer.save(employer=employer)


@job_offer_profile_detail_docs
class JobOfferProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific job offer of the authenticated employer.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return JobOfferUpdateSerializer
        return JobOfferSerializer

    def get_queryset(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        return JobOffer.objects.filter(employer=employer)


@employer_job_offer_list_docs
class EmployerJobOfferListView(generics.ListAPIView):
    """
    Retrieve a list of job offers for a specific employer.
    """

    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]
    pagination_class = OptionalPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "position",
    ]
    ordering = ["-created_at"]

    def get_queryset(self):
        employer = get_object_or_404(Employer, pk=self.kwargs["pk"])
        return JobOffer.objects.filter(employer=employer)


@apply_to_job_offer_docs
class ApplyToJobOfferView(generics.CreateAPIView):
    """
    Create an OfferResponse (apply) for the authenticated candidate.
    """

    permission_classes = [IsAuthenticated, IsCandidate]
    serializer_class = OfferResponseSerializer

    def create(self, request, *args, **kwargs):
        job_offer = get_object_or_404(JobOffer, pk=self.kwargs["pk"])
        candidate = get_object_or_404(Candidate, user=request.user)

        if OfferResponse.objects.filter(offer=job_offer, candidate=candidate).exists():
            return Response(
                {"detail": "You have already applied to this job offer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        offer_response = OfferResponse.objects.create(
            offer=job_offer,
            candidate=candidate,
        )
        return Response(
            OfferResponseSerializer(
                offer_response,
                context={"request": request},
            ).data,
            status=status.HTTP_201_CREATED,
        )


@job_offer_applicants_docs
class JobOfferApplicantsListView(generics.ListAPIView):
    """
    List OfferResponse (applicants) for an authenticated employer's job offer.
    """

    permission_classes = [IsAuthenticated, IsEmployer]
    serializer_class = OfferResponseSerializer
    pagination_class = OptionalPagination

    def get_queryset(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        job_offer = get_object_or_404(
            JobOffer,
            pk=self.kwargs["pk"],
            employer=employer,
        )
        return OfferResponse.objects.filter(offer=job_offer).order_by("id")
