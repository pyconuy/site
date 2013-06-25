from django import forms
from symposion.proposals.models import PresentationKind, Proposal
from bootstrap.forms import BootstrapForm
from django.utils.translation import ugettext_lazy as _

class ProposalForm(BootstrapForm):

    title = forms.CharField(max_length=100, label=_("Title"))
    abstract = forms.CharField(widget=forms.Textarea, label=_("Abstract"))
    description = forms.CharField(widget=forms.Textarea, label=_("Description"))
    kind = forms.ModelChoiceField(PresentationKind.objects.all().order_by('name'), label=_("Kind"))
    audience_level = forms.ChoiceField(choices=Proposal.AUDIENCE_LEVELS, label=_("Audience Level"))
    duration = forms.ChoiceField(choices=Proposal.DURATION_CHOICES, label=_("Duration"))
    additional_notes = forms.CharField(widget=forms.Textarea(), required=False, label=_("Additional Notes"))

    biography = forms.CharField(widget=forms.Textarea, label=_("About you (biography)"))