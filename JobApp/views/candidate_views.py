from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from JobApp.filters import CandidateFilter
from JobApp.mixins import CandidateWithExperienceMixin
from JobApp.models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidateSkill,
)
from JobApp.pagination import OptionalPagination
from JobApp.permissions import IsEmployer
from JobApp.serializers import (
    CandidateEducationCreateSerializer,
    CandidateEducationSerializer,
    CandidateExperienceCreateSerializer,
    CandidateExperienceSerializer,
    CandidateRegistrationSerializer,
    CandidateSerializer,
    CandidateSerializerWithTotalExp,
    CandidateSkillCreateSerializer,
    CandidateSkillSerializer,
)
from docs.candidate_docs import (
    candidate_detail_docs,
    candidate_education_detail_docs,
    candidate_education_list_docs,
    candidate_education_profile_docs,
    candidate_experience_detail_docs,
    candidate_experience_list_docs,
    candidate_experience_profile_docs,
    candidate_list_docs,
    candidate_profile_docs,
    candidate_skill_detail_docs,
    candidate_skill_list_docs,
    candidate_skill_profile_docs,
    register_candidate_docs,
)


@candidate_list_docs
class CandidateListView(CandidateWithExperienceMixin, generics.ListAPIView):
    """
    List all candidates with their total experience.
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializerWithTotalExp
    permission_classes = [IsEmployer]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CandidateFilter
    pagination_class = OptionalPagination
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["id", "user__city__name", "user__city__country__name"]
    ordering = ["id"]


@candidate_detail_docs
class CandidateDetailView(CandidateWithExperienceMixin, generics.RetrieveAPIView):
    """
    Retrieve a candidate's details along with their total experience.
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializerWithTotalExp
    permission_classes = [IsEmployer]


@candidate_skill_list_docs
class CandidateSkillListView(generics.ListAPIView):
    """
    List all skills of a candidate.
    """

    serializer_class = CandidateSkillSerializer
    permission_classes = [IsEmployer]
    pagination_class = OptionalPagination

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, pk=self.kwargs["pk"])
        return CandidateSkill.objects.filter(candidate=candidate).order_by("id")


@candidate_experience_list_docs
class CandidateExperienceListView(generics.ListAPIView):
    """
    List all experiences of a candidate.
    """

    serializer_class = CandidateExperienceSerializer
    permission_classes = [IsEmployer]
    pagination_class = OptionalPagination

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, pk=self.kwargs["pk"])
        return CandidateExperience.objects.filter(candidate=candidate).order_by(
            "-is_current", "-date_to"
        )


@candidate_education_list_docs
class CandidateEducationListView(generics.ListAPIView):
    """
    List all education records of a candidate.
    """

    serializer_class = CandidateEducationSerializer
    permission_classes = [IsEmployer]
    pagination_class = OptionalPagination

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, pk=self.kwargs["pk"])
        return CandidateEducation.objects.filter(candidate=candidate).order_by(
            "-is_current", "-date_to"
        )


@register_candidate_docs
class RegisterCandidateView(generics.CreateAPIView):
    """
    Register a new candidate.
    """

    serializer_class = CandidateRegistrationSerializer

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


@candidate_profile_docs
class CandidateProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update the profile of the authenticated candidate.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CandidateSerializer

    def get_object(self):
        return get_object_or_404(Candidate, user=self.request.user)


@candidate_skill_profile_docs
class CandidateSkillListProfileView(generics.ListCreateAPIView):
    """
    List all skills of the authenticated candidate.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = OptionalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CandidateSkillCreateSerializer
        return CandidateSkillSerializer

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        return CandidateSkill.objects.filter(candidate=candidate).order_by("id")

    def perform_create(self, serializer):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        serializer.save(candidate=candidate)


@candidate_education_profile_docs
class CandidateEducationListProfileView(generics.ListCreateAPIView):
    """
    List all education records of the authenticated candidate.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = OptionalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CandidateEducationCreateSerializer
        return CandidateEducationSerializer

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        return CandidateEducation.objects.filter(candidate=candidate).order_by(
            "-is_current", "-date_to"
        )

    def perform_create(self, serializer):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        serializer.save(candidate=candidate)


@candidate_experience_profile_docs
class CandidateExperienceListProfileView(generics.ListCreateAPIView):
    """
    List all experience records of the authenticated candidate.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = OptionalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CandidateExperienceCreateSerializer
        return CandidateExperienceSerializer

    def get_queryset(self):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        return CandidateExperience.objects.filter(candidate=candidate).order_by(
            "-is_current", "-date_to"
        )

    def perform_create(self, serializer):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        serializer.save(candidate=candidate)


@candidate_experience_detail_docs
class CandidateExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific experience record of the authenticated candidate.
    """

    serializer_class = CandidateExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        experience_id = self.kwargs["pk"]
        return get_object_or_404(
            CandidateExperience, pk=experience_id, candidate=candidate
        )


@candidate_education_detail_docs
class CandidateEducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific education record of the authenticated candidate.
    """

    serializer_class = CandidateEducationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        education_id = self.kwargs["pk"]
        return get_object_or_404(
            CandidateEducation, pk=education_id, candidate=candidate
        )


@candidate_skill_detail_docs
class CandidateSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific skill record of the authenticated candidate.
    """

    serializer_class = CandidateSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        candidate = get_object_or_404(Candidate, user=self.request.user)
        skill_id = self.kwargs["pk"]
        return get_object_or_404(CandidateSkill, pk=skill_id, candidate=candidate)
