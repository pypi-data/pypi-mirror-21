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

import csv
import sys

from django.shortcuts import get_object_or_404, redirect
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _, ungettext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

import six
from six.moves.urllib.parse import urlencode

from weblate.utils import messages
from weblate.trans.exporters import get_exporter
from weblate.trans.models import Translation, Dictionary, Change
from weblate.lang.models import Language
from weblate.trans.site import get_site_url
from weblate.utils.errors import report_error
from weblate.trans.util import render
from weblate.trans.forms import WordForm, DictUploadForm, LetterForm
from weblate.permissions.helpers import (
    can_add_dictionary, can_upload_dictionary, can_delete_dictionary,
    can_change_dictionary,
)
from weblate.trans.views.helper import get_project, import_message


def dict_title(prj, lang):
    """Return dictionary title."""
    return _('%(language)s dictionary for %(project)s') % {
        'language': lang,
        'project': prj
    }


def show_dictionaries(request, project):
    obj = get_project(request, project)
    dicts = Translation.objects.filter(
        subproject__project=obj
    ).values_list('language', flat=True).distinct()

    return render(
        request,
        'dictionaries.html',
        {
            'title': _('Dictionaries'),
            'dicts': Language.objects.filter(id__in=dicts),
            'project': obj,
        }
    )


def edit_dictionary(request, project, lang):
    prj = get_project(request, project)
    if not can_change_dictionary(request.user, prj):
        raise PermissionDenied()
    lang = get_object_or_404(Language, code=lang)
    word = get_object_or_404(
        Dictionary,
        project=prj,
        language=lang,
        id=request.GET.get('id')
    )

    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word.edit(
                request,
                form.cleaned_data['source'],
                form.cleaned_data['target']
            )
            return redirect(
                'show_dictionary',
                project=prj.slug,
                lang=lang.code
            )
    else:
        form = WordForm(
            initial={'source': word.source, 'target': word.target}
        )

    last_changes = Change.objects.last_changes(request.user).filter(
        dictionary=word,
    )[:10]

    return render(
        request,
        'edit_dictionary.html',
        {
            'title': dict_title(prj, lang),
            'project': prj,
            'language': lang,
            'form': form,
            'last_changes': last_changes,
            'last_changes_url': urlencode({
                'project': prj.slug,
                'lang': lang.code,
                'glossary': 1
            }),
        }
    )


def delete_dictionary(request, project, lang):
    prj = get_project(request, project)
    if not can_delete_dictionary(request.user, prj):
        raise PermissionDenied()

    lang = get_object_or_404(Language, code=lang)
    word = get_object_or_404(
        Dictionary,
        project=prj,
        language=lang,
        id=request.POST.get('id')
    )

    word.delete()

    return redirect(
        'show_dictionary',
        project=prj.slug,
        lang=lang.code
    )


def upload_dictionary(request, project, lang):
    prj = get_project(request, project)
    if not can_upload_dictionary(request.user, prj):
        raise PermissionDenied()
    lang = get_object_or_404(Language, code=lang)

    form = DictUploadForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            count = Dictionary.objects.upload(
                request,
                prj,
                lang,
                request.FILES['file'],
                form.cleaned_data['method']
            )
            import_message(
                request, count,
                _('No words to import found in file.'),
                ungettext(
                    'Imported %d word from the uploaded file.',
                    'Imported %d words from the uploaded file.',
                    count
                )
            )
        except Exception as error:
            report_error(error, sys.exc_info(), request)
            messages.error(
                request, _('File upload has failed: %s') % force_text(error)
            )
    else:
        messages.error(request, _('Failed to process form!'))
    return redirect(
        'show_dictionary',
        project=prj.slug,
        lang=lang.code
    )


def download_dictionary_ttkit(export_format, prj, lang, words):
    """Translate-toolkit builder for dictionary downloads."""
    exporter = get_exporter(export_format)(
        prj, lang,
        get_site_url(reverse(
            'show_dictionary',
            kwargs={'project': prj.slug, 'lang': lang.code}
        ))
    )

    # Add words
    for word in words.iterator():
        exporter.add_dictionary(word)

    # Save to response
    return exporter.get_response(
        'glossary-{project}-{language}.{extension}'
    )


def download_dictionary(request, project, lang):
    """Export dictionary into various formats."""
    prj = get_project(request, project)
    lang = get_object_or_404(Language, code=lang)

    # Parse parameters
    export_format = None
    if 'format' in request.GET:
        export_format = request.GET['format']
    if export_format not in ('csv', 'po', 'tbx', 'xliff'):
        export_format = 'csv'

    # Grab all words
    words = Dictionary.objects.filter(
        project=prj,
        language=lang
    ).order_by('source')

    # Translate toolkit based export
    if export_format in ('po', 'tbx', 'xliff'):
        return download_dictionary_ttkit(export_format, prj, lang, words)

    # Manually create CSV file
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    filename = 'dictionary-{0}-{1}.csv'.format(prj.slug, lang.code)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename
    )

    writer = csv.writer(response)

    # Add header
    writer.writerow(('source', 'target'))

    for word in words.iterator():
        if six.PY2:
            writer.writerow((
                word.source.encode('utf8'), word.target.encode('utf8')
            ))
        else:
            writer.writerow((
                word.source, word.target
            ))

    return response


def show_dictionary(request, project, lang):
    prj = get_project(request, project)
    lang = get_object_or_404(Language, code=lang)

    if request.method == 'POST' and can_add_dictionary(request.user, prj):
        form = WordForm(request.POST)
        if form.is_valid():
            Dictionary.objects.create(
                request.user,
                project=prj,
                language=lang,
                source=form.cleaned_data['source'],
                target=form.cleaned_data['target']
            )
        return HttpResponseRedirect(
            request.POST.get('next', request.get_full_path())
        )
    else:
        form = WordForm()

    uploadform = DictUploadForm()

    words = Dictionary.objects.filter(
        project=prj, language=lang
    ).order_by('source')

    limit = request.GET.get('limit', 25)
    page = request.GET.get('page', 1)

    letterform = LetterForm(request.GET)

    if letterform.is_valid() and letterform.cleaned_data['letter'] != '':
        words = words.filter(
            source__istartswith=letterform.cleaned_data['letter']
        )
        letter = letterform.cleaned_data['letter']
    else:
        letter = ''

    paginator = Paginator(words, limit)

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        words = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        words = paginator.page(paginator.num_pages)

    last_changes = Change.objects.last_changes(request.user).filter(
        dictionary__project=prj,
        dictionary__language=lang
    )[:10]

    return render(
        request,
        'dictionary.html',
        {
            'title': dict_title(prj, lang),
            'project': prj,
            'language': lang,
            'page_obj': words,
            'form': form,
            'uploadform': uploadform,
            'letterform': letterform,
            'letter': letter,
            'last_changes': last_changes,
            'last_changes_url': urlencode({
                'project': prj.slug,
                'lang': lang.code,
                'glossary': 1
            }),
        }
    )
