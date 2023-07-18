import datetime

from odoo import api, fields, models, _
from odoo.http import request
from odoo.tools import formatLang
from odoo.exceptions import UserError


class RentalSubmission(models.Model):
    _name = "rental.submission"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Zarzis Park Erp Rental Submission"
    _rec_name = "reference"
    _order = 'create_date desc'

    admin_email = fields.Char(string='Admin E-mail', default="wael.dhaoui.2001@gmail.com")

    reference = fields.Char(string="Reference", copy=False, readonly=True, default=lambda self: _("New"))

    # Name of company to be created:
    state = fields.Selection([
        ('draft', 'Draft'),
        ('being_processed', 'Being Processed'),
        ('accepted', 'Accepted'),
        ('validated', 'Validated'),
        ('expired', 'Expired'),
        ('refused', 'Refused'),
    ], string='State', default="draft", tracking=True)
    name = fields.Char(string='Promoter Name & Surname')
    owner_national_id = fields.Many2one('res.country', string='Nationality')
    address = fields.Char(string='Address')
    phone = fields.Char(string='Tel')
    email = fields.Char(string='E-mail')

    # test cron
    submission_date = fields.Date(string="Submission Date")
    accepted_date = fields.Date(string="Accept Date")
    validated_date = fields.Date(string="Validate Date")
    first_refuse_date = fields.Date(string="First Refuse Date")
    second_refuse_date = fields.Date(string="Second Refuse Date")
    expire_date = fields.Date(string="Expired Date")
    send_mail_before_expire = fields.Date(string="Send email before expired date")
    locale_id = fields.Many2one('zarzis.park.erp.local', string='Related Local', readonly=True)

    # Main shareholders(precise resident / non - resident)
    first_proposal = fields.Char(string='Name of company to be created: 1st Proposal')
    second_proposal = fields.Char(string='2nd Proposal')
    third_proposal = fields.Char(string='3rd Proposal')
    activity = fields.Char(string='Activities')
    name_surname_manager = fields.Char(string='Name & surname of the manager:')
    company_national_id = fields.Many2one('res.country', string='Nationality')
    currency_id = fields.Many2one('res.currency', string='Currency')
    company_capital = fields.Monetary(string='Capital of the company to be created (EURO / US $ / TND):')

    # Requirements (in Sq m):
    shareholders_ids = fields.One2many("main.shareholders", "shareholder_id", string=" ", readonly=True)

    # Construction nature:
    category = fields.Selection([
        ('land', 'Land'),
        ('premises', 'Premises'),
        ('office', 'Office'),
    ], string='Requirements (in Sq m):', default="land")
    area_size = fields.Integer(string="Construction area (in Sq m):")

    # Number of national jobs to be created:
    construction_nature = fields.Selection([
        ('permanent', 'Permanent'),
        ('temporary', 'Temporary'),
        ('mixed', 'Mixed'),
    ], string='Construction nature:')
    description = fields.Text(string="Description")

    # Investment & financing program (EURO / US $ / TND)
    year_one = fields.Integer(string="Year 1")
    year_two = fields.Integer(string="Year 2")
    year_three = fields.Integer(string="Year 3")
    estimated_export_value = fields.Char(string="Estimated export value (in EURO / US$ / TND)")
    local_added_value = fields.Text(string="Local added value (Tunisian goods and services):")
    origin_of_imported_goods = fields.Text(string="Origin of imported goods (raw materials or merchandises):",
                                           readonly=True)
    export_destination_id = fields.Many2one('res.country',
                                            string='Export destination (manufactured goods or merchandises):')

    # INVESTMENT
    construction_equipments = fields.Monetary(string="Construction & Equipments")
    imported_equipments = fields.Monetary(string="Imported equipments")
    local_equipments = fields.Monetary(string="Local equipments")
    means_of_transport = fields.Monetary(string="Means of transport")
    other_costs = fields.Monetary(string="Other costs")
    working_capital = fields.Monetary(string="Working capital")
    total_investment = fields.Monetary(string="TOTAL")

    # FINANCING
    capital = fields.Monetary(string="Capital")
    current_account_partners = fields.Monetary(string="Current account of partners")
    long_term_credit = fields.Char(string="Long term credit")
    middle_term_credit = fields.Char(string="Middle term credit")
    short_term_credit = fields.Char(string="Short term credit")
    total_financing = fields.Monetary(string="TOTAL")

    # Wizard refused
    reason_refuse = fields.Text(string="Reason", readonly=True)

    # local smart button
    local = fields.Char(string="Local", readonly=True)

    # editable smart button
    is_unlocked = fields.Boolean(string='Unlock', default=True)

    # Qweb reference
    qweb_reference = fields.Char(string="report reference", compute="_qweb_reference")
    qweb_reference_number = fields.Integer(string="report reference number", compute="_compute_qweb_reference_number")

    # Qweb get the print's day
    print_day = fields.Date(string="Print Date", compute="_print_day", readonly=True)

    def _compute_qweb_reference_number(self):
        if self.reference:
            number_part = self.reference[-3:]
            if number_part.isdigit():
                self.qweb_reference_number = int(number_part)

    def _qweb_reference(self):
        self.qweb_reference = self.reference[-2:]

    def _print_day(self):
        self.print_day = datetime.date.today()

    def set_to_process(self):
        self.state = 'being_processed'

    def set_to_accept(self):
        self.state = 'accepted'
        self.is_unlocked = False
        self.accepted_date = datetime.date.today()
        self.second_refuse_date = datetime.date.today() + datetime.timedelta(days=15)

    def set_to_refuse(self):
        # wizard = self.env['state.refuse']

        self.ensure_one()
        if not self.email:
            raise UserError(
                _("Missing email on  '%s'.") % self.name
            )
        template = self.env.ref('zarzis_park_erp.refuse_rental_request_email_template')
        compose_form = self.env.ref("mail.email_compose_message_wizard_form")
        ctx = dict(
            default_model="rental.submission",
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode="comment",
        )
        action = {
            "name": _("Refuse Rental Request Email"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

        return action

    def set_to_validate(self):
        self.state = 'validated'
        self.validated_date = datetime.date.today()
        self.expire_date = datetime.date.today() + datetime.timedelta(days=365)
        self.send_mail_before_expire = datetime.date.today() + datetime.timedelta(days=355)

    def set_to_expire(self):
        today = datetime.date.today()
        self.expire_date = today
        self.send_mail_before_expire = False
        self.state = 'expired'
        local = self.env['zarzis.park.erp.local'].search([('id', '=', self.locale_id.id)])
        local.write({
            'state': 'not_reserved',
        })

    def cron_delay(self):
        processed_requests = request.env['rental.submission'].search([('state', '=', 'being_processed')]) or ''
        accepted_requests = request.env['rental.submission'].search([('state', '=', 'accepted')]) or ''
        validated_requests = request.env['rental.submission'].search([('state', '=', 'validated')]) or ''

        today = datetime.date.today()

        for ren in processed_requests:
            if ren.first_refuse_date == today:
                ren.reason_refuse = False
                ren.locale_id.set_to_not_reserved()
                ren.state = 'refused'

        for ren in accepted_requests:
            if ren.second_refuse_date == today:
                ren.locale_id.set_to_not_reserved()
                ren.state = 'refused'

        for ren in validated_requests:
            if ren.send_mail_before_expire == today:
                template = self.env.ref('zarzis_park_erp.send_mail_before_expire_email_template')
                for record in self:
                    template.send_mail(record.id)
            if ren.expired_date == today:
                ren.locale_id.set_to_not_reserved()
                ren.state = 'expired'

    def reserved_local_form(self):
        local_id = self.env['zarzis.park.erp.local'].search([('id', '=', self.locale_id.id)])
        return {
            'name': _('Reserved Local'),
            'type': 'ir.actions.act_window',
            'res_model': 'zarzis.park.erp.local',
            'view_mode': 'form',
            'res_id': local_id.id,
            'target': '_blank',
        }

    # Send Email when a client submit the form
    def send_mail(self):
        if self.state == "accepted":
            self.ensure_one()
            if not self.email:
                raise UserError(
                    _("Missing email on  '%s'.") % self.name
                )
            template = self.env.ref('zarzis_park_erp.accept_rental_request_email_template')
            compose_form = self.env.ref("mail.email_compose_message_wizard_form")
            ctx = dict(
                default_model="rental.submission",
                default_res_id=self.id,
                default_use_template=bool(template),
                default_template_id=template.id,
                default_composition_mode="comment",
            )
            action = {
                "name": _("Accept Rental Request"),
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "mail.compose.message",
                "view_id": compose_form.id,
                "target": "new",
                "context": ctx,
            }

            return action
        if self.state == "validated":
            self.ensure_one()
            if not self.email:
                raise UserError(
                    _("Missing email on  '%s'.") % self.name
                )
            template = self.env.ref('zarzis_park_erp.validate_rental_request_email_template')
            compose_form = self.env.ref("mail.email_compose_message_wizard_form")
            ctx = dict(
                default_model="rental.submission",
                default_res_id=self.id,
                default_use_template=bool(template),
                default_template_id=template.id,
                default_composition_mode="comment",
            )
            action = {
                "name": _("Validate Rental Request Email"),
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "mail.compose.message",
                "view_id": compose_form.id,
                "target": "new",
                "context": ctx,
            }

            return action
        # for record in self:
        #     template.send_mail(record.id)

    def edit_access_button(self):
        for rec in self:
            if rec.is_unlocked:
                rec.is_unlocked = False
            else:
                rec.is_unlocked = True

    # Sequence
    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = 'New Rental Submission'
            vals['reference'] = self.env['ir.sequence'].sudo().next_by_code('rental.submission') or _('New')
        res = super(RentalSubmission, self).create(vals)
        return res
