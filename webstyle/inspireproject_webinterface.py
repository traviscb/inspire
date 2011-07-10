## This file is part of Invenio.
## Copyright (C) 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

# pylint: disable=C0103
"""INSPIRE HEP Project Web Interface URL Handlers"""

import sys
if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
        simplejson_available = True
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        simplejson_available = False
else:
    import json
    simplejson_available = True

import invenio.template
from invenio.access_control_engine import acc_authorize_action
from invenio.bibedit_engine import perform_request_ajax, perform_request_init, \
    perform_request_newticket, perform_request_compare
from invenio.bibedit_utils import json_unicode_to_utf8
from invenio.bibtask import task_low_level_submission
from invenio.config import CFG_SITE_LANG, CFG_SITE_URL, CFG_SITE_RECORD
from invenio.messages import gettext_set_language
from invenio.search_engine import guess_primary_collection_of_a_record
from invenio.urlutils import redirect_to_url
from invenio.webinterface_handler import WebInterfaceDirectory, wash_urlargd
from invenio.webpage import page
from invenio.webuser import collect_user_info, getUid, page_not_authorized


navtrail = (' <a class="navtrail" href=\"%s/inspire\">INSPIRE Utilities</a> '
            ) % CFG_SITE_URL


class WebInterfaceInspirePages(WebInterfaceDirectory):
    """Defines the set of /inspire pages."""

    _exports = ['', '/', 'file_upload']

    def __init__(self, recid=None):
        self.recid = recid
        self.template = invenio.template.load('inspireproject')

    def index(self, request, form):
        #permission = check_request_allowed(request)
        #if permission != True:
        #    return permission

        #f = wash_urlargd(form, {
        #        'recID':   (int, -1),
        #        #'offset':  (int, 0),
        #        #'perPage': (int, 30),
        #        })

        #if f['recID'] != -1:
        #    return self.rec(request, f)

        return invenio.webpage.page(title = "INSPIRE Project Page",
                                    body = self.template.index(),
                                    req = request)

    def file_upload(self, request, form):
        """Accept a stream of bytes for the disk and some metadata for the DB"""
        # bytes coming in off of filedata
        import tempfile, os
        # other form elements: username, recid, etc.
        bytes = form.get('filedata', None)
        if bytes:
            fd, fpath = tempfile.mkstemp(prefix='inspire_file_upload')
            os.write(fd, bytes.value)
            os.close(fd)
            #SUCCESS: TODO:
            # * create marcxml to send to bibupload
            marc_fd, marc_fpath = tempfile.mkstemp(prefix='inspire_file_upload', suffix="marcxml")

            task_low_level_submission('bibupload', 'file_upload', '-P', '5', '-c', '%s' % marcfpath)

            # * create ticket w/ link to bibdoc web admin
            return invenio.webpage.page(title = "File written to disk",
                                        body = fpath,
                                        req = request)
        # FAILURE: file data wasn't present (the form is unvalidated?)
        return invenio.webpage.page(title = "no bytes to write", body = "oops, lol", req=request)

    def __call__(self, req, form):
        """Redirect calls without final slash."""
        redirect_to_url(req, '%s/inspire/' % (CFG_SITE_URL))
