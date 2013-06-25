from django.conf.urls import *

urlpatterns = patterns('main.views',
    url(r"^$", 'index', name='index'),
    url(r"^proposal-add$", 'proposal_add', name='proposal_add'),
    url(r"^proposal-sent$", 'proposal_sent', name='proposal_sent'),
    url(r"^schedule$", 'schedule', name='schedule'),
    url(r"^sponsors", 'sponsors', name='sponsors'),
    url(r"^speakers", 'speakers', name='speakers'),
    url(r"^proposals", 'proposals', name='proposals'),
    url(r"^talks", 'talks', name='talks'),
)