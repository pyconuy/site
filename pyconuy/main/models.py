from cms.models import CMSPlugin, Page
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict
from django.utils import timezone


class MenuPlugin(CMSPlugin):

    title = models.CharField(max_length=30)
    url = models.CharField(max_length=30, null=True, blank=True)
    page = models.ForeignKey(Page, verbose_name=_("page"), blank=True, null=True, help_text=_("A link to a page has priority over a text link."))
    target = models.CharField(_("target"), blank=True, max_length=100, choices=((
        ("", _("same window")),
        ("_blank", _("new window")),
        ("_parent", _("parent window")),
        ("_top", _("topmost frame")),
    )))
    css_class = models.CharField(max_length=30, null=True, blank=True)
    condition = models.CharField(max_length=1, choices=(
        ('A', _('User must be authenticated')),
        ('B', _('Show always')),
        ('U', _('User must not be authenticated'))
    ))

    def __unicode__(self):
        return self.title


class SiteConfig(models.Model):

    site = models.ForeignKey('sites.Site')

    show_sponsors = models.BooleanField()

    call_for_proposals_open = models.DateTimeField(null=True, blank=True)
    call_for_proposals_deadline = models.DateTimeField(null=True, blank=True)
    call_for_proposals_acceptance = models.DateTimeField(null=True, blank=True)

    event_start_date = models.DateTimeField(null=True, blank=True)
    event_end_date = models.DateTimeField(null=True, blank=True)
    event_talks_date = models.DateTimeField(null=True, blank=True)
    event_sprints_date = models.DateTimeField(null=True, blank=True)

    venue_name = models.CharField(max_length=100, blank=True, null=True)
    venue_long_name = models.CharField(max_length=200, blank=True, null=True)
    venue_address = models.CharField(max_length=200, blank=True, null=True)
    venue_link = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.site)

    @property
    def can_add_proposal(self):
        if self.call_for_proposals_open is None:
            return False
        elif self.call_for_proposals_deadline is None:
            return False
        else:
            return self.call_for_proposals_open <= timezone.now() <= self.call_for_proposals_deadline

    def to_dict(self):
        value = model_to_dict(self)
        value['can_add_proposal'] = self.can_add_proposal
        return value
