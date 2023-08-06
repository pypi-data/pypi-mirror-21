# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2017 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

import json
import re
import unicodedata

from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

from six.moves.urllib.request import Request, urlopen

from social_core.pipeline.partial import partial
from social_core.exceptions import (
    AuthException, AuthMissingParameter, AuthAlreadyAssociated
)

from weblate.accounts.notifications import send_notification_email
from weblate.accounts.models import VerifiedEmail
from weblate import USER_AGENT

USERNAME_RE = r'^[\w.@+-]+$'
USERNAME_MATCHER = re.compile(USERNAME_RE)
STRIP_MATCHER = re.compile(r'[^\w\s.@+-]')
CLEANUP_MATCHER = re.compile(r'[-\s]+')


def get_github_email(access_token):
    """Get real email from GitHub"""

    request = Request('https://api.github.com/user/emails')
    request.timeout = 1.0
    request.add_header('User-Agent', USER_AGENT)
    request.add_header(
        'Authorization',
        'token {0}'.format(access_token)
    )
    handle = urlopen(request)
    data = json.loads(handle.read().decode('utf-8'))
    email = None
    for entry in data:
        # Skip not verified ones
        if not entry['verified']:
            continue
        email = entry['email']
        if entry['primary']:
            break
    return email


@partial
def require_email(strategy, backend, details, user=None, is_new=False,
                  **kwargs):
    """Force entering email for backends which don't provide it."""

    if backend.name == 'github':
        email = get_github_email(kwargs['response']['access_token'])
        if email is not None:
            details['email'] = email

    if user and user.email:
        # Force validation of new email address
        if backend.name == 'email':
            return {'is_new': True}

        return

    elif is_new and not details.get('email'):
        return redirect('register')


def send_validation(strategy, backend, code):
    """Send verification email."""

    # We need to have existing session
    if not strategy.request.session.session_key:
        strategy.request.session.create()

    template = 'activation'
    if strategy.request.session.pop('password_reset', False):
        template = 'reset'

    url = '{0}?verification_code={1}&id={2}&type={3}'.format(
        reverse('social:complete', args=(backend.name,)),
        code.code,
        strategy.request.session.session_key,
        template
    )

    send_notification_email(
        None,
        code.email,
        template,
        info=url,
        context={
            'url': url
        }
    )


def password_reset(strategy, details, user=None, **kwargs):
    """Set unusable password on reset."""
    if (strategy.request is not None and
            user is not None and
            strategy.request.GET.get('type', '') == 'reset'):
        user.set_unusable_password()
        user.save()


def verify_open(strategy, backend, user=None, **kwargs):
    """Check whether it is possible to create new user."""

    if not user and not settings.REGISTRATION_OPEN:
        raise AuthException(backend, _('New registrations are disabled!'))


def verify_username(strategy, backend, details, user=None, **kwargs):
    """Verified whether username is still free.

    It can happen that user has registered several times or other user has
    taken the username meanwhile.
    """
    if user or 'username' not in details:
        return
    if User.objects.filter(username__iexact=details['username']).exists():
        raise AuthAlreadyAssociated(
            backend,
            _('This username is already taken. Please choose another.')
        )


def store_email(strategy, backend, user, social, details, **kwargs):
    """Store verified email."""
    if 'email' not in details or details['email'] is None:
        raise AuthMissingParameter(backend, 'email')
    verified, dummy = VerifiedEmail.objects.get_or_create(social=social)
    if verified.email != details['email']:
        verified.email = details['email']
        verified.save()


def user_full_name(strategy, details, user=None, **kwargs):
    """Update user full name using data from provider."""
    if user:
        full_name = details.get('fullname', '').strip()

        if (not full_name and
                ('first_name' in details or 'last_name' in details)):
            first_name = details.get('first_name', '')
            last_name = details.get('last_name', '')

            if first_name and first_name not in last_name:
                full_name = '{0} {1}'.format(first_name, last_name)
            elif first_name:
                full_name = first_name
            else:
                full_name = last_name

        full_name = full_name.strip()

        # The Django User model limit is 30 chars, this should
        # be raised if we switch to custom User model
        if len(full_name) > 30:
            full_name = full_name[:30]

        if full_name and full_name != user.first_name:
            user.first_name = full_name
            strategy.storage.user.changed(user)


def slugify_username(value):
    """Clean up username

    This is based on Django slugify with exception of lowercasing

    - Converts to ascii
    - Removes not wanted chars
    - Merges whitespaces and - into single -
    """
    value = unicodedata.normalize(
        'NFKD', force_text(value)
    ).encode(
        'ascii', 'ignore'
    ).decode('ascii')

    # Return username if it matches our standards
    if USERNAME_MATCHER.match(value):
        return value

    value = STRIP_MATCHER.sub('', value).strip()
    return CLEANUP_MATCHER.sub('-', value)
