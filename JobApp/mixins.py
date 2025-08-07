from datetime import date

from django.db.models import DurationField, ExpressionWrapper, F, Sum
from django.db.models.functions import Coalesce

from JobApp.models import Candidate


class CandidateWithExperienceMixin:
    """ """

    def get_queryset(self):
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
