# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request
from datetime import datetime
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo import http, _
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from collections import OrderedDict
import re
import json
import base64
from odoo.exceptions import ValidationError
import requests
from urllib.parse import urlencode
from urllib.request import urlopen
from datetime import datetime, timedelta
from datetime import date
from werkzeug.utils import redirect

import random


from odoo import http  
from odoo.http import request
import json
import logging
import string

_logger = logging.getLogger(__name__)


class ClientePortal(http.Controller):

    @http.route('/cliente', auth='user', website=True)
    def portal_documentos(self, **kw):
        search_term = kw.get('search', '').strip()
        domain = []

        if search_term:
            domain += [('name', 'ilike', search_term)]

        partners = request.env['res.partner'].sudo().search(domain)
        return request.render("crm_social_links.cliente", {
            'partners': partners,
            'search': search_term  # para mantener el término en el input si lo necesitas
        })
