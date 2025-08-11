from datetime import date

from django.db.models import DurationField, ExpressionWrapper, F, Sum
from django.db.models.functions import Coalesce

from JobApp.models import Candidate


class CandidateWithExperienceMixin:
    """
    A mixin for views that provides a queryset of candidates
    annotated with their total work experience in days.
    """

    def get_queryset(self):
        """
        Returns a queryset of `Candidate` objects, each annotated with the
        `total_experience_days` field.
        """
        today = date.today()
        return Candidate.objects.annotate(
            total_experience_days=Sum(
                ExpressionWrapper(
                    (
                        Coalesce("candidateexperience__date_to", today)
                        - F("candidateexperience__date_from")
                    ),
                    output_field=DurationField(),
                )
            )
        )
