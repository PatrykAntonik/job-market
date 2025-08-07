from datetime import date, timedelta

import django_filters
from django.db.models import DurationField, ExpressionWrapper, F
from django.db.models.functions import Now
from django_filters import FilterSet, widgets

from .models import Candidate, CandidateEducation, City, Country, Skill, User


class UserFilter(django_filters.FilterSet):
    city = django_filters.ModelMultipleChoiceFilter(
        field_name="city__name",
        to_field_name="name",
        queryset=City.objects.all(),
        widget=widgets.CSVWidget,
    )
    country = django_filters.ModelMultipleChoiceFilter(
        field_name="city__country__name",
        to_field_name="name",
        queryset=Country.objects.all(),
        label="Country",
        widget=widgets.CSVWidget,
    )

    class Meta:
        model = User
        fields = ["city", "country"]


def round_half_year(years):
    return round(years * 2) / 2


class CandidateFilter(django_filters.FilterSet):
    city = django_filters.ModelMultipleChoiceFilter(
        field_name="user__city__name",
        to_field_name="name",
        queryset=City.objects.all(),
        widget=widgets.CSVWidget,
    )
    country = django_filters.ModelMultipleChoiceFilter(
        field_name="user__city__country__name",
        to_field_name="name",
        queryset=Country.objects.all(),
        label="Country",
        widget=widgets.CSVWidget,
    )
    skill = django_filters.ModelMultipleChoiceFilter(
        field_name="candidateskill__skill__name",
        to_field_name="name",
        queryset=Skill.objects.all(),
        label="Skill",
        widget=widgets.CSVWidget,
    )
    field_of_study = django_filters.BaseInFilter(
        field_name="candidateeducation__field_of_study",
        lookup_expr="in",
        widget=widgets.CSVWidget,
    )
    school_name = django_filters.BaseInFilter(
        field_name="candidateeducation__school_name",
        lookup_expr="in",
        widget=widgets.CSVWidget,
    )
    degree = django_filters.BaseInFilter(
        field_name="candidateeducation__degree",
        lookup_expr="in",
        widget=widgets.CSVWidget,
    )
    education_is_current = django_filters.BooleanFilter(
        field_name="candidateeducation__is_current",
    )
    job_is_current = django_filters.BooleanFilter(
        field_name="candidateexperience__is_current",
    )
    job_position = django_filters.BaseInFilter(
        field_name="candidateexperience__job_position",
        lookup_expr="in",
        widget=widgets.CSVWidget,
    )
    min_experience_years = django_filters.NumberFilter(
        method="filter_min_experience_years", label="Min experience (years)"
    )

    def filter_min_experience_years(self, queryset, name, value):
        def days_to_half_years(days):
            if days is None:
                return 0
            return round((days / 365.25) * 2) / 2

        ids = [
            c.id
            for c in queryset
            if days_to_half_years(
                getattr(c, "total_experience_days", 0).days
                if getattr(c, "total_experience_days", None)
                else 0
            )
            >= value
        ]
        return queryset.filter(id__in=ids)

    class Meta:
        model = Candidate
        fields = [
            "city",
            "country",
            "skill",
            "field_of_study",
            "school_name",
            "degree",
            "education_is_current",
            "job_is_current",
            "min_experience_years",
        ]
