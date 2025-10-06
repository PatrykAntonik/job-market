from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from JobApp.filters import EmployerFilter
from JobApp.models import Benefit, Employer, EmployerBenefit, EmployerLocation
from JobApp.pagination import OptionalPagination
from JobApp.serializers import (
    BenefitSerializer,
    EmployerBenefitCreateSerializer,
    EmployerBenefitSerializer,
    EmployerLocationCreateSerializer,
    EmployerLocationSerializer,
    EmployerRegistrationSerializer,
    EmployerSerializer,
)
from docs.employer_docs import (
    benefit_list_docs,
    employer_benefit_detail_docs,
    employer_benefit_list_profile_docs,
    employer_detail_docs,
    employer_list_benefit_docs,
    employer_list_docs,
    employer_location_detail_docs,
    employer_location_list_docs,
    employer_location_list_profile_docs,
    employer_profile_docs,
    register_employer_docs,
)


@benefit_list_docs
class BenefitListView(generics.ListAPIView):
    """
    Retrieve a list of all benefits.
    """

    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    permission_classes = [AllowAny]
    pagination_class = OptionalPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering = ["name"]
    search_fields = ["name"]


@employer_list_docs
class EmployerListView(generics.ListAPIView):
    """
    Retrieve a list of employers with optional filtering, searching, and ordering.
    """

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [AllowAny]
    pagination_class = OptionalPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering = ["id"]
    ordering_fields = ["id", "company_name", "industry__name"]
    search_fields = ["company_name", "description"]
    filterset_class = EmployerFilter


@employer_detail_docs
class EmployerDetailView(generics.RetrieveAPIView):
    """
    Retrieve an employer's details.
    """

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [AllowAny]


@employer_profile_docs
class EmployerProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an employer's profile details.
    """

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Employer, user=self.request.user)


@register_employer_docs
class RegisterEmployerView(generics.CreateAPIView):
    """
    Register a new employer.
    """

    serializer_class = EmployerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@employer_location_list_docs
class EmployerLocationListView(generics.ListAPIView):
    """
    Retrieve a list of locations for a specific employer.
    """

    serializer_class = EmployerLocationSerializer
    permission_classes = [AllowAny]
    pagination_class = OptionalPagination

    def get_queryset(self):
        employer = get_object_or_404(Employer, pk=self.kwargs["pk"])
        return EmployerLocation.objects.filter(employer=employer).order_by("city__name")


@employer_location_detail_docs
class EmployerLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific location of the authenticated employer.
    """

    serializer_class = EmployerLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        location_id = self.kwargs["pk"]
        return get_object_or_404(EmployerLocation, pk=location_id, employer=employer)


@employer_location_list_profile_docs
class EmployerLocationListProfileView(generics.ListCreateAPIView):
    """
    Retrieve a list of locations for the authenticated employer.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = OptionalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EmployerLocationCreateSerializer
        return EmployerLocationSerializer

    def get_queryset(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        return EmployerLocation.objects.filter(employer=employer).order_by("city__name")

    def perform_create(self, serializer):
        employer = get_object_or_404(Employer, user=self.request.user)
        serializer.save(employer=employer)


@employer_benefit_list_profile_docs
class EmployerBenefitListProfileView(generics.ListCreateAPIView):
    """
    Retrieve a list of benefits for the authenticated employer.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = OptionalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EmployerBenefitCreateSerializer
        return EmployerBenefitSerializer

    def get_queryset(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        return EmployerBenefit.objects.filter(employer=employer).order_by(
            "benefit__name"
        )

    def perform_create(self, serializer):
        employer = get_object_or_404(Employer, user=self.request.user)
        serializer.save(employer=employer)


@employer_benefit_detail_docs
class EmployerBenefitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific benefit of the authenticated employer.
    """

    serializer_class = EmployerBenefitSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        employer = get_object_or_404(Employer, user=self.request.user)
        benefit_id = self.kwargs["pk"]
        return get_object_or_404(EmployerBenefit, pk=benefit_id, employer=employer)


@employer_list_benefit_docs
class EmployerListBenefitView(generics.ListAPIView):
    """
    Retrieve a list of benefits for a specific employer.
    """

    serializer_class = EmployerBenefitSerializer
    permission_classes = [AllowAny]
    pagination_class = OptionalPagination

    def get_queryset(self):
        employer = get_object_or_404(Employer, pk=self.kwargs["pk"])
        return EmployerBenefit.objects.filter(employer=employer).order_by(
            "benefit__name"
        )
