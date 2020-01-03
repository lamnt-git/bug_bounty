from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from company.views import RewardBountyView, RejectSubmissionView

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:addr>/<int:submissionId>/add_comment', login_required(views.AddCommentView), name='add_comment'),
    path('<str:addr>/<int:submissionId>/reward', login_required(RewardBountyView), name='reward_bounty'),
    path('<str:addr>/<int:submissionId>/reject', login_required(RejectSubmissionView), name='reject'),
    path('<str:addr>/<int:submissionId>', login_required(views.SubmissionView.as_view()), name='submission_detail'),
]