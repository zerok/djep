import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import models as auth_models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import generic as generic_views

from userprofiles.contrib.emailverification.models import EmailVerification
from userprofiles.contrib.emailverification.views import EmailChangeView as BaseEmailChangeView
from userprofiles.contrib.profiles.views import ProfileChangeView as BaseProfileChangeView

from . import forms
from . import models


class AutocompleteUser(generic_views.View):
    """
    This view is used for instance within the proposals application to support
    the autocompletion widget in there.

    The current implementation matches users with the dipslay namee being
    equal to the given "term" parameter and returns their speaker pk as JSON
    object.

    TODO: Evaluation if this might be better placed somewhere within the
          speakers application.
    """

    def get_matching_users(self, term):
        """
        Returns a list of dicts containing a user's name ("label") and her
        speaker pk ("value").
        """
        result = []
        for profile in models.Profile.objects.filter(
                display_name__icontains=term):
            user = profile.user
            result.append({
                'label': u'{0} ({1})'.format(profile.display_name,
                    user.username),
                'value': user.speaker_profile.pk
            })
        return result

    def get(self, request):
        term = request.GET['term']
        result = []
        if term and len(term) >= 2:
            result = self.get_matching_users(term)
        return HttpResponse(json.dumps(result))


class ProfileView(generic_views.TemplateView):
    """
    Displays a profile page for the given user. If the user also has a
    speaker_profile, also render the information given there.
    """

    template_name = 'userprofiles/profile_view.html'

    def get_context_data(self, uid):
        user = get_object_or_404(auth_models.User, pk=uid)
        speaker_profile = user.speaker_profile
        sessions = None
        profile = user.get_profile()
        if speaker_profile:
            sessions = list(speaker_profile.sessions.all()) + list(speaker_profile.session_participations.all())
        return {
            'userobj': user,
            'speaker_profile': speaker_profile,
            'sessions': sessions,
            'profile': profile
        }


class LoginEmailRequestView(generic_views.FormView):
    """
    Requests an email address for the user currently trying to login. If the
    input is valid, continue the login process.
    """

    form_class = forms.LoginEmailRequestForm
    template_name = 'accounts/login-email-request.html'

    def form_valid(self, form):
        data = self.request.session[getattr(settings, 'SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')]
        backend = data['backend']
        user_pk = data['kwargs']['user']['pk']
        if form.cleaned_data['email']:
            user = auth_models.User.objects.get(pk=user_pk)
            EmailVerification.objects.create_new_verification(
                user, form.cleaned_data['email'])
        self.request.session['_email_passed_{0}'.format(user_pk)] = True
        return HttpResponseRedirect('/complete/{0}/'.format(backend))


class EmailChangeView(BaseEmailChangeView):
    form_class = forms.ChangeEmailForm


class ProfileChangeView(BaseProfileChangeView):
    def form_invalid(self, form):
        messages.error(self.request, _('An error occurred while saving the form.'))
        return super(ProfileChangeView, self).form_invalid(form)
