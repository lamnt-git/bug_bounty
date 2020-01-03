import django_tables2 as tables
from django_tables2.utils import A
from .models import Program
from submission.models import Submission


class ProgramTable(tables.Table):
    address = tables.Column(linkify=('company_program_detail', {'addr': A('address')}))

    class Meta:
        model = Program
        fields = ('address', 'scope', 'baseBounty', 'notice')


class SubmissionTable(tables.Table):
    submissionId = tables.Column(linkify=('submission_detail', {'addr': A('program__address'), 'submissionId': A('submissionId')}))
    # resolved = tables.TemplateColumn("{{ processing }}")
      
    class Meta:
        model = Submission
        fields = ('submissionId', 'name', 'severity', 'bounty', 'resolved')
        # attrs = {"class": "table-striped table-bordered"}
        # empty_text = "There are no program matching the search criteria..."