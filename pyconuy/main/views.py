import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from conference.models import Speaker, Proposal, Presentation, Sponsor, PresentationCategory
from main.forms import ProposalForm


def index(request):
    return render_to_response('index.html',
        {'sponsors':Sponsor.objects.filter(active=True).order_by('level__order', 'contact_name')},
        context_instance=RequestContext(request))


@login_required
def proposal_add(request):

    try:
        speaker = Speaker.objects.get(user=request.user)
    except Speaker.DoesNotExist:
        if request.user.first_name or request.user.last_name:
            name = u'{0} {1}'.format(request.user.first_name, request.user.last_name)
        else:
            name = request.user.username
        speaker = Speaker(user=request.user,
            name = name,
            invite_email = request.user.email,
            invite_token = '')

    if request.method == 'POST':
        form = ProposalForm(request.POST)

        if form.is_valid():

            #save speaker
            speaker.biography = form.cleaned_data['biography']
            speaker.annotation = speaker.annotation or ''
            speaker.save()

            #save proposal
            Proposal.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                kind=form.cleaned_data['kind'],
                category=PresentationCategory.objects.get(slug='general'),
                abstract=form.cleaned_data['abstract'],
                audience_level=form.cleaned_data['audience_level'],
                additional_notes=form.cleaned_data['additional_notes'],
                duration=form.cleaned_data['duration'],
                speaker=speaker,
                submitted=datetime.datetime.now(),
                cancelled=False)

            return HttpResponseRedirect('/proposal-sent')
    else:
        form = ProposalForm(initial={'biography': speaker.biography.raw})

    return render_to_response('proposal_add.html', {
        'form': form,
        }, context_instance=RequestContext(request))

def proposal_sent(request):
    return render_to_response('proposal_sent.html', context_instance=RequestContext(request))

def schedule(request):
    regroup = {}
    presentations = Presentation.objects.all().order_by('slot__start')
    if presentations.count() > 0:
        last_session_id = presentations[1].slot.session.id
    else:
        last_session_id = None
    session = []
    session_order = 1
    for presentation in presentations:
        session_id = presentation.slot.session.id
        if session_id == last_session_id:
            session.append(presentation)
        else:
            regroup[str(session_order)] = session
            session_order += 1
            last_session_id = session_id
            session = [presentation]
    regroup[str(session_order)] = session
    regroup = sorted(regroup.iteritems())
    return render_to_response('schedule.html',
        {'presentations_group': regroup},
        context_instance=RequestContext(request))

def sponsors(request):
    return render_to_response('sponsors.html',
        {'sponsors': Sponsor.objects.filter(active=True).order_by('level__order', 'contact_name')},
        context_instance=RequestContext(request))

def speakers(request):
    return render_to_response('speakers.html',
        {'speakers': Speaker.objects.filter(sessions_preference=1).order_by('invite_token')},
        context_instance=RequestContext(request))

def proposals(request):
    return HttpResponseRedirect(reverse("main:talks"))

def talks(request):
    return render_to_response('talks.html',
        {'proposals': Proposal.objects.filter(cancelled=False).order_by('speaker__invite_token')},
        context_instance=RequestContext(request))
