# encoding: utf-8
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from markitup.fields import MarkupField
from conference.utils import send_email

from conference.managers import SponsorManager
from conference import SPONSOR_COORDINATORS


class PresentationKind(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    closed = models.NullBooleanField()
    published = models.NullBooleanField()

    @classmethod
    def available(cls):
        now = datetime.datetime.now()
        return cls._default_manager.filter(
            Q(start__lt=now) | Q(start=None),
            Q(end__gt=now) | Q(end=None),
            Q(closed=False) | Q(closed=None),
            )

    def __unicode__(self):
        return self.name


class PresentationCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class Speaker(models.Model):

    SESSION_COUNT_CHOICES = [
        (1, "One"),
        (2, "Two")
    ]

    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(max_length=100)
    biography = MarkupField(help_text="A little bit about you. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>.")
    photo = models.ImageField(upload_to="speaker_photos", blank=True)
    twitter_username = models.CharField(
        max_length = 15,
        blank = True,
        help_text = "Your Twitter account, with or without the @"
    )
    annotation = models.TextField() # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True)
    invite_token = models.CharField(max_length=40, db_index=True)
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    sessions_preference = models.IntegerField(
        choices=SESSION_COUNT_CHOICES,
        null=True,
        blank=True,
        help_text="If you've submitted multiple proposals, please let us know if you only want to give one or if you'd like to give two talks. You may submit more than two proposals."
    )

    def __unicode__(self):
        if self.user:
            return self.name
        else:
            return "?"

    def get_absolute_url(self):
        return reverse("speaker_edit")

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email


class Proposal(models.Model):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
        ]

    DURATION_CHOICES = [
        (0, "No preference"),
        (1, "I prefer a 30 minute slot"),
        (2, "I prefer a 45 minute slot"),
        ]

    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "If your talk is accepted this will be made public and printed in the program. Should be one paragraph, maximum 400 characters."
    )
    kind = models.ForeignKey(PresentationKind)
    category = models.ForeignKey(PresentationCategory)
    abstract = MarkupField(
        help_text = "Detailed description and outline. Will be made public if your talk is accepted. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>."
    )
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    additional_notes = MarkupField(
        blank=True,
        help_text = "Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>."
    )
    extreme = models.BooleanField(
        default=False,
        help_text = "'Extreme' talks are advanced talks with little or no introductory material. See <a href='http://us.pycon.org/2012/speaker/extreme/' target='_blank'>http://us.pycon.org/2012/speaker/extreme/</a> for details."
    )
    duration = models.IntegerField(choices=DURATION_CHOICES)
    submitted = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False,
        )
    speaker = models.ForeignKey("conference.Speaker", related_name="proposals")
    additional_speakers = models.ManyToManyField("conference.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)

    def can_edit(self):
        return True

    @property
    def speaker_email(self):
        return self.speaker.email

    @property
    def number(self):
        return str(self.pk).zfill(3)

    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker


class Track(models.Model):

    name = models.CharField(max_length=65)

    def __unicode__(self):
        return self.name


class Session(models.Model):

    track = models.ForeignKey(Track, null=True, related_name="sessions")

    def sorted_slots(self):
        ct = ContentType.objects.get_for_model(Presentation)
        return self.slots.filter(kind=ct).order_by("start")

    # @@@ cache?
    def start(self):
        slots = self.sorted_slots()
        if slots:
            return list(slots)[0].start
        else:
            return None

    # @@@ cache?
    def end(self):
        slots = self.sorted_slots()
        if slots:
            return list(slots)[-1].end
        else:
            return None

    def __unicode__(self):
        start = self.start()
        end = self.end()
        if start and end:
            return u"%s: %s — %s" % (
                start.strftime("%a"),
                start.strftime("%X"),
                end.strftime("%X")
            )
        return u""


class Slot(models.Model):

    title = models.CharField(max_length=100, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    kind = models.ForeignKey(ContentType, null=True, blank=True)
    track = models.ForeignKey(Track, null=True, blank=True, related_name="slots")
    session = models.ForeignKey(Session, null=True, blank=True, related_name="slots")

    def content(self):
        if self.kind_id:
            return self.kind.get_object_for_this_type(slot=self)
        else:
            return None

    def assign(self, content, old_content=None):
        if old_content is not None:
            old_content.slot = None
            old_content.save()
        content.slot = self
        content.save()
        self.kind = ContentType.objects.get_for_model(content)
        self.save()

    def unassign(self):
        content = self.content()
        content.slot = None
        content.save()
        self.kind = None
        self.save()

    def __unicode__(self):
        return u"%s (%s: %s — %s)" % (self.title, self.start.strftime("%a"), self.start.strftime("%X"), self.end.strftime("%X"))


class Presentation(models.Model):

    PRESENTATION_TYPE_TALK = 1
    PRESENTATION_TYPE_PANEL = 2
    PRESENTATION_TYPE_TUTORIAL = 3
    PRESENTATION_TYPE_POSTER = 4

    PRESENTATION_TYPES = [
        (PRESENTATION_TYPE_TALK, "Talk"),
        (PRESENTATION_TYPE_PANEL, "Panel"),
        (PRESENTATION_TYPE_TUTORIAL, "Tutorial"),
        (PRESENTATION_TYPE_POSTER, "Poster")
    ]

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
        ]

    DURATION_CHOICES = [
        (0, "No preference"),
        (1, "I prefer a 30 minute slot"),
        (2, "I prefer a 45 minute slot"),
        ]

    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="presentation")

    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "Brief one paragraph blurb (will be public if accepted). Must be 400 characters or less"
    )
    kind = models.ForeignKey(PresentationKind)
    category = models.ForeignKey(PresentationCategory)
    abstract = MarkupField(
        help_text = "More detailed description (will be public if accepted).",
        )
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    duration = models.IntegerField(choices=DURATION_CHOICES)

    submitted = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False,
        )
    speaker = models.ForeignKey("conference.Speaker", related_name="sessions")
    additional_speakers = models.ManyToManyField("conference.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)

    extreme_pycon = models.BooleanField(u"EXTREME PyCon!", default=False)
    invited = models.BooleanField(default=False)

    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker

    def __unicode__(self):
        return u"%s" % self.title


class Benefit(models.Model):

    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    type = models.CharField(
        _("type"),
        choices=[
            ("text", "Text"),
            ("file", "File"),
            ("weblogo", "Web Logo"),
            ("simple", "Simple")
        ],
        max_length=10,
        default="simple"
    )

    def __unicode__(self):
        return self.name


class SponsorLevel(models.Model):

    name = models.CharField(_("name"), max_length=100)
    order = models.IntegerField(_("order"), default=0)
    cost = models.PositiveIntegerField(_("cost"))
    description = models.TextField(_("description"), blank=True, help_text=_("This is private."))

    class Meta:
        ordering = ["order"]

    def __unicode__(self):
        return self.name


class Sponsor(models.Model):

    applicant = models.OneToOneField(
        User, related_name="sponsorship", verbose_name=_("applicant"), null=True
    )
    name = models.CharField(_("sponsor name"), max_length=100)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(_("contact name"), max_length=100)
    contact_email = models.EmailField(_(u"Contact email"))
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"), null=True)
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    active = models.NullBooleanField(_("active"))

    # Denormalization  # @@@ This'll break if we can ever have more than one logo
    sponsor_logo = models.ForeignKey("SponsorBenefit", related_name="+", null=True, blank=True, editable=False)

    objects = SponsorManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.active:
            return reverse("sponsor_detail", kwargs={"pk": self.pk})
        return reverse("sponsor_info")

    @property
    def website_logo_url(self):
        if not hasattr(self, '_website_logo_url'):
            self._website_logo_url = None
            benefits = self.sponsor_benefits.filter(benefit__type="weblogo", upload__isnull=False)
            if benefits.count():
                # @@@ smarter handling of multiple weblogo benefits?
                # shouldn't happen
                if benefits[0].upload:
                    self._website_logo_url = benefits[0].upload.url
        return self._website_logo_url

    @property
    def listing_text(self):
        if not hasattr(self, '_listing_text'):
            self._listing_text = None
            benefits = self.sponsor_benefits.filter(benefit__id=8)
            if benefits.count():
                self._listing_text = benefits[0].text
        return self._listing_text

    @property
    def joblisting_text(self):
        if not hasattr(self, '_joblisting_text'):
            self._joblisting_text = None
            benefits = self.sponsor_benefits.filter(benefit__id=21)
            if benefits.count():
                self._joblisting_text = benefits[0].text
        return self._joblisting_text

    @property
    def website_logo(self):
        if self.sponsor_logo is None:
            benefits = self.sponsor_benefits.filter(benefit__type="weblogo", upload__isnull=False)[:1]
            if benefits.count():
                if benefits[0].upload:
                    self.sponsor_logo = benefits[0]
                    self.save()
        return self.sponsor_logo.upload

    def reset_benefits(self):
        """
        Reset all benefits for this sponsor to the defaults for their
        sponsorship level.
        """
        level = None

        try:
            level = self.level
        except SponsorLevel.DoesNotExist:
            pass

        allowed_benefits = []
        if level:
            for benefit_level in level.benefit_levels.all():
                # Create all needed benefits if they don't exist already
                sponsor_benefit, created = SponsorBenefit.objects.get_or_create(
                    sponsor=self, benefit=benefit_level.benefit)

                # and set to default limits for this level.
                sponsor_benefit.max_words = benefit_level.max_words
                sponsor_benefit.other_limits = benefit_level.other_limits

                # and set to active
                sponsor_benefit.active = True

                # @@@ We don't call sponsor_benefit.clean here. This means
                # that if the sponsorship level for a sponsor is adjusted
                # downwards, an existing too-long text entry can remain,
                # and won't raise a validation error until it's next
                # edited.
                sponsor_benefit.save()

                allowed_benefits.append(sponsor_benefit.pk)

        # Any remaining sponsor benefits that don't normally belong to
        # this level are set to inactive
        self.sponsor_benefits.exclude(pk__in=allowed_benefits).update(active=False, max_words=None, other_limits="")

    def send_coordinator_emails(self):
        for user in User.objects.filter(groups__name=SPONSOR_COORDINATORS):
            send_email(
                [user.email], "sponsor_signup",
                context = {"sponsor": self}
            )


class SponsorBenefit(models.Model):

    sponsor = models.ForeignKey(
        Sponsor,
        related_name="sponsor_benefits",
        verbose_name=_("sponsor")
    )
    benefit = models.ForeignKey(Benefit,
                                related_name="sponsor_benefits",
                                verbose_name=_("benefit")
    )
    active = models.BooleanField(default=True)

    # Limits: will initially be set to defaults from corresponding BenefitLevel
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)

    # Data: zero or one of these fields will be used, depending on the
    # type of the Benefit (text, file, or simple)
    text = models.TextField(_("text"), blank=True)
    upload = models.FileField(_("file"), blank=True, upload_to="sponsor_files")

    class Meta:
        ordering = ['-active']

    def __unicode__(self):
        return u"%s - %s" % (self.sponsor, self.benefit)

    def clean(self):
        if self.max_words and len(self.text.split()) > self.max_words:
            raise ValidationError("Sponsorship level only allows for %s words." % self.max_words)

    def data_fields(self):
        """
        Return list of data field names which should be editable for
        this ``SponsorBenefit``, depending on its ``Benefit`` type.
        """
        if self.benefit.type == "file" or self.benefit.type == "weblogo":
            return ["upload"]
        elif self.benefit.type == "text":
            return ["text"]
        return []
