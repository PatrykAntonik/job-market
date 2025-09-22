from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from JobApp.filters import EmployerFilter
from JobApp.models import Employer, EmployerBenefit, EmployerLocation
from JobApp.pagination import OptionalPagination
from JobApp.serializers import (
    EmployerBenefitCreateSerializer,
    EmployerBenefitSerializer,
    EmployerLocationCreateSerializer,
    EmployerLocationSerializer,
    EmployerRegistrationSerializer,
    EmployerSerializer,
)


class EmployerListView(generics.ListAPIView):
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


class EmployerDetailView(generics.RetrieveAPIView):
    """
    Retrieve an employer's details.
    """

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [AllowAny]


class EmployerProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an employer's profile details.
    """

    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

    def get_object(self):
        return get_object_or_404(Employer, user=self.request.user)


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
