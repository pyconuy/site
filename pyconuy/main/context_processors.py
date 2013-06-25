# -*- coding: utf-8 -*-
from main.models import SiteConfig
from django.contrib.sites.models import get_current_site
from django.db.models import ObjectDoesNotExist
from django.conf import settings

def add_site_config(request):
    try:
        config = SiteConfig.objects.get(site=get_current_site(request))
        return {'config': config.to_dict()}
    except ObjectDoesNotExist:
        return {}

def add_settings(request):
    return {'settings': settings}
