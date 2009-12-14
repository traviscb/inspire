## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""
WebStyle templates. Customize the look of pages of CDS Invenio
"""
__revision__ = \
    "$Id$"

import time
import cgi

from invenio.config import \
     CFG_SITE_LANG, \
     CFG_SITE_NAME, \
     CFG_SITE_NAME_INTL, \
     CFG_SITE_SUPPORT_EMAIL, \
     CFG_SITE_SECURE_URL, \
     CFG_SITE_URL, \
     CFG_VERSION, \
     CFG_WEBSTYLE_INSPECT_TEMPLATES, \
     CFG_WEBSTYLE_TEMPLATE_SKIN

from invenio.messages import gettext_set_language
from invenio.webstyle_templates import Template as DefaultTemplate

class Template(DefaultTemplate):
    """INSPIRE style templates."""


    def tmpl_pageheader(self, req, ln=CFG_SITE_LANG, headertitle="",
                        description="", keywords="", userinfobox="",
                        useractivities_menu="", adminactivities_menu="",
                        navtrailbox="", pageheaderadd="", uid=0,
                        secure_page_p=0, navmenuid="admin", metaheaderadd="",
                        rssurl=CFG_SITE_URL+"/rss", body_css_classes=None):

        """Creates a page header

           Parameters:

          - 'ln' *string* - The language to display

          - 'headertitle' *string* - the second part of the page HTML title

          - 'description' *string* - description goes to the metadata in the header of the HTML page

          - 'keywords' *string* - keywords goes to the metadata in the header of the HTML page

          - 'userinfobox' *string* - the HTML code for the user information box

          - 'useractivities_menu' *string* - the HTML code for the user activities menu

          - 'adminactivities_menu' *string* - the HTML code for the admin activities menu

          - 'navtrailbox' *string* - the HTML code for the navigation trail box

          - 'pageheaderadd' *string* - additional page header HTML code

          - 'uid' *int* - user ID

          - 'secure_page_p' *int* (0 or 1) - are we to use HTTPS friendly page elements or not?

          - 'navmenuid' *string* - the id of the navigation item to highlight for this page

          - 'metaheaderadd' *string* - list of further tags to add to the <HEAD></HEAD> part of the page

          - 'rssurl' *string* - the url of the RSS feed for this page

          - 'body_css_classes' *list* - list of classes to add to the body tag

           Output:

          - HTML code of the page headers
        """

        # load the right message language
        _ = gettext_set_language(ln)

        if body_css_classes is None:
            body_css_classes = []
        body_css_classes.append(navmenuid)

        if CFG_WEBSTYLE_INSPECT_TEMPLATES:
            inspect_templates_message = '''
<table width="100%%" cellspacing="0" cellpadding="2" border="0">
<tr bgcolor="#aa0000">
<td width="100%%">
<font color="#ffffff">
<strong>
<small>
CFG_WEBSTYLE_INSPECT_TEMPLATES debugging mode is enabled.  Please
hover your mouse pointer over any region on the page to see which
template function generated it.
</small>
</strong>
</font>
</td>
</tr>
</table>
'''
        else:
            inspect_templates_message = ""

        out = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="%(ln_iso_639_a)s" xml:lang="%(ln_iso_639_a)s">
<head>
 <title>%(headertitle)s - %(sitename)s</title>
 <link rev="made" href="mailto:%(sitesupportemail)s" />
 <link rel="stylesheet" href="%(cssurl)s/img/invenio%(cssskin)s.css" type="text/css" />
 <link rel="alternate" type="application/rss+xml" title="%(sitename)s RSS" href="%(rssurl)s" />
 <link rel="unapi-server" type="application/xml" title="unAPI" href="%(unAPIurl)s" />
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
 <meta http-equiv="Content-Language" content="%(ln)s" />
 <meta name="description" content="%(description)s" />
 <meta name="keywords" content="%(keywords)s" />
 %(metaheaderadd)s
</head>

<body%(body_css_classes)s lang="%(ln_iso_639_a)s">
<div class="pageheader">
%(inspect_templates_message)s
 
<span class="warning"><small>Welcome to an <a class="nearestterms" href="http://www.projecthepinspire.net">Inspire</a> test server.
Please go to <a class="nearestterms" href="http://www.slac.stanford.edu/spires/">SPIRES</a> if you are here by mistake.</small></span>


<!-- replaced page header -->





<table class="headerbox"  cellspacing="0">
 <tr>
  <td align="left">
    <div>
      <a href="%(siteurl)s?ln=%(ln)s">
       <img border="0" src="%(cssurl)s/img/inspire_logo.png" alt="INSPIRE"
 />
      </a>
    </div>
  </td>
  <td  class="feedbackbox">
   <div class="feedbackboxbody">
    %(feedback)s
   </div>
  </td>
 </tr>
</table>
 
<div class="navbar">
<a id="nav-hep" href="%(siteurl)s?ln=%(ln)s">Hep</a>
::
<a id="nav-jobs" href="%(siteurl)s/help/?ln=%(ln)s">%(msg_help)s</a>
&nbsp;&nbsp;&nbsp;
..::..
&nbsp;&nbsp;&nbsp;
<a id="nav-hepnames" href="http://www.slac.stanford.edu/spires/hepnames/">HepNames</a>
::
<a id="nav-inst" href="http://www.slac.stanford.edu/spires/institutions/">Inst</a>
::
<a id="nav-conf" href="http://www.slac.stanford.edu/spires/conferences/">Conf</a>
::
<a id="nav-exp" href="http://www.slac.stanford.edu/spires/experiments/">Exp</a>
::
<a id="nav-jobs" href="http://www.slac.stanford.edu/spires/jobs/">Jobs</a>
</div>
<table class="navtrailbox">
 <tr>
  <td class="navtrailboxbody">
   %(navtrailbox)s
  </td>
 </tr>
</table>
<!-- end replaced page header -->
%(pageheaderadd)s
</div>
        """ % {
          'siteurl' : CFG_SITE_URL,
          'sitesecureurl' : CFG_SITE_SECURE_URL,
          'cssurl' : secure_page_p and CFG_SITE_SECURE_URL or CFG_SITE_URL,
          'cssskin' : CFG_WEBSTYLE_TEMPLATE_SKIN != 'default' and '_' + CFG_WEBSTYLE_TEMPLATE_SKIN or '',
          'rssurl': rssurl,
          'ln' : ln,
          'ln_iso_639_a' : ln.split('_', 1)[0],
          'langlink': '?ln=' + ln,

          'sitename' : CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME),
          'headertitle' : cgi.escape(headertitle),

          'sitesupportemail' : CFG_SITE_SUPPORT_EMAIL,

          'description' : cgi.escape(description),
          'keywords' : cgi.escape(keywords),
          'metaheaderadd' : metaheaderadd,

          'userinfobox' : userinfobox,
          'navtrailbox' : navtrailbox,
          'useractivities': useractivities_menu,
          'adminactivities': adminactivities_menu and ('<td class="headermoduleboxbodyblank">&nbsp;</td><td class="headermoduleboxbody%(personalize_selected)s">%(adminactivities)s</td>' % \
          {'personalize_selected': navmenuid.startswith('admin') and "selected" or "",
          'adminactivities': adminactivities_menu}) or '<td class="headermoduleboxbodyblank">&nbsp;</td>',

          'pageheaderadd' : pageheaderadd,
          'body_css_classes' : body_css_classes and ' class="%s"' % ' '.join(body_css_classes) or '',

          'search_selected': navmenuid == 'search' and "selected" or "",
          'submit_selected': navmenuid == 'submit' and "selected" or "",
          'personalize_selected': navmenuid.startswith('your') and "selected" or "",
          'help_selected': navmenuid == 'help' and "selected" or "",

          'msg_search' : _("Search"),
          'msg_submit' : _("Submit"),
          'msg_personalize' : _("Personalize"),
          'msg_help' : _("Help"),
          'languagebox' : self.tmpl_language_selection_box(req, ln),

          'feedback' : self.tmpl_feedback_box(ln),

          'unAPIurl' : cgi.escape('%s/unapi' % CFG_SITE_URL),
          'inspect_templates_message' : inspect_templates_message

        }
        return out


    def tmpl_feedback_box(self, ln=CFG_SITE_LANG):

        _ = gettext_set_language(ln)


        out = """
        <div class = "feedbackbox">
        <div class = "top-right">
        %(feedback_text)s <a
        href="mailto:%(feedback_address)s">%(feedback_address)s
        </a>
        </div>
        </div>""" % {
            'feedback_text' : _("Please send feedback on INSPIRE to"),
            'feedback_address' : 'feedback@inspire-hep.net',
            }
        return out
