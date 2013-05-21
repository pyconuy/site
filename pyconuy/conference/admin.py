# -*- coding: utf-8 -*-
from django.contrib import admin

from conference.models import (PresentationKind, PresentationCategory, Proposal, Session, Track, Slot, Presentation,
                               Speaker, Sponsor, SponsorLevel, SponsorBenefit, Benefit)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class KindAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SponsorBenefitInline(admin.StackedInline):
    model = SponsorBenefit
    extra = 0
    fieldsets = [
        (None, {
            "fields": [
                ("benefit", "active"),
                ("max_words", "other_limits"),
                "text",
                "upload",
                ]
        })
    ]


class SponsorAdmin(admin.ModelAdmin):

    save_on_top = True
    fieldsets = [
        (None, {
            "fields": [
                ("name", "applicant"),
                ("level", "active"),
                "external_url",
                "annotation",
                ("contact_name", "contact_email")
            ]
        }),
        ("Metadata", {
            "fields": ["added"],
            "classes": ["collapse"]
        })
    ]
    inlines = [SponsorBenefitInline]

    def get_form(self, *args, **kwargs):
        # @@@ kinda ugly but using choices= on NullBooleanField is broken
        form = super(SponsorAdmin, self).get_form(*args, **kwargs)
        form.base_fields["active"].widget.choices = [
            (u"1", "unreviewed"),
            (u"2", "approved"),
            (u"3", "rejected")
        ]
        return form


admin.site.register(PresentationCategory, CategoryAdmin)
admin.site.register(PresentationKind, KindAdmin)
admin.site.register(Proposal,
                    list_display=[
                        "id",
                        "title",
                        "speaker",
                        "speaker_email",
                        "kind",
                        "audience_level",
                        "cancelled",
                        ],
                    list_filter=[
                        "kind__name",
                        # "result__accepted",
                        ],
                    )
admin.site.register(Session)
admin.site.register(Track,
                    list_display=["pk", "name"]
)

admin.site.register(Slot,
                    list_display=["pk", "title", "start", "end", "track"]
)

admin.site.register(Presentation,
                    list_display=[
                        "pk",
                        "title",
                        "slot",
                        "kind",
                        "audience_level",
                        "cancelled"
                    ],
                    list_filter=[
                        "kind",
                        "cancelled",
                        ],
                    raw_id_fields = ["speaker"]
)

admin.site.register(Speaker,
                    list_display = ["name", "email", "twitter_username", "sessions_preference", "created"],
                    search_fields = ["name"],
                    )
admin.site.register(SponsorLevel)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Benefit)