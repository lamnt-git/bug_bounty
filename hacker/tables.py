import django_tables2 as tables
from django_tables2.utils import A
from company.models import Program
from submission.models import Submission

from contracts.contracts import HackerInterface

class ProgramListTable(tables.Table):
    address = tables.Column(linkify=('hacker_program_detail', {'addr': A('address')}))
    status  = tables.Column(empty_values=())

    def render_status(self, record):
        caller = HackerInterface(record.company.address)
        return caller.getContractStatus(record.address, record.abi)

    class Meta:
        model = Program
        fields = ['address', 'baseBounty', 'status']
        attrs = {"class": "table-striped table-bordered"}
        # empty_text = "There are no program matching the search criteria..."

class ProgramDetailTable(tables.Table):
      
    class Meta:
        model = Program
        fields = ('address', 'scope', 'baseBounty', 'notice')
        attrs = {"class": "table-striped table-bordered"}
        # empty_text = "There are no program matching the search criteria..."


class MySubmissionsTable(tables.Table):
    submissionId = tables.Column(linkify=('submission_detail', {'addr': A('program__address'), 'submissionId': A('submissionId')}))
      
    class Meta:
        model = Submission
        fields = ('submissionId', 'program__address', 'name', 'bounty', 'resolved')
        attrs = {"class": "table-striped table-bordered"}
        # empty_text = "There are no program matching the search criteria..."