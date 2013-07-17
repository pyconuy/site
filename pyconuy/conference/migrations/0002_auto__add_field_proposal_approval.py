# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Proposal.approval'
        db.add_column(u'conference_proposal', 'approval',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Proposal.approval'
        db.delete_column(u'conference_proposal', 'approval')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'conference.benefit': {
            'Meta': {'object_name': 'Benefit'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '10'})
        },
        u'conference.presentation': {
            'Meta': {'object_name': 'Presentation'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['conference.Speaker']", 'symmetrical': 'False', 'blank': 'True'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.PresentationCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'extreme_pycon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.PresentationKind']"}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'presentation'", 'unique': 'True', 'null': 'True', 'to': u"orm['conference.Slot']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': u"orm['conference.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'conference.presentationcategory': {
            'Meta': {'object_name': 'PresentationCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'conference.presentationkind': {
            'Meta': {'object_name': 'PresentationKind'},
            'closed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'conference.proposal': {
            'Meta': {'object_name': 'Proposal'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_additional_notes_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_notes': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['conference.Speaker']", 'symmetrical': 'False', 'blank': 'True'}),
            'approval': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.PresentationCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'extreme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.PresentationKind']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': u"orm['conference.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'conference.session': {
            'Meta': {'object_name': 'Session'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'null': 'True', 'to': u"orm['conference.Track']"})
        },
        u'conference.slot': {
            'Meta': {'object_name': 'Slot'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'slots'", 'null': 'True', 'to': u"orm['conference.Session']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'slots'", 'null': 'True', 'to': u"orm['conference.Track']"})
        },
        u'conference.speaker': {
            'Meta': {'object_name': 'Speaker'},
            '_biography_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'biography': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'invite_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'sessions_preference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'speaker_profile'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'conference.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'active': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'annotation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'sponsorship'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'external_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.SponsorLevel']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sponsor_logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['conference.SponsorBenefit']"})
        },
        u'conference.sponsorbenefit': {
            'Meta': {'ordering': "['-active']", 'object_name': 'SponsorBenefit'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'benefit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsor_benefits'", 'to': u"orm['conference.Benefit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_words': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_limits': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsor_benefits'", 'to': u"orm['conference.Sponsor']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'conference.sponsorlevel': {
            'Meta': {'ordering': "['order']", 'object_name': 'SponsorLevel'},
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'conference.track': {
            'Meta': {'object_name': 'Track'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '65'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['conference']