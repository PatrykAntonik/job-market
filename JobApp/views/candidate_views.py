from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from JobApp.filters import CandidateFilter
from JobApp.pagination import OptionalPagination
from JobApp.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from JobApp.permissions import IsEmployer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from JobApp.models import *
from JobApp.pagination import OptionalPagination
from datetime import date
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.db.models.functions import Coalesce
from JobApp.mixins import *
from JobApp.models import *
from docs.candidate_docs import *
from rest_framework import status


@candidate_list_docs
class CandidateListView(CandidateWithExperienceMixin, generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsEmployer]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CandidateFilter
    pagination_class = OptionalPagination
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["user__city__name"]
    ordering = ["id"]


@candidate_detail_docs
class CandidateDetailView(CandidateWithExperienceMixin, generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsEmployer]


@candidate_skill_list_docs
class CandidateSkillListView(generics.ListAPIView):
    serializer_class = CandidateSkillSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, pk=self.kwargs["pk"])
        return CandidateSkill.objects.filter(candidate=candidate).order_by("id")


@candidate_experience_list_docs
class CandidateExperienceListView(CandidateWithExperienceMixin, generics.ListAPIView):
    serializer_class = CandidateExperienceSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, pk=self.kwargs["pk"])
        return CandidateExperience.objects.filter(candidate=candidate).order_by(
            "-is_current", "-date_to"
        )


@candidate_education_list_docs
class CandidateEducationListView(generics.ListAPIView):
    serializer_class = CandidateEducationSerializer
    permission_classes = [IsEmployer]

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, pk=self.kwargs["pk"])
        return CandidateEducation.objects.filter(candidate=candidate).order_by(
            "-is_current", "-date_to"
        )


@register_candidate_docs
class RegisterCandidateView(generics.CreateAPIView):
    serializer_class = CandidateRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# class CandidateProfileView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CandidateSerializer
