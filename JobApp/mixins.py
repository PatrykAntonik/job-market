from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.db.models.functions import Coalesce
from datetime import date
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
