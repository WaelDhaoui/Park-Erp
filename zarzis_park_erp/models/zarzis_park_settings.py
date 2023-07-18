import this

from odoo import api, fields, models, _


class CompanyChanges(models.Model):
    _inherit = "res.company"

    description = fields.Text(string="Description")


class MainShareholders(models.Model):
    _name = "main.shareholders"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Zarzis Park Erp Main Shareholders"
    _rec_name = "reference"

    reference = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _("New"))
    name_surname = fields.Char(string="Name and Surname")
    nationality_shareholders = fields.Char(string='Nationality')
    subscription_percentage = fields.Integer(string="% of subscription")

    shareholder_id = fields.Many2one("rental.submission", string="")

    # Sequence
    @api.model
    def create(self, vals):
        if not vals.get('reference'):
            vals['reference'] = 'New Shareholder'
            vals['reference'] = self.env['ir.sequence'].next_by_code('zarzis.park.erp.local') or _('New')
        res = super(MainShareholders, self).create(vals)
        return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # Check if the current user is a portal user and has the group_user access rights
        if self.env.user.has_group('base.group_portal'):
            return super().create(vals)
        else:
            return super().create(vals)

    def write(self, vals):
        # Check if the current user is a portal user
        if self.env.user.has_group('base.group_portal'):
            return False
        else:
            return super(ResPartner, self).write(vals)
