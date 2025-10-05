from datetime import timedelta

from django.utils import timezone
import django_filters
from django_filters import widgets

from .models import (
    Benefit,
    Candidate,
    City,
    Country,
    Employer,
    Industry,
    JobOffer,
    Skill,
    User,
)


class UserFilter(django_filters.FilterSet):
    """
    FilterSet for filtering users by city and country.

    Filters:
        - city: Filters users by city name.
        - country: Filters users by country name.
    """

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


class EmployerFilter(django_filters.FilterSet):
    """
    FilterSet for filtering employers based on city, country and industry.
    Filters:
        - city: Filters employers by city name.
        - country: Filters employers by country name.
        - industry: Filters employers by industry name.
        - benefits: Filters employers by benefits offered.
    """

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
    industry = django_filters.ModelMultipleChoiceFilter(
        field_name="industry__name",
        to_field_name="name",
        queryset=Industry.objects.all(),
        label="Industry",
        widget=widgets.CSVWidget,
    )
    benefits = django_filters.ModelMultipleChoiceFilter(
        field_name="benefits__name",
        to_field_name="name",
        queryset=Benefit.objects.all(),
        label="Benefit",
        widget=widgets.CSVWidget,
    )

    class Meta:
        model = Employer
        fields = ["city", "country", "industry", "benefits"]


class CandidateFilter(django_filters.FilterSet):
    """
    FilterSet for filtering candidates based on various criteria.

    Filters:
        - city: Filters candidates by city name.
        - country: Filters candidates by country name.
        - skill: Filters candidates by skill name.
        - field_of_study: Filters candidates by field of study.
        - school_name: Filters candidates by school name.
        - degree: Filters candidates by degree.
        - education_is_current: Filters candidates by whether their education is current.
        - job_is_current: Filters candidates by whether their job is current.
        - job_position: Filters candidates by job position.
        - min_experience_years: Filters candidates by minimum years of experience.
    """

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
    max_experience_years = django_filters.NumberFilter(
        method="filter_max_experience_years", label="Max experience (years)"
    )

    def filter_min_experience_years(self, queryset, name, value):
        """
        Filters the queryset to include only candidates with at least the specified number of years of experience.
        """

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

    def filter_max_experience_years(self, queryset, name, value):
        """
        Filters the queryset to include only candidates with at most the specified number of years of experience.
        """

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
            <= value
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
            "max_experience_years",
        ]


class JobOfferFilter(django_filters.FilterSet):
    """
    FilterSet for filtering job offers based on various criteria.

    Filters:

    """

    city = django_filters.ModelMultipleChoiceFilter(
        field_name="location__city__name",
        to_field_name="name",
        queryset=City.objects.all(),
        widget=widgets.CSVWidget,
    )
    country = django_filters.ModelMultipleChoiceFilter(
        field_name="location__city__country__name",
        to_field_name="name",
        queryset=Country.objects.all(),
        label="Country",
        widget=widgets.CSVWidget,
    )
    skill = django_filters.ModelMultipleChoiceFilter(
        field_name="jobofferskill__skill__name",
        to_field_name="name",
        queryset=Skill.objects.all(),
        label="Skill",
        widget=widgets.CSVWidget,
    )
    industry = django_filters.ModelMultipleChoiceFilter(
        field_name="employer__industry__name",
        to_field_name="name",
        queryset=Industry.objects.all(),
        label="Industry",
        widget=widgets.CSVWidget,
    )
    seniority = django_filters.BaseInFilter(
        field_name="seniority",
        lookup_expr="in",
        widget=widgets.CSVWidget,
    )
    contract = django_filters.BaseInFilter(
        field_name="contract",
        lookup_expr="in",
        widget=widgets.CSVWidget,
    )
    remoteness = django_filters.BaseInFilter(
        field_name="remoteness",
        lookup_expr="in",
        widget=widgets.CSVWidget,
    )
    min_wage = django_filters.NumberFilter(field_name="wage", lookup_expr="gte")
    max_wage = django_filters.NumberFilter(field_name="wage", lookup_expr="lte")
    benefits = django_filters.ModelMultipleChoiceFilter(
        field_name="employer__employerbenefit__benefit__name",
        to_field_name="name",
        queryset=Benefit.objects.all(),
        label="Benefit",
        widget=widgets.CSVWidget,
    )
    posted_within = django_filters.CharFilter(
        method="filter_posted_within",
        label="Posted within (e.g., 1d, 7d, 30d, 24h)",
    )

    def filter_posted_within(self, queryset, name, value):
        try:
            unit = value[-1].lower()
            amount = int(value[:-1])
            now = timezone.now()
            if unit == "d":
                delta = timedelta(days=amount)
            elif unit == "h":
                delta = timedelta(hours=amount)
            elif unit == "m":
                delta = timedelta(minutes=amount)
            else:
                return queryset
            return queryset.filter(created_at__gte=now - delta)
        except (ValueError, IndexError):
            return queryset

    class Meta:
        model = JobOffer
        fields = [
            "city",
            "country",
            "skill",
            "industry",
            "seniority",
            "contract",
            "remoteness",
            "min_wage",
            "max_wage",
            "benefits",
            "posted_within",
        ]
