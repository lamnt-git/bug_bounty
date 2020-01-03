import django_tables2 as tables
from django_tables2.utils import A

from .models import Submission

class SubmissionTable(tables.Table):
    # resolved = tables.Boolean

    class Meta:
        model = Submission
        fields = ('submissionId', 'program__address', 'name', 'poc', 'severity', 'resolved')