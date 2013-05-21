# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PresentationKind'
        db.create_table('conference_presentationkind', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('conference', ['PresentationKind'])

        # Adding model 'PresentationCategory'
        db.create_table('conference_presentationcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('conference', ['PresentationCategory'])

        # Adding model 'Speaker'
        db.create_table('conference_speaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='speaker_profile', unique=True, null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('biography', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('twitter_username', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('annotation', self.gf('django.db.models.fields.TextField')()),
            ('invite_email', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, db_index=True)),
            ('invite_token', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('sessions_preference', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('_biography_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('conference', ['Speaker'])

        # Adding model 'Proposal'
        db.create_table('conference_proposal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.PresentationKind'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.PresentationCategory'])),
            ('abstract', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('audience_level', self.gf('django.db.models.fields.IntegerField')()),
            ('additional_notes', self.gf('markitup.fields.MarkupField')(no_rendered_field=True, blank=True)),
            ('extreme', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='proposals', to=orm['conference.Speaker'])),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_abstract_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_additional_notes_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('conference', ['Proposal'])

        # Adding M2M table for field additional_speakers on 'Proposal'
        db.create_table('conference_proposal_additional_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proposal', models.ForeignKey(orm['conference.proposal'], null=False)),
            ('speaker', models.ForeignKey(orm['conference.speaker'], null=False))
        ))
        db.create_unique('conference_proposal_additional_speakers', ['proposal_id', 'speaker_id'])

        # Adding model 'Track'
        db.create_table('conference_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=65)),
        ))
        db.send_create_signal('conference', ['Track'])

        # Adding model 'Session'
        db.create_table('conference_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', null=True, to=orm['conference.Track'])),
        ))
        db.send_create_signal('conference', ['Session'])

        # Adding model 'Slot'
        db.create_table('conference_slot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='slots', null=True, to=orm['conference.Track'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='slots', null=True, to=orm['conference.Session'])),
        ))
        db.send_create_signal('conference', ['Slot'])

        # Adding model 'Presentation'
        db.create_table('conference_presentation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='presentation', unique=True, null=True, to=orm['conference.Slot'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.PresentationKind'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.PresentationCategory'])),
            ('abstract', self.gf('markitup.fields.MarkupField')(no_rendered_field=True)),
            ('audience_level', self.gf('django.db.models.fields.IntegerField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['conference.Speaker'])),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('extreme_pycon', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_abstract_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('conference', ['Presentation'])

        # Adding M2M table for field additional_speakers on 'Presentation'
        db.create_table('conference_presentation_additional_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('presentation', models.ForeignKey(orm['conference.presentation'], null=False)),
            ('speaker', models.ForeignKey(orm['conference.speaker'], null=False))
        ))
        db.create_unique('conference_presentation_additional_speakers', ['presentation_id', 'speaker_id'])

        # Adding model 'Benefit'
        db.create_table('conference_benefit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='simple', max_length=10)),
        ))
        db.send_create_signal('conference', ['Benefit'])

        # Adding model 'SponsorLevel'
        db.create_table('conference_sponsorlevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cost', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('conference', ['SponsorLevel'])

        # Adding model 'Sponsor'
        db.create_table('conference_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='sponsorship', unique=True, null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('external_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('annotation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['conference.SponsorLevel'], null=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('active', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sponsor_logo', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['conference.SponsorBenefit'])),
        ))
        db.send_create_signal('conference', ['Sponsor'])

        # Adding model 'SponsorBenefit'
        db.create_table('conference_sponsorbenefit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sponsor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sponsor_benefits', to=orm['conference.Sponsor'])),
            ('benefit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sponsor_benefits', to=orm['conference.Benefit'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('max_words', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('other_limits', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('upload', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('conference', ['SponsorBenefit'])


    def backwards(self, orm):
        # Deleting model 'PresentationKind'
        db.delete_table('conference_presentationkind')

        # Deleting model 'PresentationCategory'
        db.delete_table('conference_presentationcategory')

        # Deleting model 'Speaker'
        db.delete_table('conference_speaker')

        # Deleting model 'Proposal'
        db.delete_table('conference_proposal')

        # Removing M2M table for field additional_speakers on 'Proposal'
        db.delete_table('conference_proposal_additional_speakers')

        # Deleting model 'Track'
        db.delete_table('conference_track')

        # Deleting model 'Session'
        db.delete_table('conference_session')

        # Deleting model 'Slot'
        db.delete_table('conference_slot')

        # Deleting model 'Presentation'
        db.delete_table('conference_presentation')

        # Removing M2M table for field additional_speakers on 'Presentation'
        db.delete_table('conference_presentation_additional_speakers')

        # Deleting model 'Benefit'
        db.delete_table('conference_benefit')

        # Deleting model 'SponsorLevel'
        db.delete_table('conference_sponsorlevel')

        # Deleting model 'Sponsor'
        db.delete_table('conference_sponsor')

        # Deleting model 'SponsorBenefit'
        db.delete_table('conference_sponsorbenefit')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'conference.benefit': {
            'Meta': {'object_name': 'Benefit'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'simple'", 'max_length': '10'})
        },
        'conference.presentation': {
            'Meta': {'object_name': 'Presentation'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['conference.Speaker']", 'symmetrical': 'False', 'blank': 'True'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.PresentationCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'extreme_pycon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.PresentationKind']"}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'presentation'", 'unique': 'True', 'null': 'True', 'to': "orm['conference.Slot']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['conference.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'conference.presentationcategory': {
            'Meta': {'object_name': 'PresentationCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'conference.presentationkind': {
            'Meta': {'object_name': 'PresentationKind'},
            'closed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'conference.proposal': {
            'Meta': {'object_name': 'Proposal'},
            '_abstract_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_additional_notes_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'abstract': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'additional_notes': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'additional_speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['conference.Speaker']", 'symmetrical': 'False', 'blank': 'True'}),
            'audience_level': ('django.db.models.fields.IntegerField', [], {}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.PresentationCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'extreme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.PresentationKind']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': "orm['conference.Speaker']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'conference.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'null': 'True', 'to': "orm['conference.Track']"})
        },
        'conference.slot': {
            'Meta': {'object_name': 'Slot'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'slots'", 'null': 'True', 'to': "orm['conference.Session']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'slots'", 'null': 'True', 'to': "orm['conference.Track']"})
        },
        'conference.speaker': {
            'Meta': {'object_name': 'Speaker'},
            '_biography_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'biography': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'invite_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'sessions_preference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'speaker_profile'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'conference.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'active': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'annotation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'sponsorship'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'external_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['conference.SponsorLevel']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sponsor_logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['conference.SponsorBenefit']"})
        },
        'conference.sponsorbenefit': {
            'Meta': {'ordering': "['-active']", 'object_name': 'SponsorBenefit'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'benefit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsor_benefits'", 'to': "orm['conference.Benefit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_words': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'other_limits': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsor_benefits'", 'to': "orm['conference.Sponsor']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        'conference.sponsorlevel': {
            'Meta': {'ordering': "['order']", 'object_name': 'SponsorLevel'},
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'conference.track': {
            'Meta': {'object_name': 'Track'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '65'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['conference']